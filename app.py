# 1063
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from pathlib import Path
# from groq import Groq
# import os

# # =====================================
# # PAGE CONFIG
# # =====================================

# st.set_page_config(
#     page_title="OmniCX AI",
#     page_icon="🛒",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # =====================================
# # CUSTOM CSS
# # =====================================

# st.markdown("""
# <style>

# .main {
#     padding-top: 1rem;
# }

# .metric-card {
#     background: #1f2937;
#     padding: 1rem;
#     border-radius: 12px;
#     border: 1px solid #374151;
# }

# .block-container {
#     padding-top: 1rem;
# }

# div[data-testid="metric-container"] {
#     background-color: #111827;
#     border: 1px solid #374151;
#     padding: 15px;
#     border-radius: 12px;
# }

# h1 {
#     color: #60a5fa;
# }

# </style>
# """, unsafe_allow_html=True)

# # =====================================
# # DATA LOADER
# # =====================================

# @st.cache_data
# def load_data():

#     BASE_DIR = Path(__file__).resolve().parent

#     df = pd.read_csv(
#         BASE_DIR /
#         "data/processed/final_dashboard_dataset.csv"
#     )

#     date_cols = [
#         "review_creation_date",
#         "review_answer_timestamp",
#         "order_purchase_timestamp",
#         "order_approved_at",
#         "order_delivered_carrier_date",
#         "order_delivered_customer_date",
#         "order_estimated_delivery_date",
#         "shipping_limit_date"
#     ]

#     df = df.copy()

#     for col in date_cols:

#         if col in df.columns:

#             df.loc[:, col] = pd.to_datetime(
#                 df[col],
#                 errors="coerce"
#             )

#     return df


# df = load_data()
# def value_count_df(series, column_name):

#     return (
#         series.value_counts()
#         .reset_index(name="count")
#         .rename(
#             columns={
#                 series.name: column_name
#             }
#         )
#     )

# # =====================================
# # GROQ CLIENT
# # =====================================

# def get_groq_client():

#     try:

#         api_key = None

#         if "GROQ_API_KEY" in st.secrets:
#             api_key = st.secrets["GROQ_API_KEY"]

#         elif os.getenv("GROQ_API_KEY"):
#             api_key = os.getenv("GROQ_API_KEY")

#         if api_key:
#             return Groq(api_key=api_key)

#     except Exception:
#         pass

#     return None

# # =====================================
# # SIDEBAR
# # =====================================

# st.sidebar.title("🎛️ Filters")

# sentiment_filter = st.sidebar.multiselect(
#     "Sentiment",
#     options=sorted(
#         df["sentiment"].dropna().unique()
#     ),
#     default=sorted(
#         df["sentiment"].dropna().unique()
#     )
# )

# priority_filter = st.sidebar.multiselect(
#     "Priority",
#     options=sorted(
#         df["priority"].dropna().unique()
#     ),
#     default=sorted(
#         df["priority"].dropna().unique()
#     )
# )

# category_filter = st.sidebar.multiselect(
#     "Product Category",
#     options=sorted(
#         df["product_category_name_english"]
#         .dropna()
#         .unique()
#     ),
#     default=[]
# )

# # =====================================
# # APPLY FILTERS
# # =====================================

# filtered_df = df.copy()

# filtered_df = filtered_df[
#     filtered_df["sentiment"]
#     .isin(sentiment_filter)
# ]

# filtered_df = filtered_df[
#     filtered_df["priority"]
#     .isin(priority_filter)
# ]

# if category_filter:

#     filtered_df = filtered_df[
#         filtered_df[
#             "product_category_name_english"
#         ].isin(category_filter)
#     ]

# # =====================================
# # HEADER
# # =====================================

# st.title("🛒 OmniCX AI")

# st.markdown("""
# ### AI-Powered Ecommerce Customer Experience Intelligence Platform

# Analyze customer reviews, delivery performance,
# root causes, sentiment trends, and product-category risks.
# """)

# st.divider()

# # =====================================
# # KPI CALCULATIONS
# # =====================================

# total_reviews = len(filtered_df)

# positive_count = (
#     filtered_df["sentiment"]
#     .eq("Positive")
#     .sum()
# )

# neutral_count = (
#     filtered_df["sentiment"]
#     .eq("Neutral")
#     .sum()
# )

# negative_count = (
#     filtered_df["sentiment"]
#     .eq("Negative")
#     .sum()
# )

# positive_pct = (
#     positive_count /
#     total_reviews * 100
# ) if total_reviews else 0

# neutral_pct = (
#     neutral_count /
#     total_reviews * 100
# ) if total_reviews else 0

# negative_pct = (
#     negative_count /
#     total_reviews * 100
# ) if total_reviews else 0

# cx_health_score = (
#     (
#         positive_count * 100
#         +
#         neutral_count * 60
#     )
#     /
#     total_reviews
# ) if total_reviews else 0

# high_priority_count = (
#     filtered_df["priority"]
#     .eq("High")
#     .sum()
# )

# avg_delay = (
#     filtered_df[
#         "delivery_delay_days"
#     ].mean()
# )

# avg_order_value = (
#     filtered_df["price"]
#     .mean()
# )

# ai_reviews = len(
#     filtered_df[
#         filtered_df["issue_category"]
#         != "Not Analyzed"
#     ]
# )

# # =====================================
# # KPI ROW
# # =====================================

# c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

# c1.metric(
#     "Reviews",
#     f"{total_reviews:,}"
# )

# c2.metric(
#     "Positive %",
#     f"{positive_pct:.1f}%"
# )

# c3.metric(
#     "Negative %",
#     f"{negative_pct:.1f}%"
# )

# c4.metric(
#     "CX Health",
#     f"{cx_health_score:.1f}"
# )

# c5.metric(
#     "High Priority",
#     f"{high_priority_count:,}"
# )

# c6.metric(
#     "Avg Delay",
#     f"{avg_delay:.1f} days"
# )

# c7.metric(
#     "AI RCA Reviews",
#     f"{ai_reviews:,}"
# )

# st.divider()

# # =====================================
# # TABS
# # =====================================

# tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
#     "📊 Executive Overview",
#     "😊 Sentiment Analytics",
#     "🚚 Delivery Intelligence",
#     "📦 Product Intelligence",
#     "🧠 AI RCA Center",
#     "🔍 Review Explorer",
#     "🤖 OmniCX Copilot"
# ])

# # =====================================
# # TAB 1 - EXECUTIVE OVERVIEW
# # =====================================

# with tab1:

#     st.subheader("Executive Summary")

#     ai_df = filtered_df[
#         filtered_df["issue_category"]
#         != "Not Analyzed"
#     ]

#     top_issue = "N/A"

