import plotly.express as px
# This dataframe has 244 lines, but 4 distinct values for `day`
import pandas as pd

def piePlot(df):
    df_selection = df.query(
        "City == @city & Customer_type ==@customer_type & Gender == @gender & Product_line==@product"
    )

    ratio_by_product_line = (
        df_selection.groupby(by=["Product line"]).sum()[["Gender"]].sort_values(by="Gender")
    )
    fig_product_quantity = px.bar(
        ratio_by_product_line,
        x=ratio_by_product_line.index,
        y="Gender Ratio",
        #orientation="v",
        title="<b>Gender Ratio</b>",
        color_discrete_sequence=["red"] * len(ratio_by_product_line),
        template="plotly_white",
    )
    fig_product_quantity.show()
