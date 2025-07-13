import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import os
from datetime import datetime
from sklearn.preprocessing import LabelEncoder

# Load model and label encoder
model = pickle.load(open("itn_xgb_model.pkl", "rb"))
label_encoder = pickle.load(open("target_label_encoder.pkl", "rb"))

# Features used in model
model_features = ['educational_level_encoded',
                  'age_category_encoded',
                  'do_you_live_in_an_urban_or_rural_area?_encoded',
                  'how_do_you_feel_about_using_an_itn_every_night?_encoded']

# Sidebar branding
st.sidebar.image("images/logo.JPG", width=150)
st.sidebar.markdown("**Created by Ebenezer Kwaw**")

# Title
st.title("🛏️ ITN Usage Prediction")
st.markdown("Predict and monitor the use of insecticide-treated nets (ITNs) to support malaria prevention programs.")

# Tabs for different features
tab1, tab2, tab3, tab4 = st.tabs(["📥 Predict Usage", "📊 Risk Segmentation", "📈 Trends Over Time", "🧪 What-If Simulation"])

# ===========================
# 📥 Predict Usage
# ===========================
with tab1:
    st.header("Upload Survey Data for Prediction")
    uploaded_file = st.file_uploader("Upload CSV, Excel, or enter Google Sheet link below", type=["csv", "xlsx", "xls"])
    google_sheet_url = st.text_input("Or paste a public Google Sheet URL")

    data = None

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

    elif google_sheet_url:
        try:
            sheet_id = google_sheet_url.split("/d/")[1].split("/")[0]
            export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
            data = pd.read_csv(export_url)
            st.success("✅ Google Sheet loaded successfully")
        except Exception as e:
            st.error(f"Error loading Google Sheet: {e}")

    if data is not None:
        # Remove duplicate columns early
        data = data.loc[:, ~data.columns.duplicated()]

        st.subheader("🧭 Map Your Data Columns to Required Fields")
        all_columns = data.columns.tolist()

        selected_edu = st.selectbox("Select column for Educational Level", all_columns)
        selected_age = st.selectbox("Select column for Age Category", all_columns)
        selected_residence = st.selectbox("Select column for Residence (Urban/Rural)", all_columns)
        selected_attitude = st.selectbox("Select column for Attitude Toward ITN", all_columns)

        try:
            data['educational_level_encoded'] = LabelEncoder().fit_transform(data[selected_edu])
            data['age_category_encoded'] = LabelEncoder().fit_transform(data[selected_age])
            data['do_you_live_in_an_urban_or_rural_area?_encoded'] = LabelEncoder().fit_transform(data[selected_residence])
            data['how_do_you_feel_about_using_an_itn_every_night?_encoded'] = LabelEncoder().fit_transform(data[selected_attitude])

            data['predicted'] = model.predict(data[model_features])

            # Remove duplicate columns again if needed
            data = data.loc[:, ~data.columns.duplicated()]

            # Drop old prediction if it exists
            if 'predicted_label' in data.columns:
                data = data.drop(columns=['predicted_label'])

            data['predicted_label'] = label_encoder.inverse_transform(data['predicted'])
            st.success("✅ Prediction completed.")
            st.dataframe(data[[selected_edu, selected_age, 'predicted_label']])

            if not os.path.exists("history"):
                os.makedirs("history")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            data.to_csv(f"history/predictions_{timestamp}.csv", index=False)

        except Exception as e:
            st.error(f"❌ Error during prediction: {e}")

# ===========================
# 📊 Risk Segmentation
# ===========================
with tab2:
    st.header("Risk Segmentation by Predicted Usage")
    if data is not None and 'predicted_label' in data.columns:
        usage_counts = data['predicted_label'].value_counts()
        st.bar_chart(usage_counts)
        st.markdown("Segment population by predicted ITN usage behavior.")
    else:
        st.info("Please upload and process data in the 'Predict Usage' tab first.")

# ===========================
# 📈 Trends Over Time
# ===========================
with tab3:
    st.header("Trends in ITN Usage Over Time")
    if os.path.exists("history"):
        history_files = sorted([f for f in os.listdir("history") if f.endswith(".csv")])
        trend_data = []

        for file in history_files:
            df_hist = pd.read_csv(os.path.join("history", file))
            if 'predicted_label' not in df_hist.columns:
                continue
            counts = df_hist['predicted_label'].value_counts(normalize=True)
            row = {"timestamp": file.split("_")[1].replace(".csv", "")}
            row.update(counts)
            trend_data.append(row)

        trend_df = pd.DataFrame(trend_data).fillna(0)
        trend_df = trend_df.set_index("timestamp")
        st.line_chart(trend_df)
        st.markdown("Monitor prediction changes over time: weekly, monthly, quarterly, etc.")
    else:
        st.info("Upload prediction data first in the 'Predict Usage' tab.")

# ===========================
# 🧪 What-If Simulation
# ===========================
with tab4:
    st.header("Simulate Different Scenarios")
    st.markdown("Change inputs to see how predictions vary for different demographic or behavioral factors.")

    education = st.selectbox("Educational Level", [0, 1, 2, 3])
    age_category = st.selectbox("Age Category", [0, 1, 2])
    residence = st.selectbox("Residence", [0, 1])
    attitude = st.selectbox("Attitude Toward ITN", [0, 1, 2])

    input_df = pd.DataFrame([[education, age_category, residence, attitude]],
                            columns=model_features)
    prediction = model.predict(input_df)
    predicted_label = label_encoder.inverse_transform(prediction)[0]

    st.success(f"🎯 Predicted ITN Usage: **{predicted_label}**")
