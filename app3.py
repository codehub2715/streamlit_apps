#Inventory Management System

#Key Features:
#Add, update, and delete products
#Stock quantity tracking
#Low-stock alerts
#Sales entry system
#Inventory summary dashboard


import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

conn = sqlite3.connect("inventory.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    price REAL,
    quantity INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    quantity_sold INTEGER,
    total_price REAL,
    sale_date TEXT
)
""")

conn.commit()

#sidebar
st.set_page_config(page_title="Inventory Management System", layout="wide")
st.title("Inventory Management System")

menu = st.sidebar.selectbox("Select Option", [
    "Manage Products",
    "Sales Entry",
    "View Sales",
    "Dashboard"
])

#Manage products - add ,update, delete

if menu == "Manage Products":
    #add
    st.subheader("Add New Product")

    name = st.text_input("Product Name")
    category = st.text_input("Category")
    price = st.number_input("Price", min_value=0.0)
    quantity = st.number_input("Quantity", min_value=0)

    if st.button("Add Product"):
        cursor.execute("""
        INSERT INTO products (name, category, price, quantity)
        VALUES (?, ?, ?, ?)
        """, (name, category, price, quantity))
        conn.commit()
        st.success("Product Added Successfully!")
    
    #update
    st.subheader("Update Product")

    update_id = st.number_input("Enter Product ID to Update", min_value = 1, key="update_id")
    update_name = st.text_input("Product Name",key = "update_name")
    update_category = st.text_input("Category", key="update_category")
    update_price = st.number_input("Price", min_value=0.0, key="update_price")
    update_quantity = st.number_input("Quantity", min_value=0, key="update_quantity")

    if st.button("Update Product"):
        cursor.execute("""
        UPDATE products SET name=?, category=?, price=?, quantity=? WHERE id=?""",
        (update_name, update_category, update_price, update_quantity, update_id))
        conn.commit()
        st.success("Product Updated Successfully!")
    
    #product list
    st.subheader("Product List")

    products_df = pd.read_sql_query("SELECT * FROM products", conn)
    st.dataframe(products_df)

    #delete
    if not products_df.empty:
        delete_id = st.number_input("Enter Product ID to Delete", min_value=1,key="delete_id")
        if st.button("Delete Product"):
            cursor.execute("DELETE FROM products WHERE id=?", (delete_id,))
            conn.commit()
            st.success("Product Deleted!")

##Sales entry system
elif menu == "Sales Entry":
    st.subheader("Enter Sale")

    products = pd.read_sql_query("SELECT * FROM products",conn)

    if not products.empty:
        products['quantity'] = pd.to_numeric(products['quantity'], errors='coerce').fillna(0).astype(int)
        products['price'] = pd.to_numeric(products['price'], errors='coerce').astype(float)

        products_name = products["name"].tolist()
        selected_product = st.selectbox("Select Product", products_name)
        quantity_sold = st.number_input("Quantity Sold", min_value=1)

        if st.button("Process Sale"):
            products_data = products[products["name"] == selected_product].iloc[0]
            available_quantity = int(products_data["quantity"])

            if quantity_sold <= available_quantity:
                new_quantity = available_quantity - int(quantity_sold)
                total_price = int(quantity_sold)*float(products_data["price"])

                #update stock
                cursor.execute("""
                UPDATE products SET quantity=? WHERE name=?""", 
                (new_quantity, selected_product))

                #insert sale record
                cursor.execute("""
                INSERT INTO sales (product_name, quantity_sold, total_price, sale_date)
                VALUES (?, ?, ?, ?)""", 
                (selected_product, int(quantity_sold), total_price, datetime.now() .isoformat()))

                conn.commit()
                st.success(f"Sale Recorded! Total ₹ {total_price}")
            else:
                st.error("Not enough stock available!")
    else:
        st.warning("No products available.")

#View sales
elif menu == "View Sales":
    st.subheader("View Sales")

    sales_df = pd.read_sql_query("SELECT * FROM sales", conn)
    st.dataframe(sales_df)
        
    st.subheader("Sales Summary")

    sales_summery = pd.read_sql_query("""
    SELECT product_name, SUM(quantity_sold) AS total_quantity_sold, 
    SUM(total_price) AS total_sales
    FROM sales
    GROUP BY product_name """, conn)

    if not sales_summery.empty:
        st.dataframe(sales_summery)
    else:
        st.info("No sales data available.")

    csv = sales_summery.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Sales Summary Data",
        csv,
        "sales_summary.csv",
        "text/csv",
        key="download_csv"
    )

    st.subheader("Sales Records")

    sales_df = pd.read_sql_query("SELECT * FROM sales", conn)

    if not sales_df.empty:
        st.dataframe(sales_df)

        csv = sales_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Sales Data",
            data=csv,
            file_name="sales_report.csv",
            mime="text/csv"
        )
    else:
        st.info("No sales recorded yet.")

#dashboard

elif menu == "Dashboard":
    st.subheader("Inventory Dashboard")

    total_products = cursor.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    total_sales = cursor.execute("SELECT SUM(total_price) FROM sales").fetchone()[0]

    col1,col2 = st.columns(2)
    col1.metric("Total Products", total_products)
    col2.metric("Total Sales ₹", total_sales)

    df = pd.read_sql_query("SELECT name, quantity FROM products",conn)

    if not df.empty:
        st.subheader("Current Stock Levels")
        st.bar_chart(df.set_index("name"))
    else:
        st.info("No products available.")

    low_stock_products = pd.read_sql_query(
    "SELECT * FROM products WHERE CAST(quantity AS INTEGER) <= 10",
    conn
)

    if not low_stock_products.empty:
        st.subheader("Low Stock Alerts")
        st.dataframe(low_stock_products)
    else:
        st.info("Stocks are Avalilable")
