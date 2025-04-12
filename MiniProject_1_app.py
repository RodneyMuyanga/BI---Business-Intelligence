import streamlit as st
import matplotlib.pyplot as plt
import os
import re

# Kør fra ProjectHub
def run_mini_project_1():
    st.title("📁 MINI PROJECT 1: DATA VISUALIZATION FOCUS")

    folder = os.path.join("MiniProjects", "MiniProjects_1", "Txt filer")
    git checkout -b Rodney-Løn origin/Rodney-Løn
        st.error(f"Mappen '{folder}' blev ikke fundet.")
        return

    txt_files = [f for f in os.listdir(folder) if f.endswith(".txt")]
    if not txt_files:
        st.warning("Ingen .txt-filer fundet i mappen.")
        return

    selected_file = st.sidebar.selectbox("📄 Vælg tekstfil til analyse:", txt_files)

    file_path = os.path.join(folder, selected_file)
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    st.markdown(f"### 📝 Indhold af: **{selected_file}**")
    st.text_area("Rå tekst fra fil:", content, height=180)

    # Parser
    def parse_data(txt):
        data = {}
        lines = txt.splitlines()
        for i in range(len(lines) - 1):
            key_line = lines[i].strip()
            value_line = lines[i + 1].strip()

            if re.search(r'\d', value_line):
                key = key_line
                value = value_line.replace(".", "").replace(",", ".")
                match = re.search(r'(\d+(?:\.\d+)?)', value)
                if match:
                    data[key] = float(match.group(1))
        return data

    data_dict = parse_data(content)

    if not data_dict:
        st.info("Ingen numeriske data fundet i denne fil.")
        return

    # Viser valgt datakontekst
    st.markdown("### 📊 Visualisering af parse'de data")

    # Automatisk diagramvalg
    fig, ax = plt.subplots(figsize=(6, 4))

    if "køn" in selected_file.lower():
        # Bar chart for løn pr. køn
        ax.bar(data_dict.keys(), data_dict.values(), color=["#62aaff", "#ff6289"])
        ax.set_ylabel("Løn (kr.)")
        ax.set_title("Gennemsnitsløn fordelt på køn")
        for i, v in enumerate(data_dict.values()):
            ax.text(i, v + 500, f"{v:,.0f} kr", ha='center')
        st.pyplot(fig)
        st.markdown("✅ **Denne graf viser den gennemsnitlige løn fordelt på køn.**")

    elif "65 jobs" in selected_file.lower():
        # Pie chart for top 6 jobs
        top_jobs = dict(sorted(data_dict.items(), key=lambda x: x[1], reverse=True)[:6])
        ax.pie(top_jobs.values(), labels=top_jobs.keys(), autopct="%1.1f%%", startangle=90)
        ax.set_title("Top 6 jobs efter løn")
        st.pyplot(fig)
        st.markdown("✅ **Cirkeldiagrammet viser de 6 bedst betalte jobs og deres andel af topniveau-lønninger.**")

    elif "aldersgrupper" in selected_file.lower():
        # Line plot for alder
        labels = list(data_dict.keys())
        values = list(data_dict.values())
        ax.plot(labels, values, marker='o', linestyle='-', color="green")
        ax.set_title("Gennemsnitsløn fordelt på aldersgrupper")
        ax.set_ylabel("Løn i kr.")
        ax.set_xlabel("Aldersgrupper")
        ax.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        st.markdown("✅ **Denne graf viser gennemsnitlig timeløn opdelt efter alder.**")

    else:
        # Fallback bar chart
        ax.bar(data_dict.keys(), data_dict.values(), color="skyblue")
        ax.set_title("Visualisering af indlæst data")
        plt.xticks(rotation=45)
        st.pyplot(fig)
