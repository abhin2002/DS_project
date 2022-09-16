# Data Manipulation
import pandas as pd

# Data Visualisation
import matplotlib.pyplot as plt
#%matplotlib inline

import seaborn as sns

def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    return df

def top_10(df,name):
    # best_selling_prods = pd.DataFrame(df.groupby('Product line').sum()['Quantity'])

    # Sorting the dataframe in descending order
    # best_selling_prods.sort_values(by=['quantity'], inplace=True, ascending=False)
    top=df.groupby(by=["Product line"]).sum()[[name]]
    # Most selling products
    top.sort_values(by=name, inplace=True, ascending=False)
    # print(top[:10])
    return top[:10]


def main():
    df=get_data_from_excel()
    print(top_10(df,'Quantity'))
    

main()