#     if len(ai_df) > 0:
#         top_issue = (
#             ai_df["issue_category"]
#             .value_counts()
#             .idxmax()
#         )

#     st.info(f"""
#     Total Reviews: {total_reviews:,}

#     Positive Reviews: {positive_pct:.1f}%

#     Negative Reviews: {negative_pct:.1f}%

#     CX Health Score: {cx_health_score:.1f}

#     Top Issue Category: {top_issue}

#     High Priority Issues: {high_priority_count:,}
#     """)

#     col1, col2 = st.columns(2)

#     with col1:

#         fig = px.pie(
#             filtered_df,
#             names="sentiment",
#             title="Sentiment Distribution"
#         )

#         st.plotly_chart(
#             fig,
#             use_container_width=True,
#             key="sentiment_pie"
#         )

#     with col2:

#         if len(ai_df):

#             issue_counts = (
#                 ai_df["issue_category"]
#                 .value_counts()
#                 .reset_index(name="count")
#             )

#             issue_counts.columns = [
#                 "issue_category",
#                 "count"
#             ]

#             fig = px.bar(
#                 issue_counts,
#                 x="issue_category",
#                 y="count",
#                 title="Issue Category Breakdown"
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True,
#                 key="exec_issue_breakdown"
#             )

# # =====================================
# # TAB 2 - SENTIMENT ANALYTICS
# # =====================================

# with tab2:

#     st.subheader(
#         "Sentiment Distribution"
#     )

#     sentiment_counts = (
#         filtered_df["sentiment"]
#         .value_counts()
#         .reset_index(name="count")
#     )

#     sentiment_counts.columns = [
#         "sentiment",
#         "count"
#     ]

#     fig = px.bar(
#         sentiment_counts,
#         x="sentiment",
#         y="count",
#         color="sentiment"
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True,
#         key="sentiment_distribution"
#     )

#     st.subheader(
#         "Review Score Distribution"
#     )
    
#     fig = px.histogram(
#         filtered_df,
#         x="review_score",
#         nbins=5
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True, 
#         key="review_score_hist"
#     )

#     st.subheader(
#         "Sentiment vs Delivery Delay"
#     )

#     fig = px.box(
#         filtered_df,
#         x="sentiment",
#         y="delivery_delay_days",
#         color="sentiment"
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True,
#         key="sentiment_delay_box"
#     )

# # =====================================
# # TAB 3 - DELIVERY INTELLIGENCE
# # =====================================

# with tab3:

#     st.subheader(
#         "Delivery Delay Distribution"
#     )

#     fig = px.histogram(
#         filtered_df,
#         x="delivery_delay_days",
#         nbins=60
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True,
#         key="delivery_delay_hist"
#     )

#     st.subheader(
#         "Delay vs Review Score"
#     )

#     sample_df = filtered_df.sample(
#         min(5000, len(filtered_df)),
#         random_state=42
#     )

#     fig = px.scatter(
#         sample_df,
#         x="delivery_delay_days",
#         y="review_score",
#         color="sentiment"
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True, 
#         key="delivery_delay_scatter"
#     )

#     st.subheader(
#         "Delay by Sentiment"
#     )

#     fig = px.box(
#         filtered_df,
#         x="sentiment",
#         y="delivery_delay_days",
#         color="sentiment"
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True,
#         key="delivery_delay_box"
#     )

# # =====================================
# # TAB 4 - PRODUCT INTELLIGENCE
# # =====================================

# with tab4:

#     st.subheader(
#         "Top Product Categories"
#     )

#     category_counts = (
#         filtered_df[
#             "product_category_name_english"
#         ]
#         .value_counts()
#         .head(15)
#         .reset_index(name="count")
#     )

#     category_counts.columns = [
#         "product_category_name_english",
#         "count"
#     ]
    
#     fig = px.bar(
#         category_counts,
#         x="product_category_name_english",
#         y="count"
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True,
#         key="product_category_bar"
#     )

#     st.subheader(
#         "Revenue by Category"
#     )

#     revenue_df = (
#         filtered_df
#         .groupby(
#             "product_category_name_english"
#         )["price"]
#         .sum()
#         .sort_values(
#             ascending=False
#         )
#         .head(15)
#         .reset_index()
#     )
    
#     fig = px.bar(
#         revenue_df,
#         x="product_category_name_english",
#         y="price"
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True,
#         key="product_revenue_bar"
#     )

#     st.subheader(
#         "Category Sentiment Heatmap"
#     )

#     heatmap_df = pd.crosstab(
#         filtered_df[
#             "product_category_name_english"
#         ],
#         filtered_df["sentiment"]
#     )

#     heatmap_df = (
#         heatmap_df
#         .head(20)
#     )
    
#     fig = px.imshow(
#         heatmap_df,
#         aspect="auto",
#         title="Sentiment by Category"
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True,
#         key="category_sentiment_heatmap"
#     )

#     st.subheader(
#         "Top Negative Categories"
#     )

#     negative_df = filtered_df[
#         filtered_df["sentiment"]
#         == "Negative"
#     ]

#     negative_categories = (
#         negative_df[
#             "product_category_name_english"
#         ]
#         .value_counts()
#         .head(10)
#         .reset_index(name="count")
#     )

#     negative_categories.columns = [
#         "product_category_name_english",
#         "count"
#     ]
    
#     fig = px.bar(
#         negative_categories,
#         x="product_category_name_english",
#         y="count"
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True,
#         key="negative_category_bar"
#     )

# # =====================================
# # TAB 5 - AI RCA CENTER
# # =====================================

# with tab5:

#     st.subheader("AI Root Cause Analysis")

#     ai_df = filtered_df[
#         filtered_df["issue_category"]
#         != "Not Analyzed"
#     ].copy()

#     if len(ai_df) == 0:

#         st.warning(
#             "No AI-analyzed reviews available."
#         )

#     else:

#         col1, col2 = st.columns(2)

#         with col1:

#             issue_counts = (
#                 ai_df["issue_category"]
#                 .value_counts()
#                 .reset_index(name="count")
#             )

#             issue_counts.columns = [
#                 "issue_category",
#                 "count"
#             ]
            
#             fig = px.bar(
#                 issue_counts,
#                 x="issue_category",
#                 y="count",
#                 title="Issue Categories"
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True,
#                 key="rca_issue_chart"
#             )

#         with col2:

#             priority_counts = (
#                 ai_df["priority"]
#                 .value_counts()
#                 .reset_index(name="count")
#             )

#             priority_counts.columns = [
#                 "priority",
#                 "count"
#             ]
            
#             fig = px.bar(
#                 priority_counts,
#                 x="priority",
#                 y="count",
#                 title="Priority Distribution"
#             )

#             st.plotly_chart(
#                 fig,
#                 use_container_width=True,
#                 key="rca_priority_chart"
#             )

