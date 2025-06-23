import pandas as pd
import numpy as np
import glob
import os
from tqdm import tqdm
from augmentedsocialscientist.models import Camembert

"""
Predict on OCRed unnannotated dataset using finetuned model.
"""

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

bert = Camembert(model_name="./models/retronews")

# Load data
prediction_files = glob.glob('/store/retronews/etrangers/*.csv')
print(f"Loading {len(prediction_files)} CSV files for prediction...")

frames = []
for file in tqdm(prediction_files, desc="Loading files"):
    df = pd.read_csv(file)
    df['source_file'] = os.path.basename(file)
    frames.append(df)

prediction_data = pd.concat(frames, ignore_index=True)

# Drop rows without text
prediction_data = prediction_data.dropna(subset=['text']).copy()

# Clean data
prediction_data['text'] = prediction_data['text'].astype(str).str.strip()

# Remove entries that became empty or were 'nan' strings
prediction_data = prediction_data[
    (prediction_data['text'] != '') & 
    (prediction_data['text'].str.lower() != 'nan')
]
texts = prediction_data.text.values

# Encode text
print("Encoding prediction texts...")
pred_loader = bert.encode(list(tqdm(texts, desc="Encoding")), labels=None)

# Predict
print("Running predictions...")
pred = bert.predict_with_model(
    pred_loader,
    model_path='./models/retronews'
)

# Attach predictions to dataframe
prediction_data['pred_label'] = np.argmax(pred, axis=1)
prediction_data['pred_proba'] = np.max(pred, axis=1)

# Save predictions
prediction_data.to_csv('data/predictions_all_years.csv', index=False)
print("Predictions saved to data/predictions_all_years.csv")