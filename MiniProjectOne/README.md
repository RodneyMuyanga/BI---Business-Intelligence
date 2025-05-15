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


