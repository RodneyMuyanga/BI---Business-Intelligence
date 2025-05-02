import pandas as pd
import streamlit as st
import plotly.express as px

class miniproject2Teodora:
    def __init__(self, red_path, white_path):
        self.red_path = red_path
        self.white_path = white_path
        self.df_red = pd.read_excel(self.red_path, skiprows=1)
        self.df_white = pd.read_excel(self.white_path, skiprows=1)

        self.df_red.columns = self.df_red.columns.str.strip().str.replace(' ', '_').str.lower()
        self.df_white.columns = self.df_white.columns.str.strip().str.replace(' ', '_').str.lower()
        self.df_red['wine_type'] = 'red'
        self.df_white['wine_type'] = 'white'

        self.df = pd.concat([self.df_red, self.df_white], ignore_index=True)

    def binning_ph(self, bins=5):
        if 'ph' in self.df.columns:
            self.df['ph_bin'] = pd.cut(self.df['ph'], bins=bins)

    def pH_density_subset(self, bins=5):
        if 'ph_bin' not in self.df.columns:
            self.binning_ph(bins)
        density = self.df.groupby('ph_bin').size() / len(self.df)
        highest_density_bin = density.idxmax()
        highest_density_value = density.max()
        st.write(f"The pH bin with the highest density (using {bins} bins) is **{highest_density_bin}** with a density of **{highest_density_value:.4f}**")
        st.dataframe(density.reset_index(name='density'))

    def explore_quality_factors(self):
        st.write("### Question: What is the relationship between pH and wine quality?")
        st.write("This analysis explores how the pH level of wine affects its quality rating. It provides insights into whether lower or higher pH values tend to correlate with higher wine quality.")
        st.write("#### Why is this important for wine drinkers and distributors?")
        st.write("Wine drinkers may care about the pH because it affects taste, texture, and acidity, influencing the overall drinking experience. For distributors, understanding pH levels can help in identifying wines that have a more favorable balance of acidity, which could affect consumer preferences and marketability.")
        st.write("## pH vs Quality")
        st.dataframe(self.df[['ph', 'quality', 'wine_type']])

        st.write("### pH Correlation with Quality:")
        pH_corr = self.df[['ph', 'quality']].corr()
        st.write(pH_corr)

        fig1 = px.scatter(self.df, x='ph', y='quality', color='wine_type', title="pH vs Quality")
        fig1.update_traces(marker=dict(size=10, opacity=0.7, line=dict(width=0.5, color='black')))
        st.plotly_chart(fig1)

    def explore_alcohol_quality(self):
        st.write("### Question: How does alcohol content affect wine quality?")
        st.write("This analysis investigates the impact of alcohol content on the quality of wine. It reveals whether wines with higher alcohol content tend to be rated better.")
        st.write("#### Why is this important for wine drinkers and distributors?")
        st.write("Wine drinkers may find that alcohol content affects not only the strength but also the taste of wine. Distributors could use this information to target certain alcohol ranges to specific consumer preferences or regions, optimizing their sales strategy.")
        st.write("## Alcohol vs Quality")
        st.dataframe(self.df[['alcohol', 'quality', 'wine_type']])

        st.write("### Alcohol Correlation with Quality:")
        alcohol_corr = self.df[['alcohol', 'quality']].corr()
        st.write(alcohol_corr)

        fig2 = px.scatter(self.df, x='alcohol', y='quality', color='wine_type', title="Alcohol vs Quality")
        fig2.update_traces(marker=dict(size=10, opacity=0.7, line=dict(width=0.5, color='black')))
        st.plotly_chart(fig2)

    def explore_volatile_acidity_quality(self):
        st.write("### Question: What is the effect of volatile acidity on wine quality?")
        st.write("This analysis explores the relationship between volatile acidity levels in wine and its quality. It helps to understand whether higher levels of volatile acidity lead to lower quality ratings.")
        st.write("#### Why is this important for wine drinkers and distributors?")
        st.write("Volatile acidity can impact the taste of wine, potentially making it unpleasant. Wine drinkers may wish to avoid wines with high volatile acidity. Distributors could use this analysis to identify wines with lower volatile acidity that could appeal to a broader customer base.")
        st.write("## Volatile Acidity vs Quality")
        st.dataframe(self.df[['volatile_acidity', 'quality', 'wine_type']])

        st.write("### Volatile Acidity Correlation with Quality:")
        volatile_acidity_corr = self.df[['volatile_acidity', 'quality']].corr()
        st.write(volatile_acidity_corr)

        fig3 = px.scatter(self.df, x='volatile_acidity', y='quality', color='wine_type', title="Volatile Acidity vs Quality")
        fig3.update_traces(marker=dict(size=10, opacity=0.7, line=dict(width=0.5, color='black')))
        st.plotly_chart(fig3)

    def correlation_analysis(self):
        st.write("### Question: What are the correlations between the wine features and wine quality?")
        st.write("This section performs a correlation analysis to identify which features have the strongest relationship with wine quality. It includes separate correlation calculations for red and white wines.")
        st.write("#### Why is this important for wine drinkers and distributors?")
        st.write("Understanding which features (like alcohol, pH, or volatile acidity) most strongly correlate with wine quality can help wine drinkers find wines that suit their taste preferences. Distributors can use this information to select and promote wines that have higher quality ratings based on these key features.")
        
        st.write("## Correlation Analysis with Quality")

        red_df = self.df[self.df['wine_type'] == 'red']
        white_df = self.df[self.df['wine_type'] == 'white']
        
        red_corr = red_df.select_dtypes(include=['float64', 'int64']).corr()['quality'].sort_values(ascending=False)
        st.write("### Red Wine Correlation with Quality:")
        st.write(red_corr)

        white_corr = white_df.select_dtypes(include=['float64', 'int64']).corr()['quality'].sort_values(ascending=False)
        st.write("### White Wine Correlation with Quality:")
        st.write(white_corr)

def main():
    st.title("🍷 Wine Data Analysis")

    red_path = "winequality-red.xlsx"
    white_path = "winequality-white.xlsx"

    wine_analysis = miniproject2Teodora(red_path, white_path)

    st.sidebar.header("Select Analysis (Task 8 & 9)")
    choice = st.sidebar.radio("Choose one:", ["pH Density", "Quality Factors"])

    if choice == "pH Density":
        bins = st.sidebar.slider("Number of bins for pH", 3, 20, 5)
        wine_analysis.pH_density_subset(bins)

    elif choice == "Quality Factors":
        quality_choice = st.sidebar.radio("Select Quality Factor to Explore:", ["pH vs Quality", "Alcohol vs Quality", "Volatile Acidity vs Quality"])
        
        if quality_choice == "pH vs Quality":
            wine_analysis.explore_quality_factors()
        elif quality_choice == "Alcohol vs Quality":
            wine_analysis.explore_alcohol_quality()
        elif quality_choice == "Volatile Acidity vs Quality":
            wine_analysis.explore_volatile_acidity_quality()

    elif choice == "Correlation Analysis":
        wine_analysis.correlation_analysis()

if __name__ == "__main__":
    main()