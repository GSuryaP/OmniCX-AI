import pandas as pd

reviews = pd.read_csv(
    "data/raw/olist_order_reviews_dataset.csv"
)

print(reviews.head())
print(reviews.shape)