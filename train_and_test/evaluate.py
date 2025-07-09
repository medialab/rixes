import pandas as pd
import numpy as np
from tqdm import tqdm
from augmentedsocialscientist.models import Camembert
import os
from sklearn.metrics import classification_report, confusion_matrix

# use only one gpu
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# model
bert = Camembert(model_name="almanach/camembert-large")

# Load and clean train/test
train = pd.read_csv('data/train_1to3.csv')
test = pd.read_csv('data/test_1to4.csv')

# Clean text
def clean_text_df(df):
    df = df.dropna(subset=['text', 'label']).copy()
    df['text'] = df['text'].astype(str).str.strip()
    return df[(df['text'] != '') & (df['text'].str.lower() != 'nan')]

train = clean_text_df(train)
test = clean_text_df(test)

# Encode
print("Encoding training data...")
train_loader = bert.encode(
    tqdm(train.text.values, desc="Train texts"),
    train.label.values
)

print("Encoding test data...")
test_loader = bert.encode(
    tqdm(test.text.values, desc="Test texts"),
    test.label.values
)

# Train
print("Training...")
bert.run_training(
    train_loader,
    test_loader,
    lr=5e-5,
    n_epochs=5,
    random_state=42,
    save_model_as='xenophobic'
)

# Evaluate
print("Evaluating on test set...")
pred = bert.predict_with_model(test_loader, model_path='./models/xenophobic')
test['pred_label'] = np.argmax(pred, axis=1)
test['pred_proba'] = np.max(pred, axis=1)

# Save predictions
output_path = "data/test_set_predictions.csv"
test.to_csv(output_path, index=False)
print(f"Saved test set predictions to {output_path}")

# Print metrics
print("\nClassification Report:\n", classification_report(test['label'], test['pred_label'], target_names=["non-xeno", "xeno"]))
print("Confusion Matrix:\n", confusion_matrix(test['label'], test['pred_label']))

# Append summary to csv
from datetime import datetime
import csv

def save_evaluation_results(
    output_path,
    model,
    epochs,
    training_data,
    precision_xeno,
    recall_xeno,
    f1_xeno,
    precision_notxeno,
    recall_notxeno,
    f1_notxeno,
    model_saved,
):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = {
        "model": model,
        "n_epochs": n_epochs,
        "training_data": os.path.basename(training_data) if training_data else "",
        "precision_xeno": precision_xeno,
        "recall_xeno": recall_xeno,
        "f1_xeno": f1_xeno,
        "precision_notxeno": precision_notxeno,
        "recall_notxeno": recall_notxeno,
        "f1_notxeno": f1_notxeno,
        "model_saved": model_saved,
        "timestamp": timestamp
    }

    write_header = not os.path.exists(output_path)
    with open(output_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(row)

# Get metrics from classification report
report_dict = classification_report(test['label'], test['pred_label'], target_names=["non-xeno", "xeno"], output_dict=True)

# Save to CSV
save_evaluation_results(
    output_path="data/evaluation_results.csv",
    model=bert.model_name,
    epochs=5,
    training_data="data/train_1to3.csv",
    precision_xeno=report_dict["xeno"]["precision"],
    recall_xeno=report_dict["xeno"]["recall"],
    f1_xeno=report_dict["xeno"]["f1-score"],
    precision_notxeno=report_dict["non-xeno"]["precision"],
    recall_notxeno=report_dict["non-xeno"]["recall"],
    f1_notxeno=report_dict["non-xeno"]["f1-score"],
    model_saved="./models/xenophobic",
)
print("Evaluation results saved to evaluation_results.csv")
