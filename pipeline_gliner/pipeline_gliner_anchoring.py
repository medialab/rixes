import pandas as pd
import Levenshtein as lev
from gliner import GLiNER
from transformers import AutoTokenizer
from sklearn.metrics import precision_score, recall_score
from tqdm import tqdm

# GLiNER and tokenizer
model = GLiNER.from_pretrained("urchade/gliner_multi")
tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")

MAX_TOKENS = 384
TARGET_WORDS = ['rixe', 'bagarre']
tqdm.pandas() 

# Function to create chunks around target words rixe and bagarre
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

# Function to predict the closest city
def find_closest_city(text):
    chunks = anchor_chunks(text)
    all_location_entities = []

    for chunk in chunks:
        try:
            entities = model.predict_entities(chunk, labels=['city'])
            all_location_entities.extend([e for e in entities if e['label'] == 'city'])
        except Exception as e:
            print(f"Erreur de prédiction GLiNER (city): {e}")

    if all_location_entities:
        words = text.split()
        target_positions = [i for i, word in enumerate(words) if word.lower() in TARGET_WORDS]

        if target_positions:
            closest_location = None
            min_distance = float('inf')

            for entity in all_location_entities:
                loc_start = text.find(entity['text'])
                loc_end = loc_start + len(entity['text'])

                for pos in target_positions:
                    keyword = words[pos]
                    keyword_start = text.find(keyword)
                    keyword_end = keyword_start + len(keyword)

                    distance = min(abs(keyword_start - loc_start), abs(keyword_end - loc_end))
                    if distance < min_distance:
                        min_distance = distance
                        closest_location = entity['text']

            return closest_location if closest_location else ""

    return ""

# Function to predict closest region
def find_closest_region(text):
    chunks = anchor_chunks(text)
    all_location_entities = []

    for chunk in chunks:
        try:
            entities = model.predict_entities(chunk, labels=['region'])
            all_location_entities.extend([e for e in entities if e['label'] == 'region'])
        except Exception as e:
            print(f"Erreur de prédiction GLiNER (region): {e}")

    if all_location_entities:
        words = text.split()
        target_positions = [i for i, word in enumerate(words) if word.lower() in TARGET_WORDS]

        if target_positions:
            closest_location = None
            min_distance = float('inf')

            for entity in all_location_entities:
                loc_start = text.find(entity['text'])
                loc_end = loc_start + len(entity['text'])

                for pos in target_positions:
                    keyword = words[pos]
                    keyword_start = text.find(keyword)
                    keyword_end = keyword_start + len(keyword)

                    distance = min(abs(keyword_start - loc_start), abs(keyword_end - loc_end))
                    if distance < min_distance:
                        min_distance = distance
                        closest_location = entity['text']

            return closest_location if closest_location else ""

    return ""

# Function to check if two strings match with tolerance (max 3 characters of difference)
def is_approx_match(gt, pred, max_distance=3):
    gt = gt.strip().lower()
    pred = pred.strip().lower()
    if not gt and not pred:
        return 1
    distance = lev.distance(gt, pred)
    return 1 if distance <= max_distance else 0

# Function to process csv files
def process_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    df['event_ville'] = df['event_ville'].fillna('')
    df['event_region'] = df['event_region'].fillna('')
    df['text'] = df['text'].fillna('')

    df['prediction_ville'] = df['text'].progress_apply(find_closest_city)
    df['prediction_region'] = df['text'].progress_apply(find_closest_region)

    df['prediction_ville'] = df['prediction_ville'].fillna('')
    df['prediction_region'] = df['prediction_region'].fillna('')

    df['levenshtein_ville'] = df.apply(lambda row: lev.distance(str(row['event_ville']), str(row['prediction_ville'])), axis=1)
    df['levenshtein_region'] = df.apply(lambda row: lev.distance(str(row['event_region']), str(row['prediction_region'])), axis=1)

    # Modified here: exact match if distance <= 3
    df['exmatch_ville'] = df.apply(lambda row: is_approx_match(row['event_ville'], row['prediction_ville']), axis=1)
    df['exmatch_region'] = df.apply(lambda row: is_approx_match(row['event_region'], row['prediction_region']), axis=1)

    df_final = df[['uniqueid', 'text', 'event_ville', 'event_region', 'prediction_ville', 'prediction_region',
                   'levenshtein_ville', 'levenshtein_region', 'exmatch_ville', 'exmatch_region']]

    df_final = df_final.rename(columns={
        'event_ville': 'gt_ville',
        'event_region': 'gt_region'
    })

    df_final.to_csv(output_csv, index=False)
    print(f"Résultats sauvegardés dans '{output_csv}'")

    return df_final

if __name__ == "__main__":
    input_csv = "data/annotated_dataset_deduped.csv"  
    output_csv = "data/gliner_results_notstrict.csv"      
    df_final = process_csv(input_csv, output_csv)

    # === Evaluate precision and recall ===
    print("\n=== Évaluation des performances GLiNER ===")

    y_true_ville_match = df_final['exmatch_ville']
    y_true_region_match = df_final['exmatch_region']

    precision_ville = precision_score(y_true_ville_match, [1]*len(y_true_ville_match), zero_division=0)
    recall_ville = recall_score(y_true_ville_match, [1]*len(y_true_ville_match), zero_division=0)

    precision_region = precision_score(y_true_region_match, [1]*len(y_true_region_match), zero_division=0)
    recall_region = recall_score(y_true_region_match, [1]*len(y_true_region_match), zero_division=0)

    print("\n==== VILLE ====")
    print(f"Précision : {precision_ville:.2f}")
    print(f"Rappel    : {recall_ville:.2f}")

    print("\n==== RÉGION ====")
    print(f"Précision : {precision_region:.2f}")
    print(f"Rappel    : {recall_region:.2f}")
