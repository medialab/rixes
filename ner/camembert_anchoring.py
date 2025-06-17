import pandas as pd
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from sklearn.metrics import precision_score, recall_score
from tqdm import tqdm
import Levenshtein as lev

"""
NER pipeline (with evaluation) to detect locations with semantic anchoring around keywords 'rixe' and 'bagarre'.
"""

# camember-ner model 
model_name = "Jean-Baptiste/camembert-ner"
model = AutoModelForTokenClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

MAX_TOKENS = 500
TARGET_WORDS = ['rixe', 'bagarre'] # anchor words
tqdm.pandas()

# chunking around anchor words
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

# extraction of LOC entities around anchor words
def extract_anchor_locations(text):
    chunks = anchor_chunks(text)
    all_entities = []

    for chunk in chunks:
        try:
            entities = ner_pipeline(chunk)
            all_entities.extend([e['word'].strip() for e in entities if e['entity_group'] == 'LOC'])
        except Exception as e:
            print(f"NER Error: {e}")

    clean_entities = list(dict.fromkeys(all_entities))  # delete duplicates
    return "|".join(clean_entities)

# fuzzy matching ville or region
def match_one(gt, predictions, max_distance=3):
    if not isinstance(gt, str) or not isinstance(predictions, str):
        return 0
    gt = gt.strip().lower()
    preds = [p.strip().lower() for p in predictions.split("|") if p.strip()]
    for p in preds:
        if lev.distance(gt, p) <= max_distance:
            return 1
    return 0

# combined matching ville or region
def combined_match(row):
    return int(
        match_one(row['gt_ville'], row['prediction']) or
        match_one(row['gt_region'], row['prediction'])
    )

# process csv
def process_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    df['event_ville'] = df['event_ville'].fillna('')
    df['event_region'] = df['event_region'].fillna('')
    df['text'] = df['text'].fillna('')
    df = df.rename(columns={'event_ville': 'gt_ville', 'event_region': 'gt_region'})

    print("→ Extraction NER autour des ancres (rixe/bagarre)...")
    df['prediction'] = df['text'].progress_apply(extract_anchor_locations)

    print("Evaluation of matches")
    df['exact_match'] = df.apply(combined_match, axis=1)

    df_final = df[['uniqueid', 'text', 'gt_ville', 'gt_region', 'prediction', 'exact_match']]
    df_final.to_csv(output_csv, index=False)
    print(f"Results saved to'{output_csv}'")
    return df_final

# evaluation
def evaluate(df_final):
    print("Evaluation")
    y_true = df_final['exact_match']
    y_pred = [1] * len(y_true)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    print(f"precision : {precision:.2f}")
    print(f"recall : {recall:.2f}")

# execution
if __name__ == "__main__":
    input_csv = "data/annotated_dataset_deduped.csv"
    output_csv = "data/camembert_anchor_eval.csv"
    df_final = process_csv(input_csv, output_csv)
    evaluate(df_final)