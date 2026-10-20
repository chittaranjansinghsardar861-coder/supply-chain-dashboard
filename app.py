import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Supply Chain Profitability Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("DataCoSupplyChainDataset_small.csv", encoding="ISO-8859-1")
    df['Profit Margin (%)'] = (df['Order Profit Per Order'] / df['Sales']) * 100
    return df

df = load_data()

st.sidebar.header("Filters")
market = st.sidebar.multiselect("Select Market", options=df['Market'].unique(), default=df['Market'].unique())
segment = st.sidebar.multiselect("Select Segment", options=df['Customer Segment'].unique(), default=df['Customer Segment'].unique())

filtered_df = df[(df['Market'].isin(market)) & (df['Customer Segment'].isin(segment))]

st.title("Supply Chain Profitability Performance Analysis")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${filtered_df['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${filtered_df['Order Profit Per Order'].sum():,.2f}")
col3.metric("Avg Profit Margin", f"{filtered_df['Profit Margin (%)'].mean():.2f}%")
col4.metric("Total Orders", f"{len(filtered_df):,}")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["Revenue & Profit", "Customer Value", "Product Performance", "Discount Analyzer"])

with tab1:
    st.subheader("Revenue & Profit by Market")
    m_agg = filtered_df.groupby('Market')[['Sales', 'Order Profit Per Order']].sum().reset_index()
    fig = px.bar(m_agg, x='Market', y=['Sales', 'Order Profit Per Order'], barmode='group')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Top Customers by Profit")
    top_c = filtered_df.groupby(['Customer Fname', 'Customer Lname'])['Order Profit Per Order'].sum().reset_index().sort_values(by='Order Profit Per Order', ascending=False).head(10)
    st.dataframe(top_c, use_container_width=True)

with tab3:
    st.subheader("Category Profit Margins")
    cat_p = filtered_df.groupby('Category Name')['Profit Margin (%)'].mean().reset_index()
    fig2 = px.bar(cat_p, x='Category Name', y='Profit Margin (%)')
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.subheader("Discount vs Profit Margin")
    fig3 = px.scatter(filtered_df.sample(min(1500, len(filtered_df))), x='Order Item Discount Rate', y='Profit Margin (%)', color='Category Name')
    st.plotly_chart(fig3, use_container_width=True)
