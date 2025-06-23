import pandas as pd
import numpy as np
import glob
import os
from tqdm import tqdm
from augmentedsocialscientist.models import Camembert

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# Instantiate the classifier
bert = Camembert(model_name="ccdv/lsg-camembert-base-4096")

# Load training and test data
train = pd.read_csv('data/train_1to3.csv')
test = pd.read_csv('data/test_1to4.csv')
validation = pd.read_csv('data/validation.csv')


# Clean training data 
train = train.dropna(subset=['text', 'label']).copy()
train['text'] = train['text'].astype(str).str.strip()
train = train[(train['text'] != '') & (train['text'].str.lower() != 'nan')]

# Clean test data
test = test.dropna(subset=['text', 'label']).copy()
test['text'] = test['text'].astype(str).str.strip()
test = test[(test['text'] != '') & (test['text'].str.lower() != 'nan')]

# Encode training and test sets
print("Encoding training data...")
train_loader = bert.encode(train.text.values, train.label.values)

print("Encoding test data...")
test_loader = bert.encode(test.text.values, test.label.values)

# Train and save the model
print("Training the model...")
scores = bert.run_training(
    train_loader,
    test_loader,
    lr=5e-5,
    n_epochs=5,
    random_state=42,
    save_model_as='retronews'
)


# Validation
print("Encoding validation set...")
val_loader = bert.encode(validation.text.values, validation.label.values)

print("Running predictions on validation set...")
val_pred = bert.predict_with_model(val_loader, model_path='./models/retronews')

# Attach predictions
validation['pred_label'] = np.argmax(val_pred, axis=1)
validation['pred_proba'] = np.max(val_pred, axis=1)
