# ITN-Usage-Prediction
Connect with your research report

📄 README.md
markdown
Copy
Edit
# 🛏️ ITN Usage Prediction App

**Predict insecticide-treated net (ITN) usage patterns among individuals to support malaria prevention programs using machine learning and an interactive Streamlit web app.**

---

## 💡 Problem Statement

> Despite numerous malaria prevention campaigns, many pregnant women and community members still do not consistently use insecticide-treated nets (ITNs).  
> But why? Who are most at risk? What barriers exist?  
> Can we use data and technology to address these questions?

---

## 🧩 Key Questions This App Helps Answer

- Who is at high risk of not using ITNs regularly?
- How do education, age, location, and attitude influence ITN usage?
- Can we segment people based on predicted usage and target education programs more effectively?
- How can health workers simulate interventions and predict behavioral changes?
- Are ITN usage patterns improving over time across different campaigns or locations?

---

## 🎯 What This App Does

| Problem to Solve | ML/Analytics Feature | Web App Solution |
|------------------|----------------------|------------------|
| Identify those at risk | ML-based prediction of ITN usage | Upload survey data and get usage predictions |
| Understand usage drivers | Feature encoding & labeling | Shows patterns by education, residence, and attitude |
| Segment population | Predicted labels: 'Every night', 'Sometimes', 'Rarely', 'Never' | Visual risk segmentation via charts |
| Monitor trends | Save historical predictions | View ITN usage trends over time |
| Run interventions | What-If input simulation | Test scenarios (e.g. change age or attitude) live |
| Enable decision-making | Data-backed predictions | Empowers health workers, planners, NGOs |

---

## 📁 Files Included

- `app.py`: Streamlit web app source code
- `itn_xgb_model.pkl`: Trained XGBoost model
- `target_label_encoder.pkl`: Encodes predicted labels
- `images/logo.JPG`: Custom branding/logo
- `history/`: Folder to store and track uploaded prediction results
- `research_report.pdf`: 📚 Your full academic/project research report *(add this)*

---

## 🚀 Getting Started

### 📦 Requirements

```bash
pip install -r requirements.txt
▶️ Run the App
bash
Copy
Edit
streamlit run app.py
📊 Input Formats
CSV files

Excel files (.xlsx, .xls)

Google Sheets (shared public URL)

You can select your own column names during upload, no need to match training data exactly.

🤖 Machine Learning Details
Model used: XGBoostClassifier

Multi-class prediction: ITN usage frequency

Features used:

Educational level

Age category

Urban/Rural residence

Attitude toward ITN

🌍 Why This Matters
This app can contribute significantly to malaria prevention strategies by:

Predicting usage gaps before they become health crises

Empowering community health workers with data-driven insights

Tracking effectiveness of awareness and distribution programs

Simulating policies before costly implementations

Even if it improves ITN adherence by just 5–10%, that's lives saved.

🙋🏽‍♂️ Created By
Ebenezer Kwaw
AI Enthusiast | Public Health Advocate | Data for Good

📬 Feedback & Contributions
Feel free to open issues or contribute improvements. Let’s make this app even more useful for real-world impact.
