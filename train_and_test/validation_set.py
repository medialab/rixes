import pandas as pd

"""
Create validation set with balanced sampling from archives and rixes datasets.
"""

# Load full datasets
rixes = pd.read_csv("data/annotated_dataset_deduped.csv")
archives = pd.read_csv("data/archives_retronews_shuffled.csv")

# Assign labels
rixes['label'] = rixes['relevant'].apply(lambda x: 1 if x == 1 else 0)
archives['label'] = archives['in_retronews'].apply(lambda x: 1 if x == 1 else 0)

# Clean rixes: keep necessary columns
rixes = rixes[['uniqueid', 'text', 'label']].copy()
rixes['uniqueid'] = rixes['uniqueid'].astype(str)

# Clean archives: remove any old uniqueid, rename retronews_uniqueid
archives = archives.drop(columns=[col for col in archives.columns if col == 'uniqueid'], errors='ignore')
archives = archives.rename(columns={'retronews_uniqueid': 'uniqueid'})
archives = archives[['uniqueid', 'text', 'label']].copy()
archives['uniqueid'] = archives['uniqueid'].astype(str)

# Concatenate datasets
df = pd.concat([rixes, archives], ignore_index=True)

# Drop empty or missing text
df = df.dropna(subset=['text'])
df['text'] = df['text'].astype(str).str.strip()
df = df[df['text'] != '']

# Separate positives and negatives
positives = df[df['label'] == 1]
negatives = df[df['label'] == 0]

# Sample
positive_sample = positives.sample(n=35, random_state=42)
negative_sample = negatives.sample(n=15, random_state=42)

# Combine samples
validation_sample = pd.concat([positive_sample, negative_sample], ignore_index=True)

# Shuffle the final dataset
validation_sample = validation_sample.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to CSV
output_path = "data/validation_sample.csv"
validation_sample.to_csv(output_path, index=False)

# Print summary
print(f"Saved balanced sample to {output_path} with {len(validation_sample)} rows.")
print("Label distribution:")
print(validation_sample['label'].value_counts().sort_index().to_string(index=True))