#         st.subheader(
#             "High Priority Issues"
#         )

#         high_df = ai_df[
#             ai_df["priority"] == "High"
#         ][[
#             "review_score",
#             "issue_category",
#             "root_cause",
#             "recommended_action"
#         ]]

#         st.dataframe(
#             high_df,
#             use_container_width=True
#         )

# # =====================================
# # TAB 6 - REVIEW EXPLORER
# # =====================================

# with tab6:

#     st.subheader(
#         "Review Explorer"
#     )

#     search_text = st.text_input(
#         "Search Reviews"
#     )

#     explorer_df = filtered_df.copy()

#     if search_text:

#         explorer_df = explorer_df[
#             explorer_df[
#                 "review_comment_message"
#             ]
#             .astype(str)
#             .str.contains(
#                 search_text,
#                 case=False,
#                 na=False
#             )
#         ]

#     display_cols = [
#         "review_score",
#         "sentiment",
#         "product_category_name_english",
#         "review_comment_message"
#     ]

#     st.dataframe(
#         explorer_df[
#             display_cols
#         ],
#         use_container_width=True,
#         height=500
#     )

#     csv = explorer_df.to_csv(
#         index=False
#     ).encode("utf-8")

#     st.download_button(
#         label="📥 Download Filtered Data",
#         data=csv,
#         file_name="omnicx_filtered_reviews.csv",
#         mime="text/csv"
#     )

# # =====================================
# # TAB 7 - OMNICX COPILOT
# # =====================================

# with tab7:

#     st.subheader(
#         "🤖 OmniCX AI Copilot"
#     )

#     st.markdown("""
# Ask questions about:

# - Customer experience risks
# - Delivery issues
# - Product quality problems
# - Priority complaints
# - Business recommendations
# - Executive summaries
# """)

#     question = st.text_area(
#         "Ask OmniCX AI",
#         placeholder="Why are customers unhappy?"
#     )

#     if st.button(
#         "Analyze with AI"
#     ):

#         client = get_groq_client()

#         if client is None:

#             st.error(
#                 "Groq API Key not configured."
#             )

#         else:

#             with st.spinner(
#                 "Analyzing..."
#             ):

#                 try:

#                     ai_df = filtered_df[
#                         filtered_df[
#                             "issue_category"
#                         ] != "Not Analyzed"
#                     ]

#                     issue_summary = ""

#                     if len(ai_df):

#                         issue_summary = (
#                             ai_df[
#                                 "issue_category"
#                             ]
#                             .value_counts()
#                             .to_string()
#                         )

#                     priority_summary = ""

#                     if len(ai_df):

#                         priority_summary = (
#                             ai_df[
#                                 "priority"
#                             ]
#                             .value_counts()
#                             .to_string()
#                         )

#                     top_categories = (
#                         filtered_df[
#                             "product_category_name_english"
#                         ]
#                         .value_counts()
#                         .head(10)
#                         .to_string()
#                     )

#                     negative_categories = (
#                         filtered_df[
#                             filtered_df["sentiment"] == "Negative"
#                         ][
#                             "product_category_name_english"
#                         ]
#                         .value_counts()
#                         .head(10)
#                         .to_string()
#                     )

#                     root_causes = ""

#                     if len(ai_df):

#                         root_causes = (
#                             ai_df[
#                                 "root_cause"
#                             ]
#                             .value_counts()
#                             .head(10)
#                             .to_string()
#                         )

#                     high_priority_issues = ""

#                     if len(ai_df):

#                         high_priority_issues = (
#                             ai_df[
#                                 ai_df["priority"] == "High"
#                             ][
#                                 "issue_category"
#                             ]
#                             .value_counts()
#                             .to_string()
#                         )

#                         context = f"""
#                         Business Summary

#                         Total Reviews:
#                         {total_reviews}

#                         Positive Reviews:
#                         {positive_pct:.2f}%

#                         Negative Reviews:
#                         {negative_pct:.2f}%

#                         CX Health Score:
#                         {cx_health_score:.2f}

#                         Average Delivery Delay:
#                         {avg_delay:.2f}

#                         AI RCA Sample Analysis
#                         (Generated from a subset of 100 AI-analyzed reviews)

#                         Issue Categories:
#                         {issue_summary}

#                         Priority Breakdown:
#                         {priority_summary}

#                         Most Common Root Causes:
#                         {root_causes}

#                         Top Product Categories:
#                         {top_categories}

#                         Top Negative Categories:
#                         {negative_categories}

#                         High Priority Issues:
#                         {high_priority_issues}

#                         User Question:
#                         {question}
#                         """

#                     response = (
#                         client.chat.completions.create(
#                             model="llama-3.3-70b-versatile",
#                             messages=[
#                                 {
#                                     "role": "system",
#                                     "content":
#                                     """
#                                 You are a Senior Ecommerce Customer Experience Consultant.

#                                 Analyze the provided business data.

#                                 Your answers MUST be data-driven and based only on the provided statistics.

#                                 Provide:

#                                 1. Executive Summary

#                                 2. Key Risks
#                                 - Mention actual issue categories
#                                 - Mention actual product categories

#                                 3. Root Causes
#                                 - Use provided root causes
#                                 - Rank by frequency

#                                 4. Recommendations
#                                 - Specific actions
#                                 - Category-specific improvements

#                                 5. Business Impact
#                                 - Customer satisfaction impact
#                                 - Revenue impact
#                                 - Retention impact

#                                 Avoid generic recommendations.
#                                 Use actual numbers from the dataset.
#                                 """
#                                 },
#                                 {
#                                     "role": "user",
#                                     "content": context
#                                 }
#                             ],
#                             temperature=0.2
#                         )
#                     )

#                     answer = (
#                         response
#                         .choices[0]
#                         .message
#                         .content
#                     )

#                     st.markdown(answer)

#                 except Exception as e:

#                     st.error(str(e))

# # =====================================
# # FOOTER
# # =====================================

# st.divider()

# st.caption(
#     """
# OmniCX AI • AI-Powered Ecommerce Customer Experience Intelligence Platform

# Built using:
# Streamlit • Plotly • Scikit-Learn • Groq • Olist Dataset
# """
# )



import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from groq import Groq
import os

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="OmniCX AI",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── ROOT & BASE ── */
:root {
    --bg-base:       #080c14;
    --bg-card:       #0d1422;
    --bg-card2:      #111827;
    --border:        rgba(99,179,237,0.15);
    --accent-blue:   #3b82f6;
    --accent-cyan:   #06b6d4;
    --accent-violet: #8b5cf6;
    --accent-pink:   #ec4899;
    --accent-green:  #10b981;
    --accent-amber:  #f59e0b;
    --text-primary:  #f0f6ff;
    --text-muted:    #8ba3c4;
    --gradient-hero: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
    --gradient-card: linear-gradient(145deg, rgba(59,130,246,0.08) 0%, rgba(139,92,246,0.05) 100%);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

.main, .block-container {
    background-color: var(--bg-base) !important;
    padding-top: 0.5rem !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0f1e 0%, #0d1422 100%) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: var(--text-primary) !important;
}

.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 1rem 0 1.5rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}

