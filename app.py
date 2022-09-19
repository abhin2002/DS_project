import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# from plot import piePlot


st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",  # xcel filename
        engine="openpyxl",
        sheet_name="Sales",  # sheet name
        skiprows=3,  # rows need to skip
        usecols="B:R",
        nrows=1000,  # rows included in my selection
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df


df = get_data_from_excel()
# piePlot(df)

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:", options=df["City"].unique(), default=df["City"].unique()
)

product_line = st.sidebar.multiselect(
    "Select the Product Line:",
    options=df["Product_line"].unique(),
    default=df["Product_line"].unique(),
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:", options=df["Gender"].unique(), default=df["Gender"].unique()
)

insight_product_line = st.sidebar.selectbox(
    "See insights about buyers of this product line:",
    options=df["Product_line"].unique(),
)

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender & Product_line == @product_line"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].sum())  # sum of total column
average_rating = round(
    df_selection["Rating"].mean(), 1
)  # mean of rating column and rounded to one decimal
star_rating = ":star:" * int(
    round(average_rating, 0)
)  # rounding the number to intiger and multiply with * imogi
average_sale_by_transaction = round(
    df_selection["Total"].mean(), 2
)  # mean of total column

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"INR {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"INR {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    df_selection.groupby(by=["Product_line"]).sum()[["Total"]].sort_values(by="Total")
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["yellow"] * len(sales_by_product_line),
    template="plotly_white",
)
# Quantity by product line

quantity_by_product_line = (
    df_selection.groupby(by=["Product_line"])
    .sum()[["Quantity"]]
    .sort_values(by="Quantity")
)
fig_product_quantity = px.bar(
    quantity_by_product_line,
    x=quantity_by_product_line.index,
    y="Quantity",
    # orientation="v",
    title="<b>Quantity by Product Line</b>",
    color_discrete_sequence=["red"] * len(sales_by_product_line),
    template="plotly_white",
)

# fig_product_quantity = px.pie(
#     quantity_by_product_line,
#     value= quantity_by_product_line.index,
#     names= "Quantity"
#     # quantity_by_product_line='Quantity',
#     # Product_line='Product line'

# )
# fig_product_sales.write_html("aku.html")
# fig_product_sales.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", xaxis=(dict(showgrid=False))
)

# making pie chart
# df = px.data.tips()
# fig = px.pie(df, values='tip', names='day')
# fig.show()


# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
# fig_hourly_sales.write_html("abhin.html")
# fig_hourly_sales.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )

# INSIGHTS CHART
invoice_ids = df.query("Product_line == @insight_product_line")["Invoice_ID"].unique()
required_invoices = df.query(
    "Invoice_ID in @invoice_ids & Product_line != @insight_product_line"
)
other_items = (
    required_invoices.groupby(by=["Product_line"])
    .sum()[["Quantity"]]
    .sort_values(by="Quantity", ascending=False)
)
fig_other_items = px.bar(
    other_items,
    x=other_items.index,
    y="Quantity",
    title=f"People who bought {insight_product_line} items also bought: ",
    color_discrete_sequence=["#0083B8"] * len(other_items),
    template="plotly_white",
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_quantity, use_container_width=True)
right_column.plotly_chart(fig_other_items, use_container_width=True)
