import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    df_red = pd.read_excel("winequality-red.xlsx", header=1)
    df_white = pd.read_excel("winequality-white.xlsx", header=1)
    df_red["type"] = "red"
    df_white["type"] = "white"
    df_combined = pd.concat([df_red, df_white], ignore_index=True)
    return df_red, df_white, df_combined

df_red, df_white, df_combined = load_data()

# Sidebar navigation
st.sidebar.title("Mini Project 2 Navigation")
section = st.sidebar.radio("Go to:", [
    "Task 6 – Descriptive Statistics",
    "Task 7 – Visual Comparison",
    "Task 11 – Outliers",
    "Task 12 – Correlation Filtering"
])

if section == "Task 6 – Descriptive Statistics":
    st.title("Task 6: Descriptive Statistics and Normal Distribution Check")

    st.subheader("Red Wine – Alcohol Distribution")
    fig, ax = plt.subplots()
    ax.hist(df_red['alcohol'], bins=30)
    ax.set_title('Alcohol Distribution (Red Wine)')
    st.pyplot(fig)

    st.markdown("""
**Observation:**  
The distribution of alcohol content is not normal. This is clearly visible in the histogram, where the distribution is right-skewed and not symmetrical. Most wines have an alcohol content between 9% and 11%, while fewer wines have high alcohol content. The shape does not resemble a bell curve, which is characteristic of a normal distribution.
""")

    st.subheader("White Wine – Alcohol Distribution")
    fig, ax = plt.subplots()
    ax.hist(df_white['alcohol'], bins=30)
    ax.set_title('Alcohol Distribution (White Wine)')
    st.pyplot(fig)

    st.markdown("""**Observation:**
            The distribution of alcohol content in white wines is also not normal. Although it appears somewhat less skewed than the red wine distribution, it still shows a right-skewed shape with most wines clustered between 9% and 11% alcohol. The distribution is not perfectly symmetrical and does not follow the typical bell-shaped curve of a normal distribution.
            """)

    st.subheader("Descriptive Statistics – Red Wine")
    st.dataframe(df_red.describe())

    st.subheader("Descriptive Statistics – White Wine")
    st.dataframe(df_white.describe())

elif section == "Task 7 – Visual Comparison":
    st.title("Task 7: Comparison Between Red and White Wines")

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined, x="type", y="quality", ax=ax)
    ax.set_title("Wine Quality Comparison")
    st.pyplot(fig)

    st.markdown("**7b - The boxplot shows the distribution of wine quality ratings for red and white wines. The median quality is almost identical for both types, around 6. However, white wines have slightly more high outliers, indicating that there may be more high-quality white wines in the dataset. Overall, the average difference in quality between red and white wines is minimal.**")


    st.subheader("Quartiles")
    st.markdown("Red Wine")
    st.write(df_red["quality"].quantile([0.25, 0.5, 0.75]))
    st.markdown("White Wine")
    st.write(df_white["quality"].quantile([0.25, 0.5, 0.75]))
    st.markdown("**The median quality is 6, which is the same as the third quartile. Because the median and Q3 have the same value, the horizontal line representing the median is visually merged with the top edge of the box in the boxplot, and therefore not visible as a separate line.**")

    fig, ax = plt.subplots()
    for wine_type in ["red", "white"]:
        subset = df_combined[df_combined["type"] == wine_type]
        ax.hist(subset["alcohol"], bins=30, alpha=0.5, label=wine_type)
    ax.legend()
    ax.set_title("Alcohol Content by Wine Type")
    st.pyplot(fig)
    st.markdown("**7c - The histogram shows that white wines generally have a higher average alcohol content than red wines. Although both wine types have most samples clustered between 9% and 12%, white wine has a broader distribution and more samples with alcohol levels above 12%. This suggests that white wines in this dataset tend to have slightly higher alcohol content on average.**")


    fig, ax = plt.subplots()
    for wine_type in ["red", "white"]:
        subset = df_combined[df_combined["type"] == wine_type]
        ax.hist(subset["residual sugar"], bins=30, alpha=0.5, label=wine_type)
    ax.legend()
    ax.set_title("Residual Sugar by Wine Type")
    st.pyplot(fig)
    st.markdown("**7d - The average residual sugar content is clearly higher in white wine than in red wine. This is confirmed both by the descriptive statistics and by the visualizations. While red wines typically have low sugar content around 2–3 g/dm³, white wines show a broader range and often exceed 6 g/dm³. This reflects the common winemaking practice of allowing more residual sugar in white wines to balance acidity and flavor.**")


    fig, ax = plt.subplots()
    sns.scatterplot(data=df_combined, x="alcohol", y="quality", hue="type", ax=ax)
    ax.set_title("Alcohol vs Quality")
    st.pyplot(fig)

    fig, ax = plt.subplots()
    sns.scatterplot(data=df_combined, x="residual sugar", y="quality", hue="type", ax=ax)
    ax.set_title("Residual Sugar vs Quality")
    st.pyplot(fig)
    st.markdown("**The scatter plot and correlation analysis show that alcohol content has a positive correlation with wine quality. This means that, generally, wines with higher alcohol levels tend to be rated higher in quality. On the other hand, residual sugar does not show a clear relationship with wine quality. The correlation is very weak, and the scatter plot shows no clear pattern. In conclusion, alcohol content appears to influence quality more than sugar does – especially in red wines.**")


