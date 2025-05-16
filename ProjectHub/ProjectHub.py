import streamlit as st
import importlib.util
import os

# Find roden til ProjectHub-mappen
project_root = os.path.dirname(__file__)

# === Titanic Projekt ===
titanic_path = os.path.abspath(
    os.path.join(project_root, "..", "BI-Tasks", "FLOW 1", "Programming Exercises", "Titanic", "Titanic_App.py")
)

print(f"Titanic path being used: {titanic_path}")  # Debug print

spec_titanic = importlib.util.spec_from_file_location("Titanic_App", titanic_path)
titanic_module = importlib.util.module_from_spec(spec_titanic)
spec_titanic.loader.exec_module(titanic_module)
run_titanic = titanic_module.run_titanic

# === MiniProject 1 ===
mini1_path = os.path.abspath(
    os.path.join(project_root, "..", "BI-Tasks", "MiniProjects", "MiniProjects_1", "MiniProject_1_app.py")
)

print(f"MiniProject 1 path being used: {mini1_path}")  # Debug print

spec_mini1 = importlib.util.spec_from_file_location("MiniProject_1_app", mini1_path)
mini1_module = importlib.util.module_from_spec(spec_mini1)
spec_mini1.loader.exec_module(mini1_module)
run_mini1 = mini1_module.run_mini_project_1

# === Streamlit Layout og Navigation ===
st.set_page_config(page_title="Project Hub", layout="wide")
st.title("📊 Data Project Hub - Business Intelligence 2025")

project = st.sidebar.selectbox("Vælg projekt:", [
    "Titanic Analysis",
    "MINI PROJECT 1: DATA INGESTION AND WRANGLING",
    "🚧 Kommende projekt 2"
])

if project == "Titanic Analysis":
    run_titanic()
elif project == "MINI PROJECT 1: DATA INGESTION AND WRANGLING":
    run_mini1()
else:
    st.info("Dette projekt er endnu ikke klar. Vælg et projekt i sidebaren for at komme i gang.")
