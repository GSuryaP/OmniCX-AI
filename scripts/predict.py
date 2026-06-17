from pathlib import Path

import joblib

BASE_DIR = Path(__file__).resolve().parent.parent

model = joblib.load(
    BASE_DIR /
    "models/sentiment_model.pkl"
)

while True:

    text = input(
        "\nReview: "
    )

    pred = model.predict(
        [text]
    )[0]

    print(
        "Sentiment:",
        pred
    )