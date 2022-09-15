import pandas as pd

df=pd.read_excel('sales.xlsx')
df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender"
)
average_rating = round(df_selection["Rating"].mean(), 1)

print(average_rating)