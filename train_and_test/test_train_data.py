import pandas as pd
import os
import re
from tqdm import tqdm

"""
Create train and test datasets with stratified sampling from the unannotated dataset.
"""

# config
ANNOTATED_PATH = 'data/archives_retronews_shuffled.csv'
YEARLY_FOLDER = '/store/retronews/etrangers'
TEST_OUTPUT = 'data/test_1to4.csv'
TRAIN_OUTPUT = 'data/train_1to3.csv'
TEST_POS_FRAC = 0.25
NEG_RATIO_TEST = 4
NEG_RATIO_TRAIN = 3
RANDOM_STATE = 42

def extract_year(filename):
    match = re.search(r'(\d{4})', filename)
    return int(match.group(1)) if match else None

# load annotated positives
print("Loading annotated positives...")
df_annotated = pd.read_csv(ANNOTATED_PATH)
df_annotated['retronews_uniqueid'] = df_annotated['retronews_uniqueid'].astype(str)
df_annotated['uniqueid'] = df_annotated['retronews_uniqueid'].apply(lambda x: x.split('|')[0].strip())
df_annotated['label'] = 1
df_annotated['source_file'] = os.path.basename(ANNOTATED_PATH)
df_annotated['year'] = None  # not relevant for annotated positives

# split positives into test/train parts
print("Splitting positives into test/train...")
df_test_pos = df_annotated.sample(frac=TEST_POS_FRAC, random_state=RANDOM_STATE)
test_ids = set(df_test_pos['uniqueid'])
df_train_pos = df_annotated[~df_annotated['uniqueid'].isin(test_ids)].copy()

# load unannotated data
print("Loading unannotated data by year...")
frames = []
for filename in tqdm(os.listdir(YEARLY_FOLDER), desc="Reading yearly CSVs"):
    if filename.endswith('.csv'):
        path = os.path.join(YEARLY_FOLDER, filename)
        df_year = pd.read_csv(path, low_memory=False)
        df_year['source_file'] = filename
        df_year['year'] = extract_year(filename)
        frames.append(df_year)

df_unannotated = pd.concat(frames, ignore_index=True)
df_unannotated['uniqueid'] = df_unannotated['uniqueid'].astype(str)
df_unannotated['label'] = 0

# year stratified sampling
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

# test negatib=ves
print("Sampling negatives for test set...")
df_test_neg_pool = df_unannotated[~df_unannotated['uniqueid'].isin(test_ids)].copy()
num_test_neg = len(df_test_pos) * NEG_RATIO_TEST
df_test_neg = stratified_sample(df_test_neg_pool, num_test_neg, RANDOM_STATE)

# train negatives
print("🔹 Sampling negatives for training set...")
num_train_neg = len(df_train_pos) * NEG_RATIO_TRAIN
df_train_neg = stratified_sample(df_unannotated, num_train_neg, RANDOM_STATE + 1)

# format and save test set
df_test_pos = df_test_pos[['text', 'label', 'uniqueid', 'source_file']].copy()
df_test_pos['year'] = None
df_test_neg = df_test_neg[['text', 'label', 'uniqueid', 'source_file', 'year']]
df_test = pd.concat([df_test_pos, df_test_neg], ignore_index=True)
df_test = df_test.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
df_test.to_csv(TEST_OUTPUT, index=False)
print(f"Test set saved: {TEST_OUTPUT} ({len(df_test_pos)} positives, {len(df_test_neg)} negatives)")

# forrmat and save train set
df_train_pos = df_train_pos[['text', 'label', 'uniqueid', 'source_file']].copy()
df_train_pos['year'] = None
df_train_neg = df_train_neg[['text', 'label', 'uniqueid', 'source_file', 'year']]
df_train = pd.concat([df_train_pos, df_train_neg], ignore_index=True)
df_train = df_train.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
df_train.to_csv(TRAIN_OUTPUT, index=False)
print(f"Training set saved: {TRAIN_OUTPUT} ({len(df_train_pos)} positives, {len(df_train_neg)} negatives)")



