from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

import pandas as pd
import json
import os
import time

# =====================================
# CONFIG
# =====================================

SAMPLE_SIZE = 250
SAVE_EVERY = 25

# =====================================
# LOAD ENV
# =====================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found in .env"
    )

client = Groq(api_key=api_key)

# =====================================
# PATHS
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR /
    "data/processed/merged_reviews.csv"
)

OUTPUT_FILE = (
    BASE_DIR /
    "data/processed/groq_analysis.csv"
)

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv(INPUT_FILE)

print(f"\nTotal Reviews: {len(df):,}")

# =====================================
# KEEP ONLY ACTIONABLE REVIEWS
# =====================================

df = df[
    df["sentiment"] != "Positive"
].copy()

df = df[
    df["review_comment_message"] != "No Review"
].copy()

df = df[
    df["review_comment_message"]
    .astype(str)
    .str.len() > 5
].copy()

print(
    f"Actionable Reviews: {len(df):,}"
)

# =====================================
# RESUME SUPPORT
# =====================================

if OUTPUT_FILE.exists():

    existing_df = pd.read_csv(
        OUTPUT_FILE
    )

    processed_ids = set(
        existing_df["review_id"]
    )

    print(
        f"Already Processed: {len(processed_ids):,}"
    )

    df = df[
        ~df["review_id"].isin(
            processed_ids
        )
    ]

else:

    existing_df = pd.DataFrame()

print(
    f"Remaining Reviews: {len(df):,}"
)

# =====================================
# SAMPLE
# =====================================

sample_size = min(
    SAMPLE_SIZE,
    len(df)
)

df = df.sample(
    n=sample_size,
    random_state=42
)

print(
    f"Analyzing {sample_size} reviews..."
)

# =====================================
# ANALYSIS
# =====================================

results = []

for i, (_, row) in enumerate(
    df.iterrows(),
    start=1
):

    review = str(
        row["review_comment_message"]
    ).strip()

    prompt = f"""
You are an Ecommerce Customer Experience Analyst.

Analyze this customer review.

Review:
{review}

Return ONLY valid JSON.

{{
    "issue_category":"",
    "priority":"",
    "root_cause":"",
    "recommended_action":""
}}

Rules:

issue_category must be one of:
Delivery
Payment
Product Quality
Customer Service
Other

priority must be one of:
High
Medium
Low
"""

    try:

        response = (
            client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0
            )
        )

        content = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        content = (
            content
            .replace(
                "```json",
                ""
            )
            .replace(
                "```",
                ""
            )
            .strip()
        )

        parsed = json.loads(
            content
        )

        results.append({
            "review_id":
                row["review_id"],

            "order_id":
                row["order_id"],

            "sentiment":
                row["sentiment"],

            "issue_category":
                parsed.get(
                    "issue_category",
                    "Other"
                ),

            "priority":
                parsed.get(
                    "priority",
                    "Low"
                ),

            "root_cause":
                parsed.get(
                    "root_cause",
                    "Unknown"
                ),

            "recommended_action":
                parsed.get(
                    "recommended_action",
                    "Manual Review"
                )
        })

    except Exception as e:

        error_msg = str(e)

        print(
            f"\n[ERROR] Review {i}"
        )

        print(error_msg)

        # Stop if quota exhausted

        if (
            "rate_limit_exceeded"
            in error_msg
            or
            "429"
            in error_msg
        ):

            print(
                "\nGroq quota exhausted."
            )

            print(
                "Saving progress..."
            )

            break

        results.append({
            "review_id":
                row["review_id"],

            "order_id":
                row["order_id"],

            "sentiment":
                row["sentiment"],

            "issue_category":
                "Other",

            "priority":
                "Low",

            "root_cause":
                "Unknown",

            "recommended_action":
                "Manual Review"
        })

    # =================================
    # SAVE CHECKPOINTS
    # =================================

    if i % SAVE_EVERY == 0:

        temp_df = pd.concat(
            [
                existing_df,
                pd.DataFrame(results)
            ],
            ignore_index=True
        )

        temp_df.to_csv(
            OUTPUT_FILE,
            index=False
        )

        print(
            f"Processed {i}/{sample_size}"
        )

    time.sleep(0.2)

# =====================================
# FINAL SAVE
# =====================================

final_df = pd.concat(
    [
        existing_df,
        pd.DataFrame(results)
    ],
    ignore_index=True
)

final_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nAnalysis Complete")

print(
    f"Saved: {OUTPUT_FILE}"
)

print(
    f"Rows: {len(final_df):,}"
)

if len(final_df):

    print("\nIssue Breakdown:\n")

    print(
        final_df["issue_category"]
        .value_counts()
    )