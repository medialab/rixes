
import pandas as pd
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from tqdm import tqdm
import Levenshtein as lev

"""
NER pipeline to extract locations from articles.
"""

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
            print(f"NER error : {e}")
    
    clean_locs = list(dict.fromkeys(location_entities))
    return "|".join(clean_locs)

def process_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    df['text'] = df['text'].fillna('')

    print("Extraction of LOC entities")
    df['prediction'] = df['text'].progress_apply(extract_all_locations)

    df_final = df[['text','year','uniqueid', 'patterns', 'publication_title','published','document_publication_title','document_published','document_publication_region', 'document_histo_period', 'prediction']]
    df_final.to_csv(output_csv, index=False)
    print(f"Results saved to '{output_csv}'")
    return df_final

# execution 
if __name__ == "__main__":
    input_csv = "data/full.csv"
    output_csv = "data/camembert_full_ner.csv"
    df_final = process_csv(input_csv, output_csv)