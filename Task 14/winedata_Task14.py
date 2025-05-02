import pandas as pd
import os
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# === Load Data ===
current_dir = os.path.dirname(__file__)
data_dir = current_dir

# Load Excel files
red_wine = pd.read_excel(os.path.join(data_dir, "winequality-red.xlsx"), header=1)
white_wine = pd.read_excel(os.path.join(data_dir, "winequality-white.xlsx"), header=1)

# Add categorical label
red_wine['wine_type'] = 'red'
white_wine['wine_type'] = 'white'

# Combine datasets
combined_wine = pd.concat([red_wine, white_wine], ignore_index=True)

# Encode categorical column
combined_wine['wine_type_encoded'] = combined_wine['wine_type'].map({'red': 0, 'white': 1})

# === Task 13: Apply PCA ===

# Drop non-numeric (non-feature) columns
features = combined_wine.drop(columns=['wine_type'])

# Separate out features and standardize
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Apply PCA (reduce to 2 components for simplicity)
pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_features)

# Create a DataFrame with PCA results
pca_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'])

# Optionally, add wine_type or quality for analysis/plotting
pca_df['wine_type'] = combined_wine['wine_type']
pca_df['quality'] = combined_wine['quality']

# === Task 14: Print 10 random rows ===
print("\n🎲 10 Random Rows from PCA Result:")
print(pca_df.sample(10))
