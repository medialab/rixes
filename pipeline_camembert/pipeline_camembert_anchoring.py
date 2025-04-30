import pandas as pd
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from sklearn.metrics import precision_score, recall_score
from tqdm import tqdm
import Levenshtein as lev

# camembert model
model_name = "Jean-Baptiste/camembert-ner"
model = AutoModelForTokenClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

MAX_TOKENS = 500
TARGET_WORDS = ['rixe', 'bagarre']


tqdm.pandas()

def anchor_chunks(text, targets=TARGET_WORDS, max_tokens=MAX_TOKENS):
    words = text.split()
    target_indices = [i for i, w in enumerate(words) if w.lower() in targets]
    chunks = []

    if not target_indices:
        tokens = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False, truncation=False)
        input_ids = tokens["input_ids"]
        for start in range(0, len(input_ids), max_tokens):
            end = min(start + max_tokens, len(input_ids))
            chunk_ids = input_ids[start:end]
            chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
            chunks.append(chunk_text)
        return chunks

    for idx in target_indices:
        start = max(0, idx - (max_tokens // 2))
        end = min(len(words), idx + (max_tokens // 2))
        chunk = " ".join(words[start:end])
        while len(tokenizer(chunk)['input_ids']) > max_tokens and (end - start) > 1:
            start += 1
            end -= 1
            chunk = " ".join(words[start:end])
        chunks.append(chunk)

    return chunks

def find_closest_entity(text, label="LOC"):
    chunks = anchor_chunks(text)
    all_entities = []

    for chunk in chunks:
        try:
            entities = ner_pipeline(chunk)
            all_entities.extend([e for e in entities if e['entity_group'] == label])
        except Exception as e:
            print(f"Erreur NER : {e}")

    if all_entities:
        words = text.split()
        target_positions = [i for i, word in enumerate(words) if word.lower() in TARGET_WORDS]
        if target_positions:
            closest_entity = None
            min_distance = float('inf')
            for entity in all_entities:
                loc_start = text.find(entity['word'])
                for pos in target_positions:
                    keyword_start = text.find(words[pos])
                    distance = abs(keyword_start - loc_start)
                    if distance < min_distance:
                        min_distance = distance
                        closest_entity = entity['word']
            return closest_entity if closest_entity else ""
    return ""

def is_approx_match(gt, pred, max_distance=3):
    gt = str(gt).strip().lower() if isinstance(gt, str) else ""
    pred = str(pred).strip().lower() if isinstance(pred, str) else ""
    if not gt and not pred:
        return 1
    return 1 if lev.distance(gt, pred) <= max_distance else 0

def process_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    df['event_ville'] = df['event_ville'].fillna('')
    df['event_region'] = df['event_region'].fillna('')
    df['text'] = df['text'].fillna('')

    print("→ Prédiction des villes...")
    df['prediction_ville'] = df['text'].progress_apply(lambda t: find_closest_entity(t, label="LOC"))

    print("→ Prédiction des régions...")
    df['prediction_region'] = df['text'].progress_apply(lambda t: find_closest_entity(t, label="LOC"))  # CamemBERT n'a pas de REGION → LOC pour les deux

    df['exmatch_ville'] = df.apply(lambda row: is_approx_match(row['event_ville'], row['prediction_ville']), axis=1)
    df['exmatch_region'] = df.apply(lambda row: is_approx_match(row['event_region'], row['prediction_region']), axis=1)

    df_final = df[['uniqueid', 'text', 'event_ville', 'event_region', 'prediction_ville', 'prediction_region', 'exmatch_ville', 'exmatch_region']]
    df_final = df_final.rename(columns={'event_ville': 'gt_ville', 'event_region': 'gt_region'})
    df_final.to_csv(output_csv, index=False)
    print(f"✔ Résultats sauvegardés dans '{output_csv}'")

    return df_final

# metrics
def evaluate(df_final):

    # ville
    y_true_ville = df_final['exmatch_ville']
    y_pred_ville = [1] * len(y_true_ville)
    precision_ville = precision_score(y_true_ville, y_pred_ville, zero_division=0)
    recall_ville = recall_score(y_true_ville, y_pred_ville, zero_division=0)

    # region
    y_true_region = df_final['exmatch_region']
    y_pred_region = [1] * len(y_true_region)
    precision_region = precision_score(y_true_region, y_pred_region, zero_division=0)
    recall_region = recall_score(y_true_region, y_pred_region, zero_division=0)

    print("\n=== Évaluation des performances GLiNER ===")
    print("==== VILLE ====")
    print(f"Précision : {precision_ville:.2f}")
    print(f"Rappel    : {recall_ville:.2f}")
    print("==== REGION ====")
    print(f"Précision : {precision_region:.2f}")
    print(f"Rappel    : {recall_region:.2f}")

if __name__ == "__main__":
    input_csv = "data/annotated_dataset_deduped.csv"
    output_csv = "data/camembert_again.csv"
    df_final = process_csv(input_csv, output_csv)
    evaluate(df_final)