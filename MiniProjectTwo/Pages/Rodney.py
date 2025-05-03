import pandas as pd
import os
import streamlit as st

# Find den aktuelle mappe
current_dir = os.path.dirname(os.path.dirname(__file__))

# Definér stier til Excel-filerne
red_wine_path = os.path.join(current_dir, "winequality-red.xlsx")
white_wine_path = os.path.join(current_dir, "winequality-white.xlsx")

# Læs Excel-filerne (husk header=1 hvis kolonnenavne starter i række 2)
red_wine = pd.read_excel(red_wine_path, header=1)
white_wine = pd.read_excel(white_wine_path, header=1)

# Tilføj 'wine_type' kolonne for at identificere typen
red_wine['wine_type'] = 'red'
white_wine['wine_type'] = 'white'

# Saml de to DataFrames til ét samlet DataFrame
combined_wine = pd.concat([red_wine, white_wine], ignore_index=True)

# Print de første 10 rækker af det samlede datasæt
print(combined_wine.head(10))

# Vis form (antal rækker og kolonner)
print("\nSamlet datasæt størrelse:", combined_wine.shape)

# Gem det samlede datasæt som CSV (valgfrit)
combined_wine.to_csv(os.path.join(current_dir, "combined_wine_data.csv"), index=False)
print("\n✅ Data gemt som 'combined_wine_data.csv'")

# Sidebar navigation
st.sidebar.title("Mini Project 2 Navigation")
section = st.sidebar.radio("Go to:", [
    "Task 4 – Descriptive Statistics",
    "Task 7 – Visual Comparison",
    "Task 11 – Outliers",
    "Task 12 – Correlation Filtering"
])

if section == "Task 4 – Descriptive Statistics":
    st.title("Task 4: Explore the features of the three data frames separately. Identify the dependent and the independent variables ")

# Tilføj 'wine_type'
red_wine['wine_type'] = 'red'
white_wine['wine_type'] = 'white'

# Saml data
combined_wine = pd.concat([red_wine, white_wine], ignore_index=True)

# 🔍 Udforsk de tre datasæt hver for sig
print("🔴 Red Wine Info:")
print(red_wine.info())
print("\n📊 Red Wine Stats:")
print(red_wine.describe())

print("\n⚪ White Wine Info:")
print(white_wine.info())
print("\n📊 White Wine Stats:")
print(white_wine.describe())

print("\n🍷 Combined Wine Info:")
print(combined_wine.info())
print("\n📊 Combined Wine Stats:")
print(combined_wine.describe())

# 🎯 Identificer afhængige og uafhængige variable
dependent_var = 'quality'
independent_vars = [col for col in combined_wine.columns if col != 'quality']

print("\n🎯 Dependent Variable:", dependent_var)
print("📊 Independent Variables:", independent_vars)