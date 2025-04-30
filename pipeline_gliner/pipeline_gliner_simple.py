import pandas as pd
import Levenshtein as lev
from gliner import GLiNER
from transformers import AutoTokenizer
from sklearn.metrics import precision_score, recall_score
from tqdm import tqdm

# script for NER without anchoring around rixe and bagarre, to get all of the ville and region options

# GLiNER and tokenizer
model = GLiNER.from_pretrained("urchade/gliner_multi")
tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")

MAX_TOKENS = 384

# chunking
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

# predict ville and region
def find_location_entities(text, label):
    chunks = chunk_text(text)
    all_location_entities = []

    for chunk in chunks:
        try:
            entities = model.predict_entities(chunk, labels=[label])
            all_location_entities.extend([e['text'] for e in entities if e['label'] == label])
        except Exception as e:
            print(f"Error ({label}): {e}")
    
    return all_location_entities

# check character matching (with a tolerable error rate of 3 characters)
def is_approx_match(gt, pred_str, max_distance=3):
    gt = str(gt).strip().lower()
    preds = [p.strip().lower() for p in str(pred_str).split('|') if p.strip()]

    if not gt and not preds:
        return 1  # rien à prédire et rien de prédit → correct

    for pred in preds:
        if lev.distance(gt, pred) <= max_distance:
            return 1  # au moins un match approx → correct

    return 0  # aucun match approx


# csv file
def process_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    tqdm.pandas()

    df['event_ville'] = df['event_ville'].fillna('')
    df['event_region'] = df['event_region'].fillna('')
    df['text'] = df['text'].fillna('')

    # predictions
    df['prediction_ville'] = df['text'].progress_apply(lambda x: '|'.join(find_location_entities(x, 'city')))
    df['prediction_region'] = df['text'].progress_apply(lambda x: '|'.join(find_location_entities(x, 'region')))

    # predictions vs ground truth
    df['exmatch_ville'] = df.apply(lambda row: is_approx_match(row['event_ville'], row['prediction_ville']), axis=1)
    df['exmatch_region'] = df.apply(lambda row: is_approx_match(row['event_region'], row['prediction_region']), axis=1)


    df_final = df[['uniqueid', 'text', 'event_ville', 'event_region', 'prediction_ville', 'prediction_region', 'exmatch_ville', 'exmatch_region']]

    df_final = df_final.rename(columns={
        'event_ville': 'gt_ville',
        'event_region': 'gt_region'
    })

    df_final.to_csv(output_csv, index=False)
    print(f"Résultats sauvegardés dans '{output_csv}'")

# execution
if __name__ == "__main__":
    input_csv = "data/annotated_dataset_deduped.csv"  
    output_csv = "data/gliner_all_locations.csv"      
    process_csv(input_csv, output_csv)

    df_final = pd.read_csv(output_csv)

    y_true_ville = df_final['gt_ville']
    y_pred_ville = df_final['prediction_ville']

    y_true_ville_match = df_final.apply(lambda row: is_approx_match(row['gt_ville'], row['prediction_ville']), axis=1)
    precision_ville = precision_score(y_true_ville_match, [1] * len(y_true_ville_match), zero_division=0)
    recall_ville = recall_score(y_true_ville_match, [1] * len(y_true_ville_match), zero_division=0)


    y_true_region = df_final['gt_region']
    y_pred_region = df_final['prediction_region']

    y_true_region_match = df_final.apply(lambda row: is_approx_match(row['gt_region'], row['prediction_region']), axis=1)
    precision_region = precision_score(y_true_region_match, [1] * len(y_true_region_match), zero_division=0)
    recall_region = recall_score(y_true_region_match, [1] * len(y_true_region_match), zero_division=0)

    print("\n=== Évaluation des performances GLiNER ===")

    print("\n==== VILLE ====")
    print(f"Précision : {precision_ville:.2f}")
    print(f"Rappel    : {recall_ville:.2f}")

    print("\n==== RÉGION ====")
    print(f"Précision : {precision_region:.2f}")
    print(f"Rappel    : {recall_region:.2f}")
