import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


# Vis alle kolonner i terminalen
pd.set_option('display.max_columns', None)

def load_and_clean_wine_data():
    try:
        red_df = pd.read_excel("winequality-red.xlsx", header=1)
        white_df = pd.read_excel("winequality-white.xlsx", header=1)

        red_df["wine_type"] = "red"
        white_df["wine_type"] = "white"

        red_df = red_df.loc[:, ~red_df.columns.str.contains("^Unnamed")]
        white_df = white_df.loc[:, ~white_df.columns.str.contains("^Unnamed")]

        red_df = red_df.dropna()
        white_df = white_df.dropna()

        return red_df, white_df

    except Exception as e:
        print(f"Fejl under indlæsning: {e}")
        return None, None
    
def show_correlation_heatmap(df):
    st.header("Korrelationsanalyse")
    st.write("Herunder ser du en heatmap over korrelationerne mellem alle numeriske attributter.")

    # Fjerner ikke-numeriske kolonner
    numeric_df = df.select_dtypes(include=['float64', 'int64'])

    # Beregner korrelation
    corr = numeric_df.corr()

    # Laver heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    quality_corr = corr["quality"].sort_values(ascending=False)
    st.subheader("Attributter mest korreleret med kvalitet:")
    st.write(quality_corr)

def main():
    st.title("Wine Quality Analysis")

    red_df, white_df = load_and_clean_wine_data()
    if red_df is not None and white_df is not None:
        # Kombiner data
        combined_df = pd.concat([red_df, white_df], ignore_index=True)

        st.success("✅ Data indlæst og kombineret!")
        st.dataframe(combined_df)

        # Vis heatmap
        show_correlation_heatmap(combined_df)

if __name__ == "__main__":
    main()


# TEST
#if __name__ == "__main__":
 #   red_df, white_df = load_and_clean_wine_data()

  #  if red_df is not None and white_df is not None:
   #     print("\n🍷 Første 5 rækker af rødvin:\n", red_df.head())
    #    print("\n🥂 Første 5 rækker af hvidvin:\n", white_df.head())
#
 #               # Opgave 3: Kombinér data
   #     combined_df = pd.concat([red_df, white_df], ignore_index=True)
  #      print("\n Kombineret dataframe (første 5 rækker):\n", combined_df.head())
    #    print("\n Antal rækker i alt:", len(combined_df))
     #   print(" Fordeling af vintyper:\n", combined_df["wine_type"].value_counts())
