import pandas as pd
import os
import re
from tqdm import tqdm

# Config
ARCHIVES_PATH = 'data/archives_retronews_shuffled.csv'
RIXES_PATH = 'data/annotated_dataset_deduped.csv'
VALIDATION_PATH = 'data/validation.csv'
YEARLY_FOLDER = '/store/retronews/etrangers'
TEST_OUTPUT = 'data/test_1to4.csv'
TRAIN_OUTPUT = 'data/train_1to3.csv'
TEST_POS_FRAC = 0.25
NEG_RATIO_TEST = 4
NEG_RATIO_TRAIN = 3
RIXES_SAMPLE_SIZE = 50
RANDOM_STATE = 42

def extract_year(filename):
    match = re.search(r'(\d{4})', filename)
    return int(match.group(1)) if match else None

# Load validation set and collect uniqueids
print("Loading validation set...")
df_val = pd.read_csv(VALIDATION_PATH)
val_ids = set(df_val['uniqueid'].astype(str))

# Load annotated positives
print("Loading annotated positives...")
df_annotated = pd.read_csv(ARCHIVES_PATH)
df_annotated['retronews_uniqueid'] = df_annotated['retronews_uniqueid'].astype(str)
df_annotated['uniqueid'] = df_annotated['retronews_uniqueid'].apply(lambda x: x.split('|')[0].strip())
df_annotated['label'] = 1
df_annotated['source_file'] = os.path.basename(ARCHIVES_PATH)
df_annotated['year'] = None

# Remove positives that are in validation
df_annotated = df_annotated[~df_annotated['uniqueid'].isin(val_ids)]

# Split positives into test/train
print("Splitting positives into test/train...")
df_test_pos = df_annotated.sample(frac=TEST_POS_FRAC, random_state=RANDOM_STATE)
test_ids = set(df_test_pos['uniqueid'])
df_train_pos = df_annotated[~df_annotated['uniqueid'].isin(test_ids)].copy()

# Load unannotated secondary data
print("Loading unannotated data by year...")
frames = []
for filename in tqdm(os.listdir(YEARLY_FOLDER), desc="Reading CSVs"):
    if filename.endswith('.csv'):
        path = os.path.join(YEARLY_FOLDER, filename)
        df_year = pd.read_csv(path, low_memory=False)
        df_year['source_file'] = filename
        df_year['year'] = extract_year(filename)
        frames.append(df_year)

df_unannotated = pd.concat(frames, ignore_index=True)
df_unannotated['uniqueid'] = df_unannotated['uniqueid'].astype(str)
df_unannotated['label'] = 0

# Remove any rows with uniqueids identical to an item in validation set
df_unannotated = df_unannotated[~df_unannotated['uniqueid'].isin(val_ids)]

# Stratified sampling for secondary dataset
def stratified_sample(df_pool, total_needed, seed):
    year_counts = df_pool['year'].value_counts(normalize=True)
    samples = []
    for year, frac in year_counts.items():
        n = int(total_needed * frac)
        year_df = df_pool[df_pool['year'] == year]
        if n > len(year_df):
            n = len(year_df)
        sample = year_df.sample(n=n, random_state=seed)
        samples.append(sample)
    return pd.concat(samples, ignore_index=True)

# Sample test negatives
print("Sampling negatives for test set...")
df_test_neg_pool = df_unannotated[~df_unannotated['uniqueid'].isin(test_ids)].copy()
num_test_neg = len(df_test_pos) * NEG_RATIO_TEST
df_test_neg = stratified_sample(df_test_neg_pool, num_test_neg, RANDOM_STATE)

# Sample training negatives
print("Sampling negatives for training set...")
num_train_neg = len(df_train_pos) * NEG_RATIO_TRAIN
df_train_neg = stratified_sample(df_unannotated, num_train_neg, RANDOM_STATE + 1)

# Load and sample rixes data (balancing positives/negatives)
print("Adding balanced sample from rixes...")
df_rixes = pd.read_csv(RIXES_PATH)
df_rixes['uniqueid'] = df_rixes['uniqueid'].astype(str)
df_rixes = df_rixes[~df_rixes['uniqueid'].isin(val_ids)]

df_rixes['label'] = df_rixes['relevant'].apply(lambda x: 1 if x == 1 else 0)
rixes_pos = df_rixes[df_rixes['label'] == 1].sample(n=RIXES_SAMPLE_SIZE // 2, random_state=RANDOM_STATE)
rixes_neg = df_rixes[df_rixes['label'] == 0].sample(n=RIXES_SAMPLE_SIZE // 2, random_state=RANDOM_STATE + 1)
df_rixes_sample = pd.concat([rixes_pos, rixes_neg], ignore_index=True)
df_rixes_sample['source_file'] = 'rixes.csv'
df_rixes_sample['year'] = None
df_rixes_sample = df_rixes_sample[['text', 'label', 'uniqueid', 'source_file', 'year']]

# Format and save test set
df_test_pos = df_test_pos[['text', 'label', 'uniqueid', 'source_file']].copy()
df_test_pos['year'] = None
df_test_neg = df_test_neg[['text', 'label', 'uniqueid', 'source_file', 'year']]
df_test = pd.concat([df_test_pos, df_test_neg], ignore_index=True)
df_test = df_test.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
df_test = df_test[~df_test['uniqueid'].isin(val_ids)]  # Final check
df_test.to_csv(TEST_OUTPUT, index=False)
print(f"Test set saved: {TEST_OUTPUT} ({len(df_test_pos)} positives, {len(df_test_neg)} negatives)")

# Format and save train set
df_train_pos = df_train_pos[['text', 'label', 'uniqueid', 'source_file']].copy()
df_train_pos['year'] = None
df_train_neg = df_train_neg[['text', 'label', 'uniqueid', 'source_file', 'year']]
df_train = pd.concat([df_train_pos, df_train_neg, df_rixes_sample], ignore_index=True)
df_train = df_train.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
df_train = df_train[~df_train['uniqueid'].isin(val_ids)]  # Final check
df_train.to_csv(TRAIN_OUTPUT, index=False)
print(f"Training set saved: {TRAIN_OUTPUT} ({len(df_train_pos)} positives, {len(df_train_neg)} negatives, including {len(df_rixes_sample)} rixes)")




