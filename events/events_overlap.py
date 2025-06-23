import pandas as pd
from tqdm import tqdm

"""
Analyse overlap between events detected manually and with the rixe method
and events detected with a finetuned classifier.
"""

# Load model predictions
pred_df = pd.read_csv("data/predictions_all_years.csv")
pred_positive_ids = set(pred_df[pred_df['pred_label'] == 1]['uniqueid'].astype(str))

print(f"Model predicted {len(pred_positive_ids)} positive unique IDs.")

# Load known annotated events

# archives
print("Loading archives_retronews_shuffled.csv...")
exploded = pd.read_csv("data/archives_retronews_shuffled.csv")
exploded['retronews_uniqueid'] = exploded['retronews_uniqueid'].astype(str)
exploded_ids = set(exploded['retronews_uniqueid'])

# rixes
print("Loading annotated_dataset_deduped.csv...")
deduped = pd.read_csv("data/annotated_dataset_deduped.csv")
deduped['uniqueid'] = deduped['uniqueid'].astype(str)
deduped_ids = set(deduped[deduped['relevant'] == 1]['uniqueid'])

# notes events
print("Loading notes_new_events.csv...")
notes = pd.read_csv("data/notes_new_events.csv")
notes_ids = set()
for val in tqdm(notes['uniqueid'].dropna().astype(str), desc="Processing note IDs"):
    notes_ids.update(val.split('|'))

# Combine all known ids
total_known_ids = exploded_ids | deduped_ids | notes_ids

# Compute overlaps
overlap_exploded = pred_positive_ids & exploded_ids
overlap_deduped = pred_positive_ids & deduped_ids
overlap_notes = pred_positive_ids & notes_ids
total_overlap = pred_positive_ids & total_known_ids

# Compute missed predictions
missed_exploded = exploded_ids - pred_positive_ids
missed_deduped = deduped_ids - pred_positive_ids
missed_notes = notes_ids - pred_positive_ids
total_missed = total_known_ids - pred_positive_ids

# Print summary
print("\nOverlap Summary:")
print(f"- archives: {len(overlap_exploded)}")
print(f"- rixes (where relevant==1): {len(overlap_deduped)}")
print(f"- notes events: {len(overlap_notes)}")
print(f"Total unique overlap across all: {len(total_overlap)}")

print("\nMissed Predictions:")
print(f"- Missed from archives: {len(missed_exploded)}")
print(f"- Missed from rixes: {len(missed_deduped)}")
print(f"- Missed from notes events: {len(missed_notes)}")
print(f"Total missed across all known events: {len(total_missed)}")

# Extract and export missed events with text

print("\nPreparing missed events with text...")

# Standardize columns for merging
exploded_missed = exploded[exploded['retronews_uniqueid'].isin(missed_exploded)].copy()
exploded_missed['uniqueid'] = exploded_missed['retronews_uniqueid']

deduped_missed = deduped[deduped['uniqueid'].isin(missed_deduped)].copy()

# Process notes
notes_rows = []
for idx, row in tqdm(notes.iterrows(), total=len(notes), desc="Filtering missed notes"):
    if pd.isna(row['uniqueid']):
        continue
    for uid in str(row['uniqueid']).split('|'):
        uid = uid.strip()
        if uid in missed_notes:
            notes_rows.append({'uniqueid': uid, 'text': row.get('text', '')})
notes_missed = pd.DataFrame(notes_rows)

# Extract relevant columns
exploded_out = exploded_missed[['uniqueid', 'text']]
deduped_out = deduped_missed[['uniqueid', 'text']]
notes_out = notes_missed[['uniqueid', 'text']]

# Combine all missed examples
missed_texts_df = pd.concat([exploded_out, deduped_out, notes_out], ignore_index=True)
missed_texts_df = missed_texts_df.drop_duplicates(subset='uniqueid').reset_index(drop=True)

# Save to CSV
missed_texts_df.to_csv("data/missed_events_with_text.csv", index=False)
print(f"Saved missed events with text to: data/missed_events_with_text.csv ({len(missed_texts_df)} entries)")


