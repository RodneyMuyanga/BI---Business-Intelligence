import pandas as pd
import matplotlib.pyplot as plt

# paths 
file_stipend = 'data/SU stipendier og lån (mio. kr.).xlsx'
file_antal = 'data/Antal støttemodtagere og låntagere.xlsx'
file_aarsvaerk = 'data/Støtteårsværk.xlsx'

# function to clean and normalize a dataframe
def clean_df(df):
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(r'\n', '', regex=True)
    df.columns = df.columns.str.replace(r'[^\x00-\x7F]+', '', regex=True)  # remove non-ASCII characters
    df.columns = df.columns.str.replace(' ', '_')
    df.rename(columns={df.columns[0]: 'Aar'}, inplace=True)
    df = df[pd.to_numeric(df['Aar'], errors='coerce').notna()]  # remove non numeric year rows
    df['Aar'] = df['Aar'].astype(int)
    return df

# load and clean all excel
try:
    stipend_df = clean_df(pd.read_excel(file_stipend))
    antal_df = clean_df(pd.read_excel(file_antal))
    aarsvaerk_df = clean_df(pd.read_excel(file_aarsvaerk))
    print("All files loaded and cleaned successfully!")
except Exception as e:
    print(f"Error loading files: {e}")
    exit()

# print column names 
print("\nStipend columns:", stipend_df.columns.tolist())
print("Antal columns:", antal_df.columns.tolist())
print("Årsværk columns:", aarsvaerk_df.columns.tolist())

# merge dataframes on 'Aar' 
merged_df = stipend_df.merge(antal_df, on='Aar').merge(aarsvaerk_df, on='Aar')
print("\nMerged DataFrame:")
print(merged_df.head())

# rename columns 
merged_df.rename(columns={
    'Stipendie_(mio._kr)': 'Stipendie',  
    'Antal_stttemodtagere': 'Antal_støttemodtagere',  
}, inplace=True)

# check final column names 
print("\nFinal columns:", merged_df.columns.tolist())

# filter data starting year 2000
merged_df = merged_df[merged_df['Aar'] >= 2000]

# remove empty rows
merged_df = merged_df.dropna(subset=['Stipendie', 'Antal_støttemodtagere'])

# calculate su per student
try:
    # Calculate total per year
    merged_df['Total_stipendie'] = merged_df['Stipendie'] * 1_000_000  

    # Calculate SU per student 
    merged_df['SU_pr_student'] = merged_df['Total_stipendie'] / merged_df['Antal_støttemodtagere']
except KeyError as e:
    print(f"\nColumn missing for calculation: {e}")
    print("Please double-check column names above and adjust the rename block accordingly.")
    exit()

# Plot
plt.figure(figsize=(10, 6))
plt.plot(merged_df['Aar'], merged_df['SU_pr_student'], marker='o', color='teal')
plt.title('Average SU per Student (2000–2024)')
plt.xlabel('Year')
plt.ylabel('SU per Student (DKK)')
plt.grid(True)
plt.tight_layout()
plt.show()
