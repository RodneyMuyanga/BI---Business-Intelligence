import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import joblib
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# Setup
# -----------------------------
st.set_page_config(page_title="Employee Attrition Analysis", layout="wide")
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, 'employeeattrition.csv')

@st.cache_data
def load_and_clean_data(path):
    df = pd.read_csv(path)
    df.drop(columns=['EmployeeCount', 'Over18', 'StandardHours', 'EmployeeNumber'], inplace=True)
    df['Attrition_Flag'] = df['Attrition'].map({'Yes': 1, 'No': 0})
    if 'OverTime' in df.columns:
        df['OverTime'] = df['OverTime'].map({'Yes': 1, 'No': 0})
    df_encoded = pd.get_dummies(df, drop_first=True)
    return df, df_encoded

df_raw, df_clean = load_and_clean_data(file_path)

st.title("💼 Employee Attrition Analysis")

# -----------------------------
# 🎯 Predict Employee Attrition (Fixed)
# -----------------------------
st.header("🎯 Predict Employee Attrition")

model_map = {
    "Logistic Regression": "logistic_model.pkl",
    "Random Forest": "randomforest_model.pkl",
    "K-Nearest Neighbors": "knn_model.pkl"
}
selected_model_name = st.selectbox("Select a model", list(model_map.keys()))
model_path = os.path.join(base_dir, model_map[selected_model_name])
model = joblib.load(model_path)

# Load feature list from training
feature_list = joblib.load(os.path.join(base_dir, "model_features.pkl"))

st.markdown("### ✍️ Enter employee data:")

with st.form("predict_form"):
    age = st.slider("Age", 18, 60, 30)
    income = st.number_input("Monthly Income", 1000, 20000, 5000)
    years = st.slider("Total Working Years", 0, 40, 5)
    dist = st.slider("Distance From Home", 0, 50, 10)
    overtime = st.selectbox("OverTime", ["No", "Yes"])
    jsat = st.slider("Job Satisfaction", 1, 4, 3)
    esat = st.slider("Environment Satisfaction", 1, 4, 3)
    years_company = st.slider("Years at Company", 0, 40, 3)
    submit = st.form_submit_button("Predict")

if submit:
    overtime_val = 1 if overtime == "Yes" else 0
    input_df = pd.DataFrame([[
        age, income, jsat, dist, years_company, 3, esat, overtime_val, 1, years
    ]], columns=[
        'Age', 'MonthlyIncome', 'JobSatisfaction', 'DistanceFromHome',
        'YearsAtCompany', 'WorkLifeBalance', 'EnvironmentSatisfaction',
        'OverTime', 'BusinessTravel_Travel_Rarely', 'TotalWorkingYears'
    ])
    full_input = pd.DataFrame(columns=feature_list)
    for col in input_df.columns:
        full_input[col] = input_df[col]
    full_input.fillna(0, inplace=True)

    pred = model.predict(full_input)[0]
    prob = model.predict_proba(full_input)[0][1]

    if pred == 1:
        st.error(f"❌ The employee is likely to leave. (Confidence: {prob:.2%})")
    else:
        st.success(f"✅ The employee is likely to stay. (Confidence: {1 - prob:.2%})")

# -----------------------------
# 🔥 Top 5 Feature Importance
# -----------------------------
st.header("🔥 Top 5 Most Relevant Factors for Attrition")
X = df_clean.drop(columns=['Attrition_Flag'])
y = df_clean['Attrition_Flag']
model_rf = RandomForestClassifier(random_state=42)
model_rf.fit(X, y)
importances = pd.Series(model_rf.feature_importances_, index=X.columns)
top5 = importances.sort_values(ascending=False).head(5)
desc = {
    "MonthlyIncome": "Monthly salary. Low pay can lead to dissatisfaction.",
    "OverTime": "Frequent overtime may cause burnout.",
    "TotalWorkingYears": "Fewer years = less experience and loyalty.",
    "Age": "Younger employees may change jobs more.",
    "Attrition_Yes": "Encoded attrition label (ignore in interpretation)."
}
top5_df = pd.DataFrame({
    "Feature": top5.index,
    "Importance (%)": (top5.values * 100).round(2),
    "Description": [desc.get(f, "N/A") for f in top5.index]
})
st.dataframe(top5_df)

# -----------------------------
# 📊 Visualizations
# -----------------------------
st.header("📊 Visualizations")
fig1, ax1 = plt.subplots()
sns.countplot(x='Attrition', data=df_raw, ax=ax1)
ax1.set_title("Attrition Count")
st.pyplot(fig1)

fig2, ax2 = plt.subplots(figsize=(14, 10))
sns.heatmap(df_clean.corr(numeric_only=True), annot=False, cmap='coolwarm', ax=ax2)
st.pyplot(fig2)

# -----------------------------
# 📌 Feature Exploration
# -----------------------------
st.header("📌 Explore Individual Features")
feature = st.selectbox("Choose a feature", df_raw.columns)
fig3, ax3 = plt.subplots()
if df_raw[feature].dtype == 'object':
    sns.countplot(y=feature, data=df_raw, order=df_raw[feature].value_counts().index, ax=ax3)
else:
    sns.histplot(df_raw[feature], kde=True, bins=20, ax=ax3)
st.pyplot(fig3)

# -----------------------------
# 🧩 Clustering
# -----------------------------
st.header("🧩 Clustering: Segment Employees")
cluster_features = [
    'Age', 'MonthlyIncome', 'JobSatisfaction', 'DistanceFromHome',
    'YearsAtCompany', 'WorkLifeBalance', 'EnvironmentSatisfaction',
    'OverTime', 'NumCompaniesWorked'
]
X_cluster = df_clean[cluster_features]
scores = []
K_range = range(2, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_cluster)
    scores.append(silhouette_score(X_cluster, labels))
best_k = K_range[np.argmax(scores)]
st.success(f"✅ Best cluster count: {best_k} (Score: {max(scores):.2f})")

fig4, ax4 = plt.subplots()
ax4.plot(K_range, scores, marker='o')
ax4.set_title("Silhouette Score vs. Number of Clusters")
ax4.set_xlabel("k"); ax4.set_ylabel("Score")
st.pyplot(fig4)

# PCA visual
kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_cluster)
pca = PCA(n_components=2)
pca_data = pd.DataFrame(pca.fit_transform(X_cluster), columns=["PC1", "PC2"])
pca_data['Cluster'] = labels
fig5, ax5 = plt.subplots()
sns.scatterplot(data=pca_data, x="PC1", y="PC2", hue="Cluster", palette="Set2", ax=ax5)
st.pyplot(fig5)

# -----------------------------
# 📥 Download Cleaned Data
# -----------------------------
st.header("📥 Download Cleaned Dataset")
st.download_button("Download CSV", df_clean.to_csv(index=False), "cleaned_employee_attrition.csv", "text/csv")
