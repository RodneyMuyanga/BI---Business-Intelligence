import pandas as pd
import matplotlib.pyplot as plt

# Paths to the files
file_stipend = r'C:\skole\4Semester\BI\SU stipendier og lån (mio. kr.).xlsx'
file_antal = r'C:\skole\4Semester\BI\Antal støttemodtagere og låntagere.xlsx'
file_aarsvaerk = r'C:\skole\4Semester\BI\Støtteårsværk.xlsx'

# --- Function to clean and normalize a DataFrame ---
def clean_df(df):
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(r'\n', '', regex=True)
    df.columns = df.columns.str.replace(r'[^\x00-\x7F]+', '', regex=True)  # Remove non-ASCII characters
    df.columns = df.columns.str.replace(' ', '_')
    df.rename(columns={df.columns[0]: 'Aar'}, inplace=True)
    df = df[pd.to_numeric(df['Aar'], errors='coerce').notna()]  # Remove non-numeric year rows
    df['Aar'] = df['Aar'].astype(int)
    return df

# --- Load and clean all Excel files ---
try:
    stipend_df = clean_df(pd.read_excel(file_stipend))
    antal_df = clean_df(pd.read_excel(file_antal))
    aarsvaerk_df = clean_df(pd.read_excel(file_aarsvaerk))
    print("All files loaded and cleaned successfully!")
except Exception as e:
    print(f"Error loading files: {e}")
    exit()

# --- Print column names to confirm ---
print("\nStipend columns:", stipend_df.columns.tolist())
print("Antal columns:", antal_df.columns.tolist())
print("Årsværk columns:", aarsvaerk_df.columns.tolist())

# --- Merge dataframes on 'Aar' ---
merged_df = stipend_df.merge(antal_df, on='Aar').merge(aarsvaerk_df, on='Aar')
print("\nMerged DataFrame:")
print(merged_df.head())

# --- Rename columns to safe names if necessary ---
merged_df.rename(columns={
    'Stipendie_(mio._kr)': 'Stipendie',  # Correcting to match the stipend column name
    'Antal_stttemodtagere': 'Antal_støttemodtagere',  # Adjusted if needed
}, inplace=True)

# --- Recheck final column names ---
print("\nFinal columns:", merged_df.columns.tolist())

# --- Filter data starting from the year 2000 ---
merged_df = merged_df[merged_df['Aar'] >= 2000]

# --- Remove rows with empty (NaN) data in key columns ---
merged_df = merged_df.dropna(subset=['Stipendie', 'Antal_støttemodtagere'])

# --- Calculate SU per student (in actual DKK) ---
try:
    # Calculate total stipend per year (convert from millions to actual DKK)
    merged_df['Total_stipendie'] = merged_df['Stipendie'] * 1_000_000  # Total stipend in DKK

    # Calculate SU per student (in DKK)
    merged_df['SU_pr_student'] = merged_df['Total_stipendie'] / merged_df['Antal_støttemodtagere']
except KeyError as e:
    print(f"\nColumn missing for calculation: {e}")
    print("Please double-check column names above and adjust the rename block accordingly.")
    exit()

# --- Plot ---
plt.figure(figsize=(10, 6))
plt.plot(merged_df['Aar'], merged_df['SU_pr_student'], marker='o', color='teal')
plt.title('Average SU per Student (2000–2024)')
plt.xlabel('Year')
plt.ylabel('SU per Student (DKK)')
plt.grid(True)
plt.tight_layout()
plt.show()
