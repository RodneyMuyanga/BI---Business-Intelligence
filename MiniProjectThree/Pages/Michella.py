import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

# Settings
st.set_page_config(page_title="Employee Salary Insights", layout="wide")
st.title("💼 Employee Salary Prediction & Analysis")

# Sidebar navigation
page = st.sidebar.radio("Select Page", ["Salary Prediction", "Data Visualizations"])

# Load cleaned dataset
DATA_PATH = "data/attrition_clean.csv"
df = pd.read_csv(DATA_PATH)

# Load trained model
MODEL_PATH = "models/income_regression_model.pkl"
model = joblib.load(MODEL_PATH)

# -------------------- PAGE 1: SALARY PREDICTION --------------------
if page == "Salary Prediction":
    st.subheader("🧾 Enter Employee Information")

    age = st.slider("Age", 18, 60, 30)
    job_level = st.selectbox("Job Level", [1, 2, 3, 4, 5])
    working_years = st.slider("Total Working Years", 0, 40, 5)
    years_at_company = st.slider("Years at Current Company", 0, 30, 3)
    overtime = st.radio("Overtime Work", ["No", "Yes"])
    distance = st.slider("Distance from Home (km)", 1, 30, 10)
    education = st.selectbox("Education Level", [1, 2, 3, 4, 5])
    performance = st.selectbox("Performance Rating", [1, 2, 3, 4])
    satisfaction = st.selectbox("Environmental Satisfaction", [1, 2, 3, 4])

    overtime_binary = 1 if overtime == "Yes" else 0

    features = np.array([[age, job_level, working_years, years_at_company,
                          overtime_binary, distance, education, performance, satisfaction]])

    if st.button("🔍 Predict Monthly Salary"):

        prediction = model.predict(features)[0]
        lower = int(prediction * 0.9)
        upper = int(prediction * 1.1)

        st.success(f"💰 Estimated Monthly Salary: **{int(prediction):,} units**")
        st.caption(f"📉 Approximate range (±10%): {lower:,} – {upper:,} units")
        st.caption("Note: Salary units are from a synthetic dataset and do not reflect any real currency.")
    
    st.markdown("We applied linear regression to predict monthly income in the synthetic dataset. The model achieved a high R² score (0.89), indicating that it explains the majority of the variation in income. However, the model occasionally produced unrealistic results, especially for profiles with many years of experience. This is likely due to the limitations of linear regression in capturing non-linear relationships, as well as overlapping explanatory variables (e.g., age and total working years).")

# -------------------- PAGE 2: DATA VISUALIZATION --------------------
elif page == "Data Visualizations":
    st.subheader("📊 Explore Salary-related Patterns")

    option = st.radio("Choose a visualization:", [
        "Age vs. Salary (Scatterplot)",
        "Job Level vs. Salary (Boxplot)",
        "Correlation Matrix"
    ])

    if option == "Age vs. Salary (Scatterplot)":
        st.write("Relationship between age and monthly income.")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x="Age", y="MonthlyIncome", alpha=0.6, ax=ax)
        ax.set_xlabel("Age")
        ax.set_ylabel("Monthly Income (units)")
        ax.set_title("Age vs. Monthly Income")
        ax.grid(True)
        st.pyplot(fig)

    elif option == "Job Level vs. Salary (Boxplot)":
        st.write("Salary distribution by job level.")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.boxplot(data=df, x="JobLevel", y="MonthlyIncome", ax=ax)
        ax.set_xlabel("Job Level")
        ax.set_ylabel("Monthly Income (units)")
        ax.set_title("Monthly Income per Job Level")
        st.pyplot(fig)

    elif option == "Correlation Matrix":
        st.write("Correlation between numeric variables.")
        corr = df.corr(numeric_only=True)

        fig, ax = plt.subplots(figsize=(14, 12))
        sns.heatmap(corr, cmap="coolwarm", center=0, linewidths=0.5, ax=ax)
        ax.set_title("Correlation Matrix")
        st.pyplot(fig)
