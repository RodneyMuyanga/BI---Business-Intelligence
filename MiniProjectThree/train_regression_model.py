# train_regression_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Indlæs renset data
df = pd.read_csv("data/attrition_clean.csv")

# Vælg relevante features
X = df[[
    'Age', 'JobLevel', 'TotalWorkingYears', 'YearsAtCompany', 'OverTime',
    'DistanceFromHome', 'Education', 'PerformanceRating', 'EnvironmentSatisfaction'
]]
y = df['MonthlyIncome']

# Split i træning/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Træn model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluer
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f"✅ Model trænet.")
print(f"📈 R²-score: {r2:.2f}")
print(f"📉 Mean Squared Error: {mse:.2f}")

# Udskriv modelens koefficienter
print("\n📊 Feature-koefficienter:")
for feature, coef in zip(X.columns, model.coef_):
    print(f"{feature}: {coef:.2f}")


# Gem model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/income_regression_model.pkl")
print("💾 Model gemt i models/income_regression_model.pkl")
