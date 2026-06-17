from pathlib import Path
import pandas as pd

# =====================================
# PATHS
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# =====================================
# LOAD DATASETS
# =====================================

print("Loading datasets...")

reviews = pd.read_csv(
    RAW_DIR / "olist_order_reviews_dataset.csv"
)

orders = pd.read_csv(
    RAW_DIR / "olist_orders_dataset.csv"
)

items = pd.read_csv(
    RAW_DIR / "olist_order_items_dataset.csv"
)

products = pd.read_csv(
    RAW_DIR / "olist_products_dataset.csv"
)

translation = pd.read_csv(
    RAW_DIR / "product_category_name_translation.csv"
)

# =====================================
# TRANSLATE PRODUCT CATEGORIES
# =====================================

products = products.merge(
    translation,
    on="product_category_name",
    how="left"
)

# =====================================
# MERGE DATASETS
# =====================================

print("Merging datasets...")

df = reviews.merge(
    orders,
    on="order_id",
    how="left"
)

df = df.merge(
    items,
    on="order_id",
    how="left"
)

df = df.merge(
    products,
    on="product_id",
    how="left"
)

df = df.copy()

# =====================================
# DATE CONVERSION
# =====================================

date_cols = [
    "review_creation_date",
    "review_answer_timestamp",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "shipping_limit_date"
]

print("Converting date columns...")

for col in date_cols:

    if col in df.columns:

        df[col] = pd.to_datetime(
            df[col],
            errors="coerce"
        )

# =====================================
# SENTIMENT LABELS
# =====================================

print("Generating sentiment labels...")

def get_sentiment(score):

    if score <= 2:
        return "Negative"

    elif score == 3:
        return "Neutral"

    else:
        return "Positive"


df["sentiment"] = (
    df["review_score"]
    .apply(get_sentiment)
)

# =====================================
# DELIVERY DELAY
# =====================================

print("Calculating delivery delay...")

delivered = pd.to_datetime(
    df["order_delivered_customer_date"],
    errors="coerce"
)

estimated = pd.to_datetime(
    df["order_estimated_delivery_date"],
    errors="coerce"
)

df["delivery_delay_days"] = (
    delivered - estimated
).dt.days

# =====================================
# HANDLE NULLS
# =====================================

print("Handling null values...")

df["review_comment_message"] = (
    df["review_comment_message"]
    .fillna("No Review")
)

df["review_comment_title"] = (
    df["review_comment_title"]
    .fillna("")
)

if "product_category_name" in df.columns:

    df["product_category_name"] = (
        df["product_category_name"]
        .fillna("Unknown")
    )

if "product_category_name_english" in df.columns:

    df["product_category_name_english"] = (
        df["product_category_name_english"]
        .fillna("Unknown")
    )

# =====================================
# SAVE OUTPUT
# =====================================

OUTPUT_FILE = (
    PROCESSED_DIR /
    "merged_reviews.csv"
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

# =====================================
# SUMMARY
# =====================================

print("\nPreprocessing Complete")
print(f"Saved: {OUTPUT_FILE}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

print("\nVerification:")

checks = [
    "sentiment",
    "delivery_delay_days",
    "product_category_name",
    "product_category_name_english"
]

for col in checks:

    print(
        f"{col}:",
        col in df.columns
    )

if "product_category_name_english" in df.columns:

    print("\nTop Product Categories:")

    print(
        df["product_category_name_english"]
        .value_counts()
        .head(10)
    )