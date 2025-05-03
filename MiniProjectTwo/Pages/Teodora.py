import pandas as pd
import streamlit as st
import plotly.express as px

# Class for handling wine data analysis
class WineAnalysis:
    def __init__(self, red_path, white_path):
        """
        loading red and white wine data, cleaning, and combining them.
        """
        self.red_path = red_path
        self.white_path = white_path
        
        # Load data
        self.df_red = pd.read_excel(self.red_path, skiprows=1)
        self.df_white = pd.read_excel(self.white_path, skiprows=1)
        
        # Clean column names and merge datasets
        self.df_red.columns = self.df_red.columns.str.strip().str.replace(' ', '_').str.lower()
        self.df_white.columns = self.df_white.columns.str.strip().str.replace(' ', '_').str.lower()
        
        # Add wine type column to differentiate red and white wines
        self.df_red['wine_type'] = 'red'
        self.df_white['wine_type'] = 'white'
        
        # Combine the datasets
        self.df = pd.concat([self.df_red, self.df_white], ignore_index=True)
    
    # ---- Data Binning ----
    def binning_ph(self, bins=5):
        """
        Bins the pH values into specified categories for further analysis.
        """
        if 'ph' in self.df.columns:
            self.df['ph_bin'] = pd.cut(self.df['ph'], bins=bins)

    def pH_density_subset(self, bins=5):
        """
        Displays the pH density distribution and identifies the pH bin with the highest density.
        """
        if 'ph_bin' not in self.df.columns:
            self.binning_ph(bins)
        
        # Calculate the density for each pH bin
        density = self.df.groupby('ph_bin').size() / len(self.df)
        
        # Identify the bin with the highest density
        highest_density_bin = density.idxmax()
        highest_density_value = density.max()
        
        # Display results
        st.write(f"The pH bin with the highest density (using {bins} bins) is **{highest_density_bin}** with a density of **{highest_density_value:.4f}**")
        st.dataframe(density.reset_index(name='density'))
    
    # ---- Wine Quality Analysis ----
    def explore_quality_factors(self):
        """
        Explores the relationship between pH and wine quality, including visualizations and insights for both red and white wines.
        """
        st.write("### Question: What is the relationship between pH and wine quality?")
        st.write("This analysis explores how the pH level of wine affects its quality rating.")
        st.write("## pH vs Quality")
        
        # Display data
        st.dataframe(self.df[['ph', 'quality', 'wine_type']])
        
        # Display correlation between pH and Quality
        pH_corr = self.df[['ph', 'quality']].corr()
        st.write(pH_corr)
        
        # pH vs Quality Scatter Plot
        fig1 = px.scatter(self.df, x='ph', y='quality', color='wine_type', title="pH vs Quality")
        fig1.update_traces(marker=dict(size=10, opacity=0.7, line=dict(width=0.5, color='black')))
        st.plotly_chart(fig1)
        
        # Optimal pH for red and white wines
        self._optimal_ph_for_quality()

    def _optimal_ph_for_quality(self):
        """
        Identifies and displays the optimal pH levels for red and white wines for the highest quality.
        """
        optimal_ph_red = self.df[self.df['wine_type'] == 'red'].groupby('ph').agg({'quality': 'mean'}).reset_index()
        optimal_ph_red = optimal_ph_red.sort_values('quality', ascending=False).iloc[0]
        st.write(f"The optimal pH level for red wine with the highest quality is **{optimal_ph_red['ph']:.2f}** with an average quality score of **{optimal_ph_red['quality']:.2f}**.")
        
        optimal_ph_white = self.df[self.df['wine_type'] == 'white'].groupby('ph').agg({'quality': 'mean'}).reset_index()
        optimal_ph_white = optimal_ph_white.sort_values('quality', ascending=False).iloc[0]
        st.write(f"The optimal pH level for white wine with the highest quality is **{optimal_ph_white['ph']:.2f}** with an average quality score of **{optimal_ph_white['quality']:.2f}**.")

    def explore_alcohol_quality(self):
        """
        Analyzes the effect of alcohol content on wine quality with visualizations and insights for both red and white wines.
        """
        st.write("### Question: How does alcohol content affect wine quality?")
        st.write("This analysis investigates the impact of alcohol content on the quality of wine.")
        st.write("## Alcohol vs Quality")
        
        # Display data
        st.dataframe(self.df[['alcohol', 'quality', 'wine_type']])
        
        # Display correlation between Alcohol and Quality
        alcohol_corr = self.df[['alcohol', 'quality']].corr()
        st.write(alcohol_corr)
        
        # Alcohol vs Quality Scatter Plot
        fig2 = px.scatter(self.df, x='alcohol', y='quality', color='wine_type', title="Alcohol vs Quality")
        fig2.update_traces(marker=dict(size=10, opacity=0.7, line=dict(width=0.5, color='black')))
        st.plotly_chart(fig2)
        
        # Optimal Alcohol content for red and white wines
        self._optimal_alcohol_for_quality()

    def _optimal_alcohol_for_quality(self):
        """
        Identifies and displays the optimal alcohol content for red and white wines for the highest quality.
        """
        optimal_alcohol_red = self.df[self.df['wine_type'] == 'red'].groupby('alcohol').agg({'quality': 'mean'}).reset_index()
        optimal_alcohol_red = optimal_alcohol_red.sort_values('quality', ascending=False).iloc[0]
        st.write(f"The optimal alcohol content for red wine with the highest quality is **{optimal_alcohol_red['alcohol']:.2f}**% with an average quality score of **{optimal_alcohol_red['quality']:.2f}**.")
        
        optimal_alcohol_white = self.df[self.df['wine_type'] == 'white'].groupby('alcohol').agg({'quality': 'mean'}).reset_index()
        optimal_alcohol_white = optimal_alcohol_white.sort_values('quality', ascending=False).iloc[0]
        st.write(f"The optimal alcohol content for white wine with the highest quality is **{optimal_alcohol_white['alcohol']:.2f}**% with an average quality score of **{optimal_alcohol_white['quality']:.2f}**.")

    def explore_volatile_acidity_quality(self):
        """
        Investigates the impact of volatile acidity on wine quality with visualizations and insights for both red and white wines.
        """
        st.write("### Question: What is the effect of volatile acidity on wine quality?")
        st.write("This analysis explores the relationship between volatile acidity levels in wine and its quality.")
        st.write("## Volatile Acidity vs Quality")
        
        # Display data
        st.dataframe(self.df[['volatile_acidity', 'quality', 'wine_type']])
        
        # Display correlation between Volatile Acidity and Quality
        volatile_acidity_corr = self.df[['volatile_acidity', 'quality']].corr()
        st.write(volatile_acidity_corr)
        
        # Volatile Acidity vs Quality Scatter Plot
        fig3 = px.scatter(self.df, x='volatile_acidity', y='quality', color='wine_type', title="Volatile Acidity vs Quality")
        fig3.update_traces(marker=dict(size=10, opacity=0.7, line=dict(width=0.5, color='black')))
        st.plotly_chart(fig3)
        
        # Optimal Volatile Acidity for red and white wines
        self._optimal_acidity_for_quality()

    def _optimal_acidity_for_quality(self):
        """
        Identifies and displays the optimal volatile acidity levels for red and white wines for the highest quality.
        """
        optimal_acidity_red = self.df[self.df['wine_type'] == 'red'].groupby('volatile_acidity').agg({'quality': 'mean'}).reset_index()
        optimal_acidity_red = optimal_acidity_red.sort_values('quality', ascending=False).iloc[0]
        st.write(f"The optimal volatile acidity level for red wine with the highest quality is **{optimal_acidity_red['volatile_acidity']:.2f}** with an average quality score of **{optimal_acidity_red['quality']:.2f}**.")
        
        optimal_acidity_white = self.df[self.df['wine_type'] == 'white'].groupby('volatile_acidity').agg({'quality': 'mean'}).reset_index()
        optimal_acidity_white = optimal_acidity_white.sort_values('quality', ascending=False).iloc[0]
        st.write(f"The optimal volatile acidity level for white wine with the highest quality is **{optimal_acidity_white['volatile_acidity']:.2f}** with an average quality score of **{optimal_acidity_white['quality']:.2f}**.")
    
    def wine_quality_education(self):
        """
        Provides educational resources on wine quality, including a video and a Wikipedia link.
        """
        st.header("📚 Wine Quality Education")
        st.subheader("🎬 Learn About Wine Quality")
        st.video("https://www.youtube.com/watch?v=nJQJHOtT96s")
        st.subheader("📖 Read More on Wikipedia")
        st.markdown("""For a deeper understanding of wine quality—including the role of acidity, alcohol, and other factors—visit this [Wikipedia article on Wine Faults and Flaws](https://en.wikipedia.org/wiki/Wine_fault).""")

# ---- Main ---
def main():
    st.title("🍷 Wine Data Analysis")
    red_path = "winequality-red.xlsx"
    white_path = "winequality-white.xlsx"
    wine_analysis = WineAnalysis(red_path, white_path)
    
    # Sidebar 
    st.sidebar.header("Select Analysis (Task 8, 9 & 16)")
    choice = st.sidebar.radio("Choose one:", [
        "pH Density",
        "Quality Factors",
        "Wine Quality Education"
    ])
    
    if choice == "pH Density":
        bins = st.sidebar.slider("Number of bins for pH", 3, 20, 5)
        wine_analysis.pH_density_subset(bins)
    elif choice == "Quality Factors":
        quality_choice = st.sidebar.radio("Select Quality Factor to Explore:", [
            "pH vs Quality",
            "Alcohol vs Quality",
            "Volatile Acidity vs Quality"
        ])
        if quality_choice == "pH vs Quality":
            wine_analysis.explore_quality_factors()
        elif quality_choice == "Alcohol vs Quality":
            wine_analysis.explore_alcohol_quality()
        elif quality_choice == "Volatile Acidity vs Quality":
            wine_analysis.explore_volatile_acidity_quality()
    elif choice == "Wine Quality Education":
        wine_analysis.wine_quality_education()

if __name__ == "__main__":
    main()
