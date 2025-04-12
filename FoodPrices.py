import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

foodIndex = r"C:\Dokumenter\Datamatiker\DAT4\BI\Eksamens Projekt\FoodPricesIndex2024.xlsx"

# 1. Read Excel – skip metadata
df = pd.read_excel(foodIndex, skiprows=3, header=None)

# 2. Remove column 0 (Index)
df = df.iloc[:, 1:]

# 3. Set the columns manually
monthscolumns = ["2024M01", "2024M02", "2024M03", "2024M04", "2024M05",
                  "2024M06", "2024M07", "2024M08", "2024M09", "2024M10",
                  "2024M11", "2024M12"]
df.columns = ["Category"] + monthscolumns

# 4. Melt data
df_melted = df.melt(id_vars=["Category"], var_name="Month", value_name="Index")

# 5. Convert dates and clean up
df_melted['Month'] = pd.to_datetime(df_melted['Month'], format="%YM%m", errors="coerce")
df_melted['Index'] = pd.to_numeric(df_melted['Index'], errors='coerce')
df_melted = df_melted.dropna(subset=["Month", "Index"])

# 6. Show categories 
print("\nAvailable categories:")
print(df_melted['Category'].unique())

# 7. Plot
category = "01.1.1 Bread and cereals"
subset = df_melted[df_melted['Category'] == category]

plt.figure(figsize=(10,6))
sns.lineplot(data=subset, x='Month', y='Index')
plt.title(f"Price index over time for: {category}")
plt.xlabel("Month")
plt.ylabel("Index (2015=100)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig(f"price_index_{category.replace(' ', '_').replace('.', '')}.png")
plt.show()

