import pandas as pd
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from sklearn.metrics import precision_score, recall_score
from tqdm import tqdm
import Levenshtein as lev

# model
model_name = "Jean-Baptiste/camembert-ner"
model = AutoModelForTokenClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

MAX_TOKENS = 500
tqdm.pandas()

def chunk_text(text, max_tokens=MAX_TOKENS):
    tokens = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False, truncation=False)
    input_ids = tokens["input_ids"]
    chunks = []
    for start in range(0, len(input_ids), max_tokens):
        end = min(start + max_tokens, len(input_ids))
        chunk_ids = input_ids[start:end]
        chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        chunks.append(chunk_text)
    return chunks

# extraction LOC
def extract_all_locations(text):
    chunks = chunk_text(text)
    location_entities = []
    for chunk in chunks:
        try:
            entities = ner_pipeline(chunk)
            location_entities.extend([
                e['word'].strip() for e in entities if e['entity_group'] == 'LOC'
            ])
        except Exception as e:
            print(f"Erreur NER : {e}")
    
    clean_locs = list(dict.fromkeys(location_entities))
    return "|".join(clean_locs)

# fuzzy matching on one of the gt columns
def match_one(gt, predictions, max_distance=3):
    if not isinstance(gt, str) or not isinstance(predictions, str):
        return 0
    gt = gt.strip().lower()
    preds = [p.strip().lower() for p in predictions.split("|") if p.strip()]
    for p in preds:
        if lev.distance(gt, p) <= max_distance:
            return 1
    return 0

# combined matching : town OR region
def combined_match(row):
    return int(
        match_one(row['gt_ville'], row['prediction']) or
        match_one(row['gt_region'], row['prediction'])
    )

def process_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    df['event_ville'] = df['event_ville'].fillna('')
    df['event_region'] = df['event_region'].fillna('')
    df['text'] = df['text'].fillna('')

    df = df.rename(columns={'event_ville': 'gt_ville', 'event_region': 'gt_region'})

    print("→ Extraction des entités LOCATION...")
    df['prediction'] = df['text'].progress_apply(extract_all_locations)

    print("→ Comparaison vérité terrain...")
    df['exact_match'] = df.apply(combined_match, axis=1)

    df_final = df[['uniqueid', 'text', 'gt_ville', 'gt_region', 'prediction', 'exact_match']]
    df_final.to_csv(output_csv, index=False)
    print(f"✔ Résultats sauvegardés dans '{output_csv}'")
    return df_final

# evaluation
def evaluate(df_final):
    print("\n=== ÉVALUATION GLOBALE ===")
    y_true = df_final['exact_match']
    y_pred = [1] * len(y_true)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    print(f"Précision : {precision:.2f}")
    print(f"Rappel    : {recall:.2f}")

# execution
if __name__ == "__main__":
    input_csv = "data/annotated_dataset_deduped.csv"
    output_csv = "data/camembert_combined_eval.csv"
    df_final = process_csv(input_csv, output_csv)
    evaluate(df_final)