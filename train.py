# train.py
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

DATA_PATH = os.environ.get("DATA_PATH", "data/UNSW_2018_IoT_Botnet_Final_10_B.csv")
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")

def load_data(path=DATA_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found. Ensure DATA_URL secret or local file.")
    # semicolon separated
    df = pd.read_csv(path, sep=';', low_memory=False)
    return df

def preprocess(df):
    # Drop IP address columns (strings, high-cardinality)
    drop_cols = ['saddr', 'daddr', 'category', 'subcategory']
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors='ignore')

    # Ensure attack column exists
    if 'attack' not in df.columns:
        raise KeyError("label column 'attack' not found in CSV")

    # Convert attack to integer label (if string)
    y = df['attack'].astype(int)

    # Columns to use as features
    # We'll keep 'proto' encoded, numeric ports, and listed numeric features
    candidate_features = [
        'proto', 'sport', 'dport', 'seq', 'stddev', 'N_IN_Conn_P_SrcIP',
        'min', 'state_number', 'mean', 'N_IN_Conn_P_DstIP', 'drate', 'srate', 'max'
    ]
    features = [c for c in candidate_features if c in df.columns]
    X = df[features].copy()

    # Fill missing numeric values
    for col in X.select_dtypes(include=[np.number]).columns:
        X[col] = X[col].fillna(0)

    # Encode 'proto' (if present)
    encoders = {}
    if 'proto' in X.columns:
        le = LabelEncoder()
        X['proto'] = X['proto'].astype(str).fillna('NA')
        X['proto'] = le.fit_transform(X['proto'])
        encoders['proto'] = le

    return X, y, encoders

def train_and_save():
    print("Loading data...")
    df = load_data()
    X, y, encoders = preprocess(df)
    print(f"Features: {X.columns.tolist()}; shape={X.shape}; labels={y.shape}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y if len(y.unique())>1 else None
    )

    clf = RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=42)
    print("Training RandomForest...")
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, preds))
    print("Classification report:")
    print(classification_report(y_test, preds))

    os.makedirs(MODEL_DIR, exist_ok=True)
    # Save both model and encoders
    joblib.dump({'model': clf, 'encoders': encoders, 'features': X.columns.tolist()}, MODEL_PATH)
    print(f"Saved model bundle to {MODEL_PATH}")

if __name__ == "__main__":
    train_and_save()
