#Personal Expense Tracker Dashboard

#Key Features:
#Upload expense data in CSV format--
#Categorize expenses automatically or manually
#Visualize spending distribution using pie charts
#Monthly expense trend analysis with line charts
#Budget limit alerts and summary insights
#Dark mode toggle
#Multiple file upload support


import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# Login authentication 
user = st.text_input("User Name")
password = st.text_input("Password",type='password')

if st.button("Login"):
    if user == 'admin' and password == '1234':
        st.session_state.logged = True
        st.write("Login Successful")
    else:
        st.write("Invalid Creditials")
        
if 'logged' not in st.session_state:
    st.session_state.logged = False

#logout
if st.session_state.logged:
    if st.button("Logout"):
        st.session_state.logged = False
        st.write("Logged out successfully")
        
if not st.session_state.logged:
    st.stop()

st.set_page_config(page_title='Personal Expense Tracker Dashboard', layout='wide')
st.title('Personal Expense Tracker Dashboard')

upload = st.file_uploader('Upload Expense Data', type=['csv'],accept_multiple_files=True)
if upload:
    all_data = []

    for file in upload:
        df = pd.read_csv(file)
        all_data.append(df)

    df = pd.concat(all_data, ignore_index=True)

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

#Database save for past uploads
    
    conn = sqlite3.connect('expense_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expense_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL
        )
    ''')
    for index, row in df.iterrows():
        c.execute('INSERT INTO expense_data (date, category, amount) VALUES (?, ?, ?)', (row['Date'], row['Category'], row['Amount']))
    conn.commit()
    conn.close()

    #past uploads
    st.subheader("Past Uploads")
    conn = sqlite3.connect('expense_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expense_data")
    past_uploads = c.fetchall()
    conn.close()

    past_uploads_df = pd.DataFrame(past_uploads, columns=['ID', 'Date', 'Category', 'Amount'])
    st.dataframe(past_uploads_df)

