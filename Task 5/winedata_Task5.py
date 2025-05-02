import pandas as pd
import os

# Find sti
current_dir = os.path.dirname(__file__)
data_dir = current_dir  # Since Excel files are in the same folder

# Indlæs data
red_wine = pd.read_excel(os.path.join(data_dir, "winequality-red.xlsx"), header=1)
white_wine = pd.read_excel(os.path.join(data_dir, "winequality-white.xlsx"), header=1)

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

# 🔁 Transformér kategorisk data til numerisk
combined_wine['wine_type_encoded'] = combined_wine['wine_type'].map({'red': 0, 'white': 1})

# Bekræft encoding
print("\n🔢 Encoded 'wine_type':")
print(combined_wine[['wine_type', 'wine_type_encoded']].drop_duplicates())
