import pandas as pd
from Levenshtein import distance as lev_distance
from tqdm import tqdm

tqdm.pandas()

# check if ner prediction for location matches the target location
def fuzzy_match(predictions, target, max_distance=2):
    """
    Check if any prediction matches the target with allowed fuzziness.
    """
    preds = [p.strip().lower() for p in str(predictions).split('|') if p.strip()]
    target = str(target).strip().lower()

    return any(lev_distance(pred, target) <= max_distance for pred in preds)

# check if document month in retronews == 'mois' in archives dataset
def match_months(doc_month, mois_field):
    if pd.isna(doc_month) or pd.isna(mois_field):
        return False
    doc_month = doc_month.strip()
    mois_values = str(mois_field).split('-')
    return doc_month in mois_values

def load_and_match(df1_path, df2_path, output_path):
    df1 = pd.read_csv(df1_path)
    df2 = pd.read_csv(df2_path)

    # generate uniqueids for archives dataset
    df2 = df2.copy()
    df2['uniqueid_2'] = ['EVT_{:04d}'.format(i) for i in range(1, len(df2) + 1)]

    # extract month from df1 document_published
    df1['pub_month'] = pd.to_datetime(df1['document_published'], errors='coerce').dt.strftime('%m')

    matches = []

    for idx2, row2 in tqdm(df2.iterrows(), total=len(df2), desc="Matching"):
        target_year = str(row2['date']).strip()
        target_months = str(row2['mois']).zfill(2) if '-' not in str(row2['mois']) else row2['mois']
        localite = row2['localite']

        for idx1, row1 in df1.iterrows():
            if str(row1['year']).strip() != target_year:
                continue

            doc_month = row1['pub_month']
            if not match_months(doc_month, target_months):
                continue

            if not fuzzy_match(row1['prediction'], localite):
                continue

            matches.append({
                'uniqueid_df1': row1['uniqueid'],
                'uniqueid_df2': row2['uniqueid_2'],
                'year': row1['year'],
                'month': doc_month,
                'prediction': row1['prediction'],
                'localite': localite,
                'matched_text': row1['text'],
                'type_hostilite': row2.get('type_hostilite', '')  
            })

    matched_df = pd.DataFrame(matches)
    matched_df.to_csv(output_path, index=False)
    print(f"{len(matched_df)} matches saved to '{output_path}'")

# execution
if __name__ == "__main__":
    load_and_match(
        df1_path="data/camembert_full_ner.csv",
        df2_path="data/archives_preprocessed.csv",
        output_path="data/matched_events.csv"
    )