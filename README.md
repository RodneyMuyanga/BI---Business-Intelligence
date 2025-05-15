# BI---Business-Inteligence
📊 Business Intelligence (BI) Project  This repository is dedicated to exploring and implementing Business Intelligence (BI) solutions.
##Purpose

BI turns raw data into insights to support smarter business decisions.
Repo Use

We’ll use this repo to:

    Collect and analyze data

    Build dashboards and reports

    Collaborate on solutions

    Document our work for the teache

Michella:
Food Price Index – Excel Data Analysis
This script loads, transforms, and visualizes consumer price index data from an Excel file. The data contains monthly price indices for various food categories in 2024.

🔍 What the code does:
Reads the Excel file while skipping metadata rows that are not part of the actual dataset.

Cleans the data by removing unnecessary columns and assigning meaningful column names manually.

Transforms the data from wide format (months as columns) to long format (one row per category/month).

Converts months into proper date format for time series analysis.

Ensures numeric values in the index column and removes any missing values.

Displays all available food categories in the dataset.

Filters and plots the price index over time for a selected category (e.g., "01.1.1 Bread and cereals").

Saves the plot as a PNG image file for further use or documentation.

This script is part of a larger project where data from multiple sources (Excel, CSV, JSON) will be collected, cleaned, and visualized.

Teodora:
This project analyzes SU data in Denmark from the year 2000 and onward. It combines information from three Excel files, covering total stipends, number of recipients, and support-year equivalents.
The script cleans and merges the data, calculates the average SU amount per student each year, and visualizes the results in a line chart. The final chart shows how SU support has changed over time.

Sandra - Husleje Data:
Diagrammet viser udviklingen i huslejeindekset for fire danske regioner i løbet af 2024.
Indekset tager udgangspunkt i 2021 = 100, og vi ser en jævn stigning i alle regioner — især i Region Hovedstaden.
Dataene er baseret på de officielle kvartalstal fra Danmarks Statistik.
Visualiseringen gør det nemt at sammenligne udviklingen og se hvor huslejen stiger mest og hvor meget den er steget.

# MINI PROJECT 3: MACHINE LEARNING FOR ANALYSIS AND PREDICTION  
## Which machine learning methods did you choose to apply in the application and why? 
### Supervised Machine Learning: Salary Prediction (Linear Regression)
We applied linear regression to predict the monthly income of employees. Linear regression was chosen because it is a simple and interpretable supervised learning method that allows us to analyze the relationship between employee attributes and salary. The method was also explicitly required by the assignment.

### Employee Attrition Analysis:
We chose a Decision Tree classifier for predicting employee attrition. Decision Trees are intuitive and easy to interpret, making them suitable for explaining which employee features influence attrition. The model also handles both numerical and categorical data well and provides visualizations that help understand feature importance.

## How accurate is your solution of prediction? Explain the meaning of the quality measures. 
### Supervised Machine Learning: Salary Prediction (Linear Regression)
The linear regression model achieved an R²-score of 0.89, meaning it explained 89% of the variance in income in the dataset. The Mean Squared Error (MSE) was approximately 2.3 million (in dataset units).

R² (coefficient of determination) shows how much of the variance in salary can be explained by the model’s input features. A score of 0.89 is considered strong.

Mean Squared Error (MSE) is the average of the squared differences between the actual and predicted values. A lower MSE means the model is more accurate.

### Decision Tree
The Decision Tree model achieved an accuracy of 81.18%, indicating it correctly predicts attrition status for about 81 out of 100 employees.

However, due to class imbalance (more employees stay than leave), accuracy alone is insufficient. Looking at class-specific metrics:

Precision (attrition = Yes): 0.35 — Among employees predicted to leave, 35% were actually leaving.

Recall (attrition = Yes): 0.43 — The model correctly identified 43% of all employees who actually left.

This shows the model detects some true attritions but misses many (false negatives) and sometimes falsely predicts attrition (false positives).

## Which are the most decisive factors for quitting a job? Why do people quit their job? 
### Supervised Machine Learning: Salary Prediction (Linear Regression)
The linear model sometimes gave unrealistically low salary predictions, especially for experienced profiles. This may be due to linear regression’s limitations in capturing non-linear relationships and overlapping features (e.g., age and total working years). A more advanced model like Random Forest Regressor could offer better results. Additionally, normalizing input values and selecting more relevant features might improve accuracy.

### Attrition
The top three factors influencing attrition, based on feature importance in the decision tree, are:

OverTime_Yes (importance: 0.218): Employees working overtime are more likely to leave, suggesting work-life imbalance is a key reason.

MonthlyIncome (importance: 0.203): Lower income correlates with higher attrition, indicating dissatisfaction with pay affects quitting decisions.

TotalWorkingYears (importance: 0.107): Employees with fewer total working years tend to leave more, showing that less experienced staff may be less committed or seeking better opportunities.

These indicate that workload, compensation, and experience are the main drivers of attrition in this dataset.

## What could be done for further improvement of the accuracy of the models? 

Apply more advanced algorithms such as Random Forests or Gradient Boosting, which typically improve predictive power.

Use oversampling techniques like SMOTE to balance the dataset and help the model learn minority class patterns better.

Perform hyperparameter tuning and cross-validation to optimize model complexity and avoid overfitting.

Engineer new features capturing employee engagement, satisfaction, or external market factors.

Collect more data on managerial support, work environment, or employee sentiment for richer analysis.

## Which work positions and departments are in higher risk of losing employees?
### Attricion
From the correlation analysis:

Positions such as Sales Representatives and Laboratory Technicians have positive correlation with attrition, indicating higher risk.

The Sales Department shows a positive correlation with attrition, suggesting employees here are more likely to quit compared to Research & Development or other departments.

## Are employees of different gender paid equally in all departments? 

## Do the family status and the distance from work influence the work-life balance? 

## Does education make people happy (satisfied from the work)? 

## Which were the challenges in the project development? 
### Supervised Machine Learning: Salary Prediction (Linear Regression)
One challenge was understanding why some variables had negative coefficients, even when they intuitively seemed to have a positive impact on salary. This was caused by feature overlap (e.g., age and experience) confusing the linear model. Another challenge was that model performance metrics like R² looked good, while the real-life predictions didn’t always make sense. To address this, we added visualizations (scatterplots, boxplots, correlation heatmaps) to help interpret the data more clearly.

Note: The salary predictions are based on a synthetic dataset from IBM, and values are not linked to any real currency. Units are relative and only used for analysis purposes.