.sidebar-logo-icon {
    width: 40px;
    height: 40px;
    background: var(--gradient-hero);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}

.sidebar-logo-text {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.2rem;
    background: var(--gradient-hero);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.sidebar-section-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted) !important;
    margin: 1.2rem 0 0.5rem 0;
}

/* ── HERO HEADER ── */
.hero-banner {
    background: linear-gradient(135deg, rgba(59,130,246,0.15) 0%, rgba(139,92,246,0.1) 50%, rgba(236,72,153,0.08) 100%);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px;
    right: -60px;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(139,92,246,0.3) 0%, transparent 70%);
    border-radius: 50%;
}

.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px;
    left: 30%;
    width: 150px;
    height: 150px;
    background: radial-gradient(circle, rgba(6,182,212,0.2) 0%, transparent 70%);
    border-radius: 50%;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.4rem 0;
    line-height: 1.1;
}

.hero-subtitle {
    font-size: 0.95rem;
    color: var(--text-muted);
    font-weight: 400;
    max-width: 600px;
    line-height: 1.6;
    margin: 0;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    color: #60a5fa;
    margin-bottom: 0.8rem;
    letter-spacing: 0.03em;
}

/* ── KPI CARDS ── */
div[data-testid="metric-container"] {
    background: var(--gradient-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 1.2rem 1.4rem !important;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s ease, transform 0.2s ease;
}

div[data-testid="metric-container"]:hover {
    border-color: rgba(99,179,237,0.35) !important;
    transform: translateY(-2px);
}

div[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: var(--gradient-hero);
    opacity: 0.6;
}

div[data-testid="metric-container"] label {
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}

div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    line-height: 1.1 !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px !important;
    background: var(--bg-card2) !important;
    padding: 6px !important;
    border-radius: 14px !important;
    border: 1px solid var(--border) !important;
    margin-bottom: 1.5rem;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    padding: 8px 16px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.2s ease !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(59,130,246,0.25), rgba(139,92,246,0.2)) !important;
    color: #93c5fd !important;
    font-weight: 600 !important;
    border: 1px solid rgba(99,179,237,0.25) !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary) !important;
    background: rgba(255,255,255,0.04) !important;
}

.stTabs [data-baseweb="tab-panel"] {
    padding-top: 0 !important;
}

/* ── SECTION HEADERS ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 0.5rem 0 1.2rem 0;
}

.section-header-icon {
    width: 34px;
    height: 34px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}

.section-header-text h3 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 !important;
}

.section-header-text p {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin: 0 !important;
}

/* ── STAT SUMMARY CARD ── */
.stat-summary {
    background: var(--gradient-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
}

.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}

.stat-item {
    text-align: center;
    padding: 1rem;
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.05);
}

.stat-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 4px;
}

.stat-label {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-muted);
}

