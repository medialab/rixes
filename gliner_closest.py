import pandas as pd
from gliner import GLiNER
from transformers import AutoTokenizer

# Load model + base tokenizer (GLiNER is built on xlm-roberta-base)
model = GLiNER.from_pretrained("urchade/gliner_multi")
tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")

# Constants
MAX_TOKENS = 384
TARGET_WORDS = ['rixe', 'bagarre']

# Function for chunking around anchor words
def anchor_chunks(text, targets=TARGET_WORDS, max_tokens=MAX_TOKENS):
    words = text.split()
    target_indices = [i for i, w in enumerate(words) if w.lower() in targets]
    chunks = []
    
    # If no target words found, we still split the text into chunks of max length
    if not target_indices:
        tokens = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False, truncation=False)
        input_ids = tokens["input_ids"]
        for start in range(0, len(input_ids), max_tokens):
            end = min(start + max_tokens, len(input_ids))
            chunk_ids = input_ids[start:end]
            chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
            chunks.append(chunk_text)
        return chunks
    
    # Create chunks centered around target words
    for idx in target_indices:
        # Define a window centered around the target index
        start = max(0, idx - (max_tokens // 2))
        end = min(len(words), idx + (max_tokens // 2))
        
        # Create a chunk around the target word
        chunk = " ".join(words[start:end])
        
        # Ensure chunk does not exceed token limit
        while len(tokenizer(chunk)['input_ids']) > max_tokens and (end - start) > 1:
            start += 1
            end -= 1
            chunk = " ".join(words[start:end])

        chunks.append(chunk)

    return chunks

# Function to find the closest city entity to 'rixe' or 'bagarre'
def find_closest_city(text):
    chunks = anchor_chunks(text)

    all_location_entities = []

    for chunk in chunks:
        try:
            entities = model.predict_entities(chunk, labels=['city'])
            all_location_entities.extend([e for e in entities if e['label'] == 'city'])
        except Exception as e:
            print(f"Error in GLiNER prediction: {e}")

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

# Function to find the closest region entity to 'rixe' or 'bagarre'
def find_closest_region(text):
    chunks = anchor_chunks(text)

    all_location_entities = []

    for chunk in chunks:
        try:
            entities = model.predict_entities(chunk, labels=['region'])
            all_location_entities.extend([e for e in entities if e['label'] == 'region'])
        except Exception as e:
            print(f"Error in GLiNER prediction: {e}")

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

# Function to process the CSV file
def process_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    df['closest_city'] = df['text'].apply(find_closest_city)
    df['closest_region'] = df['text'].apply(find_closest_region)
    df.to_csv(output_csv, index=False)
    print(f"Saved to {output_csv}")

# Run the CSV processing
process_csv('data/annotated_dataset_deduped.csv', 'data/gliner_anchor.csv')
