import pandas as pd
from gliner import GLiNER

# gliner multilingual model
model = GLiNER.from_pretrained("urchade/gliner_multi_pii-v1")

# annotated dataset
df_annotated = pd.read_csv('/home/lilla/retronews/annotated_dataset_deduped.csv')

# full dataset (sample pour test)
df_full = pd.read_csv('/home/lilla/retronews/sample_fulldataset.csv')

# location label
labels = ["location"]

# extract town/city and region
def extract_city_and_region(text):
    # detect location types
    entities = model.predict_entities(text, labels)
    city = None
    region = None

    for entity in entities:
        if entity["label"] == "location":
            city = entity["text"]
            region = entity["text"]
    
    return city, region

# apply function
df_full['event_ville'], df_full['event_region'] = zip(*df_full['text'].apply(extract_city_and_region))

# output file
df_full.to_csv('gliner_full_dataset.csv', index=False)