elif section == "Task 11 – Outliers":
    st.title("Task 11: Outlier Detection in Residual Sugar")

    Q1 = df_combined["residual sugar"].quantile(0.25)
    Q3 = df_combined["residual sugar"].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df_combined[(df_combined["residual sugar"] < lower) | (df_combined["residual sugar"] > upper)]
    st.write(f"Number of outliers: {len(outliers)}")
    st.write("First 5 outlier rows:")
    st.write(outliers.head())

    df_cleaned = df_combined.drop(outliers.index)
    st.write(f"New dataset shape: {df_cleaned.shape}")

    st.markdown("""
**Explanation – Outlier Removal in 'Residual Sugar':**  
To improve data quality, we analyzed the `residual sugar` feature for outliers using the IQR (Interquartile Range) method.  
Values that were far outside the typical range (below Q1 - 1.5×IQR or above Q3 + 1.5×IQR) were identified as outliers.  

We found **118 outliers**, mostly wines with very high sugar content (e.g. above 17–20 g/dm³), which are rare and can skew the analysis.  
These rows were removed to ensure the dataset better represents the main distribution of wines.  

After removing the outliers, the dataset was reduced from **6497 to 6379 rows**.  
This step helps improve the robustness of further statistical analysis.
""")

elif section == "Task 12 – Correlation Filtering":
    st.title("Task 12: Remove Weak or Redundant Features")

    df_cleaned = df_combined.copy()
    corr_matrix = df_cleaned.corr(numeric_only=True)
    st.dataframe(corr_matrix.round(2))

    columns_to_drop = ["density", "free sulfur dioxide", "citric acid"]
    st.write("Columns removed:", columns_to_drop)
    df_reduced = df_cleaned.drop(columns=columns_to_drop)
    st.write(f"New dataset shape: {df_reduced.shape}")

    st.markdown("""
**Explanation:**  
The three columns removed had either a weak correlation with wine quality or a strong correlation with other independent variables.  
- `"density"` was strongly related to both `"residual sugar"` and `"alcohol"`, making it redundant.  
- `"free sulfur dioxide"` was highly correlated with `"total sulfur dioxide"`, so one was removed.  
- `"citric acid"` had little to no impact on wine quality and was therefore excluded.  

This cleaning step helps reduce multicollinearity and simplifies the dataset for future analysis, such as PCA or machine learning models.
""")