import pandas as pd
import os

# Find den aktuelle mappe
current_dir = os.path.dirname(__file__)

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
