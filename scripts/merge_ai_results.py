from pathlib import Path
import pandas as pd

# =====================================
# PATHS
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

REVIEWS_FILE = (
    BASE_DIR /
    "data/processed/merged_reviews.csv"
)

GROQ_FILE = (
    BASE_DIR /
    "data/processed/groq_analysis.csv"
)

OUTPUT_FILE = (
    BASE_DIR /
    "data/processed/final_dashboard_dataset.csv"
)

# =====================================
# LOAD DATA
# =====================================

reviews_df = pd.read_csv(REVIEWS_FILE)
groq_df = pd.read_csv(GROQ_FILE)

print(f"Reviews rows: {len(reviews_df):,}")
print(f"Groq rows: {len(groq_df):,}")

# =====================================
# MERGE DATASETS
# =====================================

final_df = reviews_df.merge(
    groq_df,
    on=[
        "review_id",
        "order_id",
        "sentiment"
    ],
    how="left"
)

# Create a clean copy
final_df = final_df.copy()

# =====================================
# FILL MISSING AI VALUES
# =====================================

ai_columns = [
    "issue_category",
    "priority",
    "root_cause",
    "recommended_action"
]

for col in ai_columns:
    final_df[col] = (
        final_df[col]
        .fillna("Not Analyzed")
    )


# =====================================
# SAVE FINAL DATASET
# =====================================

final_df.to_csv(
    OUTPUT_FILE,
    index=False
)

# =====================================
# SUMMARY
# =====================================

print("\nMerged Successfully")
print(f"Saved: {OUTPUT_FILE}")
print(f"Rows: {len(final_df):,}")
print(f"Columns: {len(final_df.columns)}")

print("\nAI Analysis Summary")
print(
    final_df["issue_category"]
    .value_counts()
    .head(10)
)

print("\nPriority Summary")
print(
    final_df["priority"]
    .value_counts()
)

print("\nMissing Values Check")

for col in ai_columns:
    print(
        f"{col}: "
        f"{final_df[col].isna().sum()}"
    )

print("\nFinal dashboard dataset ready.")