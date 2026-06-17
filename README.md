# OmniCX AI: Ecommerce Customer Experience Intelligence Platform

OmniCX AI is an AI-powered intelligence platform designed to analyze ecommerce customer reviews, delivery performance, product-category risks, and root causes of dissatisfaction. It provides an interactive, state-of-the-art Streamlit dashboard alongside background machine learning and LLM-driven root-cause analysis workflows.

The application leverages the **Olist Brazilian Ecommerce Dataset** and integrates a scikit-learn sentiment classification pipeline with advanced reasoning via the **Groq API** (Llama 3.3 70B) to automate root cause analysis (RCA) and generate actionable business insights.

---

## 🚀 Key Features

* **📊 Executive Overview**: High-level KPIs (CX Health Score, Review counts, Sentiment trends, top issue distributions).
* **😊 Sentiment Analytics**: Visualizing sentiment breakdowns, review score distributions, and sentiment vs. delivery delays.
* **🚚 Delivery Intelligence**: Analyzing delivery delays, delay distributions, and their direct impact on customer satisfaction.
* **📦 Product Intelligence**: Identifying category-specific performance, revenue by category, and mapping category sentiment heatmaps.
* **🧠 AI RCA Center**: Interactive dashboard showing AI-categorized issues (Delivery, Payment, Product Quality, Customer Service) and recommending specific actions.
* **🔍 Review Explorer**: A searchable data explorer with download options for filtered feedback.
* **🤖 OmniCX Copilot**: An interactive AI consultant powered by Groq to answer natural language queries based on your customer data.

---

## 📂 Project Structure

```text
omnicx-ai-hack/
├── app.py                     # Main Streamlit web application
├── requirements.txt           # Python project dependencies
├── .env                       # Environment variables (API keys)
├── .gitignore                 # Files excluded from git tracking
├── .streamlit/
│   └── secrets.toml           # Streamlit-specific configuration/secrets
├── data/
│   ├── raw/                   # Original source CSV files from Olist dataset
│   └── processed/             # Merged and AI-analyzed datasets used by the app
├── models/
│   ├── sentiment_model.pkl    # Serialized scikit-learn LogisticRegression pipeline
│   └── tfidf_vectorizer.pkl   # TF-IDF vectorizer configuration
└── scripts/
    ├── preprocess.py          # Data ingestion, cleaning, and preprocessing script
    ├── train_model.py         # Trains the machine learning sentiment classifier
    ├── groq_analysis.py       # Batch LLM processing for root cause analysis (RCA)
    ├── merge_ai_results.py    # Merges ML and LLM results into the dashboard dataset
    ├── predict.py             # CLI utility for testing the sentiment classifier
    ├── data_test.py           # Quick sanity check for dataset integrity
    └── utils.py               # Shared utility functions
```

---

## 🛠️ Installation & Setup

Follow these steps to set up and run the project locally.

### 1. Clone the Repository & Navigate to Project
```bash
git clone <repository_url>
cd omnicx-ai-hack
```

### 2. Set Up the Virtual Environment
The project includes a virtual environment in the `omni-hack` folder. Activate it using:
```bash
source omni-hack/bin/activate
```
*(If you need to create a new virtual environment: `python3 -m venv venv && source venv/bin/activate`)*

### 3. Install Dependencies
Install all required python packages:
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys & Secrets
The OmniCX Copilot and AI RCA tools require a Groq API Key. 

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Alternatively, you can set it up inside the Streamlit secrets file `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY="your_groq_api_key_here"
```

---

## 🔄 Running the Data & ML Pipeline

If you want to re-run the entire pipeline from raw data to trained models and AI analytics, run the scripts in the following order:

### Step 1: Preprocess Raw Data
Merge raw customer, orders, reviews, and translation datasets into a unified dataset:
```bash
python scripts/preprocess.py
```
*Output: `data/processed/merged_reviews.csv`*

### Step 2: Train the Sentiment Classifier Model
Train the scikit-learn TF-IDF + Logistic Regression pipeline on the reviews dataset:
```bash
python scripts/train_model.py
```
*Output: `models/sentiment_model.pkl`*

### Step 3: Run AI Root-Cause Analysis (Batch)
Extract actionable negative reviews and perform batch analysis via the Groq Llama model:
```bash
python scripts/groq_analysis.py
```
*Output: `data/processed/groq_analysis.csv`*

### Step 4: Merge AI Analysis with Core Dataset
Combine the preprocessed dataset with the AI RCA tags to construct the final dashboard dataset:
```bash
python scripts/merge_ai_results.py
```
*Output: `data/processed/final_dashboard_dataset.csv`*

---

## 🖥️ Running the Application

### Launch the Streamlit Dashboard
To run the interactive analytics dashboard, execute:
```bash
streamlit run app.py
```
The application will start, and a browser window should open automatically at `http://localhost:8501`.

### Run CLI Sentiment Predictor
To test single review classification interactively in your terminal:
```bash
python scripts/predict.py
```
Enter any review text when prompted to see its predicted sentiment (Positive, Neutral, or Negative).