.positive { color: #34d399; }
.negative { color: #f87171; }
.neutral  { color: #60a5fa; }
.warning  { color: #fbbf24; }

/* ── TOP ISSUE PILL ── */
.top-issue-card {
    background: linear-gradient(135deg, rgba(139,92,246,0.12), rgba(236,72,153,0.08));
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 14px;
}

.top-issue-icon {
    font-size: 1.8rem;
}

.top-issue-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #a78bfa;
    margin-bottom: 2px;
}

.top-issue-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    overflow: hidden;
}

.stDataFrame > div {
    background: var(--bg-card) !important;
}

/* ── INPUTS ── */
.stTextInput > div > div,
.stTextArea > div > div {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s ease;
}

.stTextInput > div > div:focus-within,
.stTextArea > div > div:focus-within {
    border-color: rgba(99,179,237,0.5) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
}

.stTextInput input,
.stTextArea textarea {
    color: var(--text-primary) !important;
    background: transparent !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: var(--text-muted) !important;
}

/* ── MULTISELECT ── */
.stMultiSelect > div {
    background: var(--bg-card2) !important;
    border-radius: 10px !important;
}

.stMultiSelect [data-baseweb="select"] {
    background: var(--bg-card2) !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
}

.stMultiSelect [data-baseweb="tag"] {
    background: rgba(59,130,246,0.2) !important;
    border: 1px solid rgba(59,130,246,0.3) !important;
    border-radius: 6px !important;
    color: #93c5fd !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(59,130,246,0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(59,130,246,0.45) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── DOWNLOAD BUTTON ── */
[data-testid="stDownloadButton"] > button {
    background: rgba(16,185,129,0.15) !important;
    color: #34d399 !important;
    border: 1px solid rgba(16,185,129,0.3) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
}

[data-testid="stDownloadButton"] > button:hover {
    background: rgba(16,185,129,0.25) !important;
    transform: translateY(-1px) !important;
}

/* ── INFO / WARNING / ERROR ── */
.stAlert {
    border-radius: 14px !important;
    border: none !important;
}

[data-testid="stNotification"] {
    border-radius: 14px !important;
}

div[data-testid="stInfo"] {
    background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(6,182,212,0.08)) !important;
    border-left: 3px solid var(--accent-blue) !important;
    border-radius: 14px !important;
    color: var(--text-primary) !important;
}

div[data-testid="stWarning"] {
    background: rgba(245,158,11,0.1) !important;
    border-left: 3px solid var(--accent-amber) !important;
    border-radius: 14px !important;
}

div[data-testid="stError"] {
    background: rgba(239,68,68,0.1) !important;
    border-left: 3px solid #ef4444 !important;
    border-radius: 14px !important;
}

/* ── SPINNER ── */
.stSpinner > div {
    border-top-color: var(--accent-blue) !important;
}

/* ── DIVIDER ── */
hr {
    border-color: var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── CAPTION / FOOTER ── */
.stCaption, [data-testid="stCaptionContainer"] {
    color: var(--text-muted) !important;
    font-size: 0.75rem !important;
    text-align: center;
}

/* ── PLOTLY CHARTS ── */
.js-plotly-plot .plotly .main-svg {
    background: transparent !important;
}

/* ── SUBHEADER OVERRIDE ── */
h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
}

/* ── COPILOT RESPONSE ── */
.copilot-response {
    background: linear-gradient(145deg, rgba(59,130,246,0.07), rgba(139,92,246,0.05));
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-top: 1rem;
    line-height: 1.7;
}

.copilot-response h1, .copilot-response h2, .copilot-response h3 {
    color: #93c5fd !important;
}

/* ── STATUS DOTS ── */
.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10b981;
    margin-right: 6px;
    box-shadow: 0 0 6px #10b981;
    animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── CHART WRAPPERS ── */
.chart-card {
    background: var(--gradient-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}

/* ── SIDEBAR FILTER LABELS ── */
[data-testid="stSidebar"] .stMultiSelect label {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}

/* ── MARKDOWN ── */
.stMarkdown p {
    color: var(--text-muted);
    line-height: 1.7;
}

.stMarkdown strong {
    color: var(--text-primary);
}

</style>
""", unsafe_allow_html=True)

# =====================================
# DATA LOADER
# =====================================

@st.cache_data
def load_data():

    BASE_DIR = Path(__file__).resolve().parent

    df = pd.read_csv(
        BASE_DIR /
        "data/processed/final_dashboard_dataset.csv"
    )

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

    df = df.copy()

    for col in date_cols:

        if col in df.columns:

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )

    return df


df = load_data()


def value_count_df(series, column_name):

    return (
        series.value_counts()
        .reset_index(name="count")
        .rename(
            columns={
                series.name: column_name
            }
        )
    )

# =====================================
# GROQ CLIENT
# =====================================

def get_groq_client():

    try:

        api_key = None

        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]

        elif os.getenv("GROQ_API_KEY"):
            api_key = os.getenv("GROQ_API_KEY")

        if api_key:
            return Groq(api_key=api_key)

    except Exception:
        pass

    return None

# =====================================
# PLOTLY THEME
# =====================================

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family="Inter, sans-serif",
        color="#8ba3c4",
        size=12
    ),
    title_font=dict(
        family="Space Grotesk, sans-serif",
        color="#f0f6ff",
        size=15
    ),
    xaxis=dict(
        gridcolor="rgba(99,179,237,0.08)",
        linecolor="rgba(99,179,237,0.15)",
        tickfont=dict(color="#8ba3c4", size=11),
        title_font=dict(color="#8ba3c4")
    ),
    yaxis=dict(
        gridcolor="rgba(99,179,237,0.08)",
        linecolor="rgba(99,179,237,0.15)",
        tickfont=dict(color="#8ba3c4", size=11),
        title_font=dict(color="#8ba3c4")
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(99,179,237,0.15)",
        font=dict(color="#8ba3c4", size=11)
    ),
    margin=dict(l=10, r=10, t=40, b=10),
    colorway=["#3b82f6", "#8b5cf6", "#ec4899", "#10b981", "#f59e0b", "#06b6d4"]
)

def apply_theme(fig):
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🛒</div>
        <div class="sidebar-logo-text">OmniCX AI</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sidebar-section-label">🔵 Filters</p>', unsafe_allow_html=True)

    sentiment_filter = st.multiselect(
        "Sentiment",
        options=sorted(
            df["sentiment"].dropna().unique()
        ),
        default=sorted(
            df["sentiment"].dropna().unique()
        )
    )

    priority_filter = st.multiselect(
        "Priority",
        options=sorted(
            df["priority"].dropna().unique()
        ),
        default=sorted(
            df["priority"].dropna().unique()
        )
    )

    category_filter = st.multiselect(
        "Product Category",
        options=sorted(
            df["product_category_name_english"]
            .dropna()
            .unique()
        ),
        default=[]
    )

    st.markdown("---")
    st.markdown('<p class="sidebar-section-label">ℹ️ About</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.78rem; color:#8ba3c4; line-height:1.6;">
    AI-powered CX intelligence built on the Olist Dataset.
    Powered by Groq · Streamlit · Plotly.
    </div>
    """, unsafe_allow_html=True)

# =====================================
# APPLY FILTERS
# =====================================

filtered_df = df.copy()

filtered_df = filtered_df[
    filtered_df["sentiment"]
    .isin(sentiment_filter)
]

filtered_df = filtered_df[
    filtered_df["priority"]
    .isin(priority_filter)
]

if category_filter:

    filtered_df = filtered_df[
        filtered_df[
            "product_category_name_english"
        ].isin(category_filter)
    ]

# =====================================
# KPI CALCULATIONS
# =====================================

total_reviews = len(filtered_df)

positive_count = (
    filtered_df["sentiment"]
    .eq("Positive")
    .sum()
)

neutral_count = (
    filtered_df["sentiment"]
    .eq("Neutral")
    .sum()
)

negative_count = (
    filtered_df["sentiment"]
    .eq("Negative")
    .sum()
)

positive_pct = (
    positive_count /
    total_reviews * 100
) if total_reviews else 0

neutral_pct = (
    neutral_count /
    total_reviews * 100
) if total_reviews else 0

negative_pct = (
    negative_count /
    total_reviews * 100
) if total_reviews else 0

cx_health_score = (
    (
        positive_count * 100
        +
        neutral_count * 60
    )
    /
    total_reviews
) if total_reviews else 0

high_priority_count = (
    filtered_df["priority"]
    .eq("High")
    .sum()
)

avg_delay = (
    filtered_df[
        "delivery_delay_days"
    ].mean()
)

avg_order_value = (
    filtered_df["price"]
    .mean()
)

ai_reviews = len(
    filtered_df[
        filtered_df["issue_category"]
        != "Not Analyzed"
    ]
)

# =====================================
# HERO HEADER
# =====================================

st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">
        <span class="status-dot"></span>
        Live Intelligence Platform
    </div>
    <div class="hero-title">OmniCX AI</div>
    <p class="hero-subtitle">
        AI-Powered Ecommerce Customer Experience Intelligence &mdash;
        Analyze reviews, delivery performance, sentiment trends, root causes, and product-category risks in real time.
    </p>
</div>
""", unsafe_allow_html=True)

# =====================================
# KPI ROW
# =====================================

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

c1.metric(
    "📋 Total Reviews",
    f"{total_reviews:,}"
)

c2.metric(
    "✅ Positive",
    f"{positive_pct:.1f}%"
)

c3.metric(
    "⚠️ Negative",
    f"{negative_pct:.1f}%"
)

c4.metric(
    "💠 CX Health",
    f"{cx_health_score:.1f}"
)

c5.metric(
    "🔴 High Priority",
    f"{high_priority_count:,}"
)

c6.metric(
    "🚚 Avg Delay",
    f"{avg_delay:.1f}d"
)

c7.metric(
    "🧠 AI RCA",
    f"{ai_reviews:,}"
)

st.divider()

# =====================================
# TABS
# =====================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Executive Overview",
    "😊 Sentiment Analytics",
    "🚚 Delivery Intelligence",
    "📦 Product Intelligence",
    "🧠 AI RCA Center",
    "🔍 Review Explorer",
    "🤖 OmniCX Copilot"
])

# =====================================
# TAB 1 - EXECUTIVE OVERVIEW
# =====================================

with tab1:

    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon" style="background:linear-gradient(135deg,rgba(59,130,246,0.2),rgba(139,92,246,0.2));">📊</div>
        <div class="section-header-text">
            <h3>Executive Summary</h3>
            <p>High-level snapshot of CX health and critical issues</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    ai_df = filtered_df[
        filtered_df["issue_category"]
        != "Not Analyzed"
    ]

    top_issue = "N/A"

    if len(ai_df) > 0:
        top_issue = (
            ai_df["issue_category"]
            .value_counts()
            .idxmax()
        )

    # Summary stats row
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(59,130,246,0.07),rgba(139,92,246,0.05));
                border:1px solid rgba(99,179,237,0.18); border-radius:16px; padding:1.5rem; margin-bottom:1.2rem;">
        <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; text-align:center;">
            <div style="padding:1rem; background:rgba(255,255,255,0.03); border-radius:12px; border:1px solid rgba(255,255,255,0.05);">
                <div style="font-family:'Space Grotesk',sans-serif; font-size:1.8rem; font-weight:700; color:#34d399;">{positive_pct:.1f}%</div>
                <div style="font-size:0.7rem; font-weight:600; letter-spacing:0.08em; text-transform:uppercase; color:#8ba3c4;">Positive Reviews</div>
            </div>
            <div style="padding:1rem; background:rgba(255,255,255,0.03); border-radius:12px; border:1px solid rgba(255,255,255,0.05);">
                <div style="font-family:'Space Grotesk',sans-serif; font-size:1.8rem; font-weight:700; color:#f87171;">{negative_pct:.1f}%</div>
                <div style="font-size:0.7rem; font-weight:600; letter-spacing:0.08em; text-transform:uppercase; color:#8ba3c4;">Negative Reviews</div>
            </div>
            <div style="padding:1rem; background:rgba(255,255,255,0.03); border-radius:12px; border:1px solid rgba(255,255,255,0.05);">
                <div style="font-family:'Space Grotesk',sans-serif; font-size:1.8rem; font-weight:700; color:#60a5fa;">{cx_health_score:.1f}</div>
                <div style="font-size:0.7rem; font-weight:600; letter-spacing:0.08em; text-transform:uppercase; color:#8ba3c4;">CX Health Score</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Top issue
    st.markdown(f"""
    <div class="top-issue-card">
        <div class="top-issue-icon">⚡</div>
        <div>
            <div class="top-issue-label">Top Issue Category Detected</div>
            <div class="top-issue-value">{top_issue}</div>
        </div>
        <div style="margin-left:auto; text-align:right;">
            <div style="font-size:0.7rem; color:#8ba3c4; text-transform:uppercase; letter-spacing:0.06em;">High Priority</div>
            <div style="font-family:'Space Grotesk',sans-serif; font-size:1.4rem; font-weight:700; color:#f472b6;">{high_priority_count:,}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            filtered_df,
            names="sentiment",
            title="Sentiment Distribution",
            color_discrete_map={
                "Positive": "#10b981",
                "Neutral":  "#3b82f6",
                "Negative": "#ef4444"
            },
            hole=0.45
        )
        fig.update_traces(
            textfont=dict(color="#f0f6ff", size=12),
            marker=dict(line=dict(color="#080c14", width=2))
        )
        apply_theme(fig)
        st.plotly_chart(
            fig,
            use_container_width=True,
            key="sentiment_pie"
        )

    with col2:
        if len(ai_df):
            issue_counts = (
                ai_df["issue_category"]
                .value_counts()
                .reset_index(name="count")
            )
            issue_counts.columns = [
                "issue_category",
                "count"
            ]
            fig = px.bar(
                issue_counts,
                x="issue_category",
                y="count",
                title="Issue Category Breakdown",
                color="count",
                color_continuous_scale=["#3b82f6", "#8b5cf6", "#ec4899"]
            )
            fig.update_traces(marker_line_width=0)
            apply_theme(fig)
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(
                fig,
                use_container_width=True,
                key="exec_issue_breakdown"
            )

# =====================================
# TAB 2 - SENTIMENT ANALYTICS
# =====================================

with tab2:

    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon" style="background:linear-gradient(135deg,rgba(16,185,129,0.2),rgba(6,182,212,0.2));">😊</div>
        <div class="section-header-text">
            <h3>Sentiment Analytics</h3>
            <p>Customer emotion breakdown, score distribution, and delivery correlation</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    sentiment_counts = (
        filtered_df["sentiment"]
        .value_counts()
        .reset_index(name="count")
    )
    sentiment_counts.columns = [
        "sentiment",
        "count"
    ]

    fig = px.bar(
        sentiment_counts,
        x="sentiment",
        y="count",
        color="sentiment",
        title="Sentiment Distribution",
        color_discrete_map={
            "Positive": "#10b981",
            "Neutral":  "#3b82f6",
            "Negative": "#ef4444"
        }
    )
    fig.update_traces(marker_line_width=0, opacity=0.9)
    apply_theme(fig)
    st.plotly_chart(
        fig,
        use_container_width=True,
        key="sentiment_distribution"
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("##### Review Score Distribution")
        fig = px.histogram(
            filtered_df,
            x="review_score",
            nbins=5,
            title="Review Score Histogram",
            color_discrete_sequence=["#8b5cf6"]
        )
        fig.update_traces(marker_line_color="#080c14", marker_line_width=1.5)
        apply_theme(fig)
        st.plotly_chart(
            fig,
            use_container_width=True,
            key="review_score_hist"
        )

    with col_b:
        st.markdown("##### Sentiment vs Delivery Delay")
        fig = px.box(
            filtered_df,
            x="sentiment",
            y="delivery_delay_days",
            color="sentiment",
            title="Delay Days by Sentiment",
            color_discrete_map={
                "Positive": "#10b981",
                "Neutral":  "#3b82f6",
                "Negative": "#ef4444"
            }
        )
        fig.update_traces(marker_line_width=0)
        apply_theme(fig)
        st.plotly_chart(
            fig,
            use_container_width=True,
            key="sentiment_delay_box"
        )

# =====================================
# TAB 3 - DELIVERY INTELLIGENCE
# =====================================

with tab3:

    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon" style="background:linear-gradient(135deg,rgba(245,158,11,0.2),rgba(239,68,68,0.15));">🚚</div>
        <div class="section-header-text">
            <h3>Delivery Intelligence</h3>
            <p>Delay patterns, score correlation, and sentiment-delay relationships</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    fig = px.histogram(
        filtered_df,
        x="delivery_delay_days",
        nbins=60,
        title="Delivery Delay Distribution",
        color_discrete_sequence=["#f59e0b"]
    )
    fig.update_traces(marker_line_color="#080c14", marker_line_width=1)
    apply_theme(fig)
    st.plotly_chart(
        fig,
        use_container_width=True,
        key="delivery_delay_hist"
    )

    col_a, col_b = st.columns(2)

    with col_a:
        sample_df = filtered_df.sample(
            min(5000, len(filtered_df)),
            random_state=42
        )
        fig = px.scatter(
            sample_df,
            x="delivery_delay_days",
            y="review_score",
            color="sentiment",
            title="Delay vs Review Score",
            opacity=0.55,
            color_discrete_map={
                "Positive": "#10b981",
                "Neutral":  "#3b82f6",
                "Negative": "#ef4444"
            }
        )
        apply_theme(fig)
        st.plotly_chart(
            fig,
            use_container_width=True,
            key="delivery_delay_scatter"
        )

    with col_b:
        fig = px.box(
            filtered_df,
            x="sentiment",
            y="delivery_delay_days",
            color="sentiment",
            title="Delay by Sentiment",
            color_discrete_map={
                "Positive": "#10b981",
                "Neutral":  "#3b82f6",
                "Negative": "#ef4444"
            }
        )
        apply_theme(fig)
        st.plotly_chart(
            fig,
            use_container_width=True,
            key="delivery_delay_box"
        )

# =====================================
# TAB 4 - PRODUCT INTELLIGENCE
# =====================================

with tab4:

    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon" style="background:linear-gradient(135deg,rgba(6,182,212,0.2),rgba(59,130,246,0.2));">📦</div>
        <div class="section-header-text">
            <h3>Product Intelligence</h3>
            <p>Category volume, revenue breakdown, sentiment heatmap, and risk signals</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    category_counts = (
        filtered_df[
            "product_category_name_english"
        ]
        .value_counts()
        .head(15)
        .reset_index(name="count")
    )
    category_counts.columns = [
        "product_category_name_english",
        "count"
    ]

    fig = px.bar(
        category_counts,
        x="product_category_name_english",
        y="count",
        title="Top Product Categories by Volume",
        color="count",
        color_continuous_scale=["#3b82f6", "#06b6d4", "#10b981"]
    )
    fig.update_traces(marker_line_width=0)
    apply_theme(fig)
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(
        fig,
        use_container_width=True,
        key="product_category_bar"
    )

    col_a, col_b = st.columns(2)

    with col_a:
        revenue_df = (
            filtered_df
            .groupby(
                "product_category_name_english"
            )["price"]
            .sum()
            .sort_values(ascending=False)
            .head(15)
            .reset_index()
        )
        fig = px.bar(
            revenue_df,
            x="product_category_name_english",
            y="price",
            title="Revenue by Category",
            color="price",
            color_continuous_scale=["#8b5cf6", "#ec4899", "#f59e0b"]
        )
        fig.update_traces(marker_line_width=0)
        apply_theme(fig)
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(
            fig,
            use_container_width=True,
            key="product_revenue_bar"
        )

    with col_b:
        negative_df = filtered_df[
            filtered_df["sentiment"] == "Negative"
        ]
        negative_categories = (
            negative_df[
                "product_category_name_english"
            ]
            .value_counts()
            .head(10)
            .reset_index(name="count")
        )
        negative_categories.columns = [
            "product_category_name_english",
            "count"
        ]
        fig = px.bar(
            negative_categories,
            x="product_category_name_english",
            y="count",
            title="⚠️ Top Negative Categories",
            color="count",
            color_continuous_scale=["#fbbf24", "#f87171", "#ef4444"]
        )
        fig.update_traces(marker_line_width=0)
        apply_theme(fig)
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(
            fig,
            use_container_width=True,
            key="negative_category_bar"
        )

    st.markdown("##### Sentiment Heatmap by Category")
    heatmap_df = pd.crosstab(
        filtered_df[
            "product_category_name_english"
        ],
        filtered_df["sentiment"]
    )
    heatmap_df = heatmap_df.head(20)

    fig = px.imshow(
        heatmap_df,
        aspect="auto",
        title="Sentiment by Category (Top 20)",
        color_continuous_scale="RdBu"
    )
    apply_theme(fig)
    st.plotly_chart(
        fig,
        use_container_width=True,
        key="category_sentiment_heatmap"
    )

# =====================================
# TAB 5 - AI RCA CENTER
# =====================================

with tab5:

    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon" style="background:linear-gradient(135deg,rgba(139,92,246,0.25),rgba(236,72,153,0.15));">🧠</div>
        <div class="section-header-text">
            <h3>AI Root Cause Analysis</h3>
            <p>AI-classified issue categories, priorities, and recommended actions</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    ai_df = filtered_df[
        filtered_df["issue_category"]
        != "Not Analyzed"
    ].copy()

    if len(ai_df) == 0:
        st.warning("No AI-analyzed reviews available with current filters.")
    else:

        col1, col2 = st.columns(2)

        with col1:
            issue_counts = (
                ai_df["issue_category"]
                .value_counts()
                .reset_index(name="count")
            )
            issue_counts.columns = [
                "issue_category",
                "count"
            ]
            fig = px.bar(
                issue_counts,
                x="issue_category",
                y="count",
                title="Issue Categories",
                color="count",
                color_continuous_scale=["#3b82f6", "#8b5cf6", "#ec4899"]
            )
            fig.update_traces(marker_line_width=0)
            apply_theme(fig)
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(
                fig,
                use_container_width=True,
                key="rca_issue_chart"
            )

        with col2:
            priority_counts = (
                ai_df["priority"]
                .value_counts()
                .reset_index(name="count")
            )
            priority_counts.columns = [
                "priority",
                "count"
            ]
            fig = px.bar(
                priority_counts,
                x="priority",
                y="count",
                title="Priority Distribution",
                color="priority",
                color_discrete_map={
                    "High":   "#ef4444",
                    "Medium": "#f59e0b",
                    "Low":    "#10b981"
                }
            )
            fig.update_traces(marker_line_width=0)
            apply_theme(fig)
            st.plotly_chart(
                fig,
                use_container_width=True,
                key="rca_priority_chart"
            )

        st.markdown("""
        <div style="display:flex; align-items:center; gap:8px; margin:1rem 0 0.7rem 0;">
            <span style="background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.3);
                         color:#f87171; font-size:0.72rem; font-weight:600; letter-spacing:0.08em;
                         text-transform:uppercase; padding:3px 10px; border-radius:20px;">🔴 High Priority Issues</span>
        </div>
        """, unsafe_allow_html=True)

        high_df = ai_df[
            ai_df["priority"] == "High"
        ][[
            "review_score",
            "issue_category",
            "root_cause",
            "recommended_action"
        ]]

        st.dataframe(
            high_df,
            use_container_width=True
        )

# =====================================
# TAB 6 - REVIEW EXPLORER
# =====================================

with tab6:

    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon" style="background:linear-gradient(135deg,rgba(16,185,129,0.2),rgba(6,182,212,0.15));">🔍</div>
        <div class="section-header-text">
            <h3>Review Explorer</h3>
            <p>Search, filter, and export individual customer reviews</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    search_text = st.text_input(
        "🔎 Search Reviews",
        placeholder="Type a keyword to search review messages..."
    )

    explorer_df = filtered_df.copy()

    if search_text:
        explorer_df = explorer_df[
            explorer_df[
                "review_comment_message"
            ]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    st.markdown(f"""
    <div style="font-size:0.8rem; color:#8ba3c4; margin-bottom:0.6rem;">
        Showing <strong style="color:#60a5fa;">{len(explorer_df):,}</strong> reviews
    </div>
    """, unsafe_allow_html=True)

    display_cols = [
        "review_score",
        "sentiment",
        "product_category_name_english",
        "review_comment_message"
    ]

    st.dataframe(
        explorer_df[
            display_cols
        ],
        use_container_width=True,
        height=500
    )

    csv = explorer_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Filtered Data",
        data=csv,
        file_name="omnicx_filtered_reviews.csv",
        mime="text/csv"
    )

# =====================================
# TAB 7 - OMNICX COPILOT
# =====================================

with tab7:

    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon" style="background:linear-gradient(135deg,rgba(59,130,246,0.25),rgba(139,92,246,0.2));">🤖</div>
        <div class="section-header-text">
            <h3>OmniCX AI Copilot</h3>
            <p>Ask natural-language questions, get data-driven executive insights instantly</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:1.2rem;">
        <span style="background:rgba(59,130,246,0.1); border:1px solid rgba(59,130,246,0.25);
                     color:#93c5fd; font-size:0.75rem; padding:4px 12px; border-radius:20px;">
            📉 Why are customers unhappy?
        </span>
        <span style="background:rgba(139,92,246,0.1); border:1px solid rgba(139,92,246,0.25);
                     color:#c4b5fd; font-size:0.75rem; padding:4px 12px; border-radius:20px;">
            🚚 What's causing delivery issues?
        </span>
        <span style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.25);
                     color:#6ee7b7; font-size:0.75rem; padding:4px 12px; border-radius:20px;">
            📦 Which categories have quality problems?
        </span>
        <span style="background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.25);
                     color:#fcd34d; font-size:0.75rem; padding:4px 12px; border-radius:20px;">
            📋 Give me an executive summary
        </span>
    </div>
    """, unsafe_allow_html=True)

    question = st.text_area(
        "Ask OmniCX AI",
        placeholder="e.g. Why are customers leaving negative reviews? What are the top risks?",
        height=100
    )

    if st.button("🚀 Analyze with AI", use_container_width=False):

        client = get_groq_client()

        if client is None:
            st.error("⚠️ Groq API Key not configured. Add it to your .streamlit/secrets.toml or environment variables.")
        else:
            with st.spinner("🧠 Analyzing your data..."):
                try:

                    ai_df = filtered_df[
                        filtered_df[
                            "issue_category"
                        ] != "Not Analyzed"
                    ]

                    issue_summary = ""

                    if len(ai_df):
                        issue_summary = (
                            ai_df["issue_category"]
                            .value_counts()
                            .to_string()
                        )

                    priority_summary = ""

                    if len(ai_df):
                        priority_summary = (
                            ai_df["priority"]
                            .value_counts()
                            .to_string()
                        )

                    top_categories = (
                        filtered_df[
                            "product_category_name_english"
                        ]
                        .value_counts()
                        .head(10)
                        .to_string()
                    )

                    negative_categories = (
                        filtered_df[
                            filtered_df["sentiment"] == "Negative"
                        ][
                            "product_category_name_english"
                        ]
                        .value_counts()
                        .head(10)
                        .to_string()
                    )

                    root_causes = ""

                    if len(ai_df):
                        root_causes = (
                            ai_df["root_cause"]
                            .value_counts()
                            .head(10)
                            .to_string()
                        )

                    high_priority_issues = ""

                    if len(ai_df):
                        high_priority_issues = (
                            ai_df[
                                ai_df["priority"] == "High"
                            ][
                                "issue_category"
                            ]
                            .value_counts()
                            .to_string()
                        )

                    context = f"""
                    Business Summary

                    Total Reviews:
                    {total_reviews}

                    Positive Reviews:
                    {positive_pct:.2f}%

                    Negative Reviews:
                    {negative_pct:.2f}%

                    CX Health Score:
                    {cx_health_score:.2f}

                    Average Delivery Delay:
                    {avg_delay:.2f}

                    AI RCA Sample Analysis
                    (Generated from a subset of 100 AI-analyzed reviews)

                    Issue Categories:
                    {issue_summary}

                    Priority Breakdown:
                    {priority_summary}

                    Most Common Root Causes:
                    {root_causes}

                    Top Product Categories:
                    {top_categories}

                    Top Negative Categories:
                    {negative_categories}

                    High Priority Issues:
                    {high_priority_issues}

                    User Question:
                    {question}
                    """

                    response = (
                        client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {
                                    "role": "system",
                                    "content": """
                                You are a Senior Ecommerce Customer Experience Consultant.

                                Analyze the provided business data.

                                Your answers MUST be data-driven and based only on the provided statistics.

                                Provide:

                                1. Executive Summary

                                2. Key Risks
                                - Mention actual issue categories
                                - Mention actual product categories

                                3. Root Causes
                                - Use provided root causes
                                - Rank by frequency

                                4. Recommendations
                                - Specific actions
                                - Category-specific improvements

                                5. Business Impact
                                - Customer satisfaction impact
                                - Revenue impact
                                - Retention impact

                                Avoid generic recommendations.
                                Use actual numbers from the dataset.
                                """
                                },
                                {
                                    "role": "user",
                                    "content": context
                                }
                            ],
                            temperature=0.2
                        )
                    )

                    answer = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    st.markdown(f"""
                    <div class="copilot-response">
                    {answer}
                    </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# =====================================
# FOOTER
# =====================================

st.divider()

st.markdown("""
<div style="text-align:center; padding:1rem 0;">
    <div style="font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:0.9rem;
                background:linear-gradient(135deg,#60a5fa,#a78bfa,#f472b6);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
                margin-bottom:0.4rem;">
        OmniCX AI
    </div>
    <div style="font-size:0.75rem; color:#8ba3c4;">
        AI-Powered Ecommerce Customer Experience Intelligence Platform<br>
        <span style="opacity:0.6;">Built with Streamlit · Plotly · Scikit-Learn · Groq · Olist Dataset</span>
    </div>
</div>
""", unsafe_allow_html=True)