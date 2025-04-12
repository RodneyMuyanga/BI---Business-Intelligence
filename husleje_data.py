import pandas as pd
import matplotlib.pyplot as plt

def loadRentData(filepath):
    try:
        df = pd.read_csv(filepath, encoding='utf-8', header=None)

        df = df.drop(columns=[0, 1])
        df.rename(columns={2: 'Region'}, inplace=True)
        kvartaler = ['2024K1', '2024K2', '2024K3', '2024K4']
        df.columns = ['Region'] + kvartaler

        df.set_index('Region', inplace=True)

       # df.colums = df.columns.str.strip()
        return df
    except Exception as e:
        print(f"Fejl under indlæsning: {e}")
        return None
    
def plotRentData(df):
   
    df.T.plot(marker='o')
    plt.title("Udvikling i huslejeindeks i 2024")
    plt.xlabel("Kvartal")
    plt.ylabel("Indeks (2021 = 100)")
    plt.legend(title="Region")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


#TEST - indlæs fil og vis i konsol
if __name__ == "__main__":
    rent_data = loadRentData("Huslejeindeks_2024.csv")
    if rent_data is not None:
        print("\n✅ Renset husleje-data:\n")
        print(rent_data)

        plotRentData(rent_data)