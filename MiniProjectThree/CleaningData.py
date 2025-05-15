import os
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd

# Brug lokal placering af API-nøglen
os.environ['KAGGLE_CONFIG_DIR'] = os.path.join(os.getcwd(), '.kaggle')

# Initialiser API
api = KaggleApi()
api.authenticate()

# Download og udpak datasættet
api.dataset_download_files('pavansubhasht/ibm-hr-analytics-attrition-dataset',
                            path='data', unzip=True)

print("Datasæt hentet og udpakket i 'data/' mappen.")

# Indlæs datasættet
df = pd.read_csv("data/WA_Fn-UseC_-HR-Employee-Attrition.csv")

irrelevante = [
    'EmployeeNumber', 'EmployeeCount', 'StandardHours', 'Over18'
]
df = df.drop(columns=irrelevante)

binære = {
    'Attrition': {'Yes': 1, 'No': 0},
    'Gender':   {'Male': 1, 'Female': 0},
    'OverTime': {'Yes': 1, 'No': 0}
}

for kol, mapping in binære.items():
    df[kol] = df[kol].map(mapping)

kategoriske = [
    'BusinessTravel', 'Department', 'EducationField',
    'JobRole', 'MaritalStatus'
]

df = pd.get_dummies(df, columns=kategoriske, drop_first=True)


# Tjek at der ikke er nulls
print(df.isnull().sum().sort_values(ascending=False).head())


df.to_csv('MiniProjectThree/data/attrition_clean.csv', index=False)
print("Renset datasæt gemt som data/attrition_clean.csv")

