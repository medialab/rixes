import pandas as pd
from gliner import GLiNER
from transformers import AutoTokenizer

# Load model + base tokenizer (GLiNER is built on xlm-roberta-base)
model = GLiNER.from_pretrained("urchade/gliner_multi")
tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")

# Constants
MAX_TOKENS = 510
OVERLAP = 60

def tokenize_to_chunks(text, max_tokens=MAX_TOKENS, overlap=OVERLAP):
    tokens = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False, truncation=False)
    input_ids = tokens["input_ids"]
    offsets = tokens["offset_mapping"]
    
    chunks = []
    start = 0
    
    while start < len(input_ids):
        end = min(start + max_tokens, len(input_ids))
        chunk_ids = input_ids[start:end]
        chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        chunks.append(chunk_text)

        if end == len(input_ids):
            break
        start += max_tokens - overlap
    
    return chunks

# function to find the recognizable location closest to the words 'rixe' or 'bagarre'
def find_closest_location(text):
    target_words = ['rixe', 'bagarre']
    chunks = tokenize_to_chunks(text)

    all_location_entities = []

    for chunk in chunks:
        try:
            entities = model.predict_entities(chunk, labels=['LOC'])
            all_location_entities.extend([e for e in entities if e['label'] == 'LOC'])
        except Exception as e:
            print(f"Error in GLiNER prediction: {e}")

    if all_location_entities:
        words = text.split()
        target_positions = [i for i, word in enumerate(words) if word.lower() in target_words]

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

            return closest_location if closest_location else "No location found"

    return "No location found"

def process_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    df['closest_location'] = df['text'].apply(find_closest_location)
    df.to_csv(output_csv, index=False)
    print(f"Saved to {output_csv}")

# execution
process_csv('data/sample_for_bert.csv', 'data/sample_with_closest_location_gliner.csv')