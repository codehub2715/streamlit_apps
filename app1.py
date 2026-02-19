#Personal Expense Tracker Dashboard

#Key Features:
#Upload expense data in CSV format--
#Categorize expenses automatically or manually
#Visualize spending distribution using pie charts
#Monthly expense trend analysis with line charts
#Budget limit alerts and summary insights


import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Personal Expense Tracker Dashboard', layout='wide')
st.title('Personal Expense Tracker Dashboard')

upload = st.file_uploader('Upload Expense Data', type=['csv'])
if upload:
    df = pd.read_csv(upload)
    st.subheader("Expense Data Preview")
    st.dataframe(df)
    
#categorization
    st.subheader("Expense Categories")
    st.write(df.groupby('Category')['Amount'].sum())

    col1, col2 = st.columns(2)
#pie
    with col1:   
        st.subheader("Expense Distribution")
        fig = px.pie(df, values = 'Amount' , names='Category')
        st.plotly_chart(fig,use_container_width=True)
    with col2:
#line
        st.subheader("Monthly Expense Trend")
        fig2 = px.line(df, x='Date',y='Amount', title = 'Monthly Expense Trend')
        st.plotly_chart(fig2,use_container_width=True)

#budget limit
    st.subheader("Budget Limit Alerts")
    budget_limit = st.number_input('Enter your budget limit', min_value=10000.0)

    if df['Amount'].sum() > budget_limit:
        st.warning("You have spent more than your budget limit.")

    st.subheader("Summary")
    st.write(f"Total Expenses: {df['Amount'].sum()}")
    st.write(f"Maximum Expense: {df['Amount'].max()}")
    st.write(f"Minimum Expense: {df['Amount'].min()}")

    