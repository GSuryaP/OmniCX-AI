from pathlib import Path

import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report
)

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.linear_model import (
    LogisticRegression
)

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    BASE_DIR /
    "data/processed/merged_reviews.csv"
)

X = df["review_comment_message"]
y = df["sentiment"]

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )
)

pipeline = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            max_features=20000,
            ngram_range=(1,3),
            min_df=2
        )
    ),
    (
        "model",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced"
        )
    )
])

pipeline.fit(
    X_train,
    y_train
)

preds = pipeline.predict(
    X_test
)

print(
    "\nAccuracy:",
    accuracy_score(
        y_test,
        preds
    )
)

print(
    classification_report(
        y_test,
        preds
    )
)

MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

joblib.dump(
    pipeline,
    MODEL_DIR /
    "sentiment_model.pkl"
)

print("Model saved")