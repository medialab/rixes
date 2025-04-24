import pandas as pd
from gliner import GLiNER
import re
from transformers import AutoTokenizer

# models
model = GLiNER.from_pretrained("urchade/gliner_multi")
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

# datasets
df_annotated = pd.read_csv('/home/lilla/retronews/annotated_dataset_deduped.csv')
df_full = pd.read_csv('/home/lilla/retronews/sample_fulldataset.csv')

# labels
labels = ["commune","région"]

# functions

def split_text_into_sentences(text):
    sentences = re.split(r'(?<=[.])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def split_text(text, max_tokens=384):
    sentences = split_text_into_sentences(text)
    #words = text.split()
    chunks = []
    current_chunk = []

    for sentence in sentences:
        tentative = current_chunk + " " + sentence if current_chunk else sentence
        tokenized = tokenizer(tentative, truncation=False, add_special_tokens=False)
        if len(tokenized["input_ids"]) <= max_tokens:
            current_chunk = tentative
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
# extract commune and region from chunks
def extract_city_and_region(text):
    city = None
    region = None
    chunks = split_text(text)

    for chunk in chunks:
        entities = model.predict_entities(chunk, labels)
        for entity in entities:
            if entity["label"] == "commune" and city is None:
                city = entity["text"]
            elif entity["label"] == "région" and region is None:
                region = entity["text"]

    return city, region

# apply function
df_full['event_ville'], df_full['event_region'] = zip(*df_full['text'].apply(extract_city_and_region))

# output file
df_full.to_csv('gliner_test_5.csv', index=False)

