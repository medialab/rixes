import pandas as pd
import numpy as np
from tqdm import tqdm
from augmentedsocialscientist.models import Camembert
import os
from sklearn.metrics import classification_report

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# Initialize model
bert = Camembert()

# === Load and preprocess test set ===
print("Loading and preprocessing test set...")
test = pd.read_csv('data/annotated_dataset_deduped.csv')

# Drop rows where participants == 'EE'
test = test[test['participants'] != 'EE']

# Set labels from 'relevant' column
test['label'] = test['relevant'].apply(lambda x: 1 if x == 1 else 0)

# Clean function
def clean_text_df(df):
    df = df.dropna(subset=['text', 'label']).copy()
    df['text'] = df['text'].astype(str).str.strip()
    return df[(df['text'] != '') & (df['text'].str.lower() != 'nan')]

test = clean_text_df(test)

# === Encode ===
print("Encoding test data...")
test_loader = bert.encode(
    tqdm(test.text.values, desc="Test texts"),
    test.label.values
)

# === Evaluate ===
print("Evaluating on test set using 'xenophobia' model...")
pred = bert.predict_with_model(test_loader, model_path='./models/xenophobic')
test['pred_label'] = np.argmax(pred, axis=1)
test['pred_proba'] = np.max(pred, axis=1)

# Save predictions
output_path = "data/test_set_rixes.csv"
test.to_csv(output_path, index=False)
print(f"Saved test set predictions to {output_path}")

# Print metrics
print("\nClassification Report:\n", classification_report(test['label'], test['pred_label'], target_names=["non-xeno", "xeno"]))