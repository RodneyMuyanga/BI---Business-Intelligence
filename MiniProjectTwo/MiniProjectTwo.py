import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


redWineData = "winequality-red.xlsx"
whiteWineData = "winequality-white.xlsx"

dfRedWine = pd.read_excel(redWineData, header = 1)
dfWhiteWine = pd.read_excel(whiteWineData, header = 1)

#
print(dfRedWine.describe())
print(dfWhiteWine.describe())

# Streamlit titel
st.title("Mini Project 2: Data Exploration and Visualisation - Task 6")
st.subheader("Wine Quality Data - Alcohol Distribution")

# Opret figur og akse
fig, ax = plt.subplots()

ax.hist(dfRedWine['alcohol'], bins=30)

ax.set_title('Alcohol Distribution of red wine')
ax.set_xlabel('Alcohol')
ax.set_ylabel('Frequency')

st.pyplot(fig)

st.markdown("""
**Observation:**  
The distribution of alcohol content is not normal. This is clearly visible in the histogram, where the distribution is right-skewed and not symmetrical. Most wines have an alcohol content between 9% and 11%, while fewer wines have high alcohol content. The shape does not resemble a bell curve, which is characteristic of a normal distribution.
""")

fig, ax = plt.subplots()

# Brug ax.hist() direkte (IKKE df['alcohol'].hist())
ax.hist(dfWhiteWine['alcohol'], bins=30)

# Tilføj aksetitler
ax.set_title('Alcohol Distribution of white wine')
ax.set_xlabel('Alcohol')
ax.set_ylabel('Frequency')

st.pyplot(fig)

st.markdown("""**Observation:**
            The distribution of alcohol content in white wines is also not normal. Although it appears somewhat less skewed than the red wine distribution, it still shows a right-skewed shape with most wines clustered between 9% and 11% alcohol. The distribution is not perfectly symmetrical and does not follow the typical bell-shaped curve of a normal distribution.
            """)

# Titel
st.title("Descriptive Statistics – White Wine")

# Vis deskriptiv statistik i appen
st.subheader("Summary Statistics")
st.dataframe(dfWhiteWine.describe())

st.title("Descriptive Statistics - Red Wine")

st.subheader("Summary Statistics")
st.dataframe(dfRedWine.describe())

st.title("Mini Project 2: Data Exploration and Visualisation - Task 7")
dfRedWine["type"] = "red"
dfWhiteWine["type"] = "white"
df_combined = pd.concat([dfRedWine, dfWhiteWine], ignore_index=True)

fig, ax = plt.subplots()
sns.boxplot(data=df_combined, x="type", y="quality", ax=ax)
ax.set_title("Wine Quality Comparison – Red vs. White")
st.pyplot(fig)
st.markdown("**7b - The boxplot shows the distribution of wine quality ratings for red and white wines. The median quality is almost identical for both types, around 6. However, white wines have slightly more high outliers, indicating that there may be more high-quality white wines in the dataset. Overall, the average difference in quality between red and white wines is minimal.**")


# Vis kvartiler
st.subheader("Quartiles for Wine Quality")
st.markdown("Red Wine")
st.write(dfRedWine["quality"].quantile([0.25, 0.5, 0.75]))
st.markdown("White Wine")
st.write(dfWhiteWine["quality"].quantile([0.25, 0.5, 0.75]))
st.markdown("**The median quality is 6, which is the same as the third quartile. Because the median and Q3 have the same value, the horizontal line representing the median is visually merged with the top edge of the box in the boxplot, and therefore not visible as a separate line.**")

fig, ax = plt.subplots()
for wine_type in ["red", "white"]:
    subset = df_combined[df_combined["type"] == wine_type]
    ax.hist(subset["alcohol"], bins=30, alpha=0.5, label=wine_type)
ax.set_title("Alcohol Content by Wine Type")
ax.set_xlabel("Alcohol")
ax.set_ylabel("Frequency")
ax.legend()
st.pyplot(fig)

st.markdown("**7c - The histogram shows that white wines generally have a higher average alcohol content than red wines. Although both wine types have most samples clustered between 9% and 12%, white wine has a broader distribution and more samples with alcohol levels above 12%. This suggests that white wines in this dataset tend to have slightly higher alcohol content on average.**")

df_combined.groupby("type")["residual sugar"].mean()
fig, ax = plt.subplots()
for wine_type in ["red", "white"]:
    subset = df_combined[df_combined["type"] == wine_type]
    ax.hist(subset["residual sugar"], bins=30, alpha=0.5, label=wine_type)
ax.set_title("Residual Sugar by Wine Type")
ax.set_xlabel("Residual Sugar (g/dm³)")
ax.set_ylabel("Frequency")
ax.legend()
st.pyplot(fig)

st.markdown("**7d - The average residual sugar content is clearly higher in white wine than in red wine. This is confirmed both by the descriptive statistics and by the visualizations. While red wines typically have low sugar content around 2–3 g/dm³, white wines show a broader range and often exceed 6 g/dm³. This reflects the common winemaking practice of allowing more residual sugar in white wines to balance acidity and flavor.**")


st.title("Do Alcohol and Sugar Influence Wine Quality?")
fig, ax = plt.subplots()
sns.scatterplot(data=df_combined, x="alcohol", y="quality", hue="type", ax=ax)
ax.set_title("Alcohol vs. Quality")
st.pyplot(fig)

fig, ax = plt.subplots()
sns.scatterplot(data=df_combined, x="residual sugar", y="quality", hue="type", ax=ax)
ax.set_title("Residual Sugar vs. Quality")
st.pyplot(fig)

df_combined[["alcohol", "residual sugar", "quality"]].corr()

st.markdown("**The scatter plot and correlation analysis show that alcohol content has a positive correlation with wine quality. This means that, generally, wines with higher alcohol levels tend to be rated higher in quality. On the other hand, residual sugar does not show a clear relationship with wine quality. The correlation is very weak, and the scatter plot shows no clear pattern. In conclusion, alcohol content appears to influence quality more than sugar does – especially in red wines.**")