import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd

# Database Connection URL
DB_URL = "mysql+pymysql://jup1user:Jup12user@localhost/retails_orders"  # Update with your credentials

# Predefined Queries
QUERIES = {
"1 state with most products sold" : "SELECT State	,SUM(Quantity) AS Most_Quantity FROM dfto_order2 E INNER JOIN dfto_order D ON (D.ORDER_ID = E.ORDER_ID) GROUP BY State ORDER BY Most_Quantity DESC LIMIT 1;"
,"2 Show me the top 10 products Ranked based on revenue" : "SELECT PRODUCT_ID,  SUM(sale_price), RANK() OVER (ORDER BY SUM(sale_price) DESC) AS Revenue_rank  FROM dfto_order2  GROUP BY      Product_Id;"
,"3 Show me the number of products per Sub Category" : "SELECT SUB_CATEGORY, COUNT(DISTINCT PRODUCT_ID) FROM DFTO_ORDER2 GROUP BY SUB_CATEGORY ;"
,"4 Which city has most discounted products" : "SELECT CITY 	,ROUND(SUM(DISCOUNTED_AMOUNT)) AS Most_Discount FROM dfto_order2 E INNER JOIN dfto_order D ON (D.ORDER_ID = E.ORDER_ID) GROUP BY CITY ORDER BY Most_Discount DESC LIMIT 1; "
,"5 show me the least performing PRODUCTS who had no sales at all " : "SELECT PRODUCT_ID FROM dfto_order2 GROUP BY PRODUCT_ID HAVING SUM(SALE_PRICE)=0;"
,"6 What is the sales in last 1 month" : "SELECT      D.Order_Date, D.ORDER_ID, STATE, CITY, CATEGORY, SUB_CATEGORY, PRODUCT_ID, SALE_PRICE FROM      dfto_order D     INNER JOIN dfto_order2 O ON D.ORDER_ID = O.ORDER_ID WHERE      Order_Date >= DATE_SUB((select max(Order_Date) from dfto_order), INTERVAL 1 MONTH)     ORDER BY 1 DESC;"
,"7 Which month has given most revenue" : "SELECT      MONTHNAME(Order_Date) AS month,     SUM(Sale_Price) AS total_revenue FROM      dfto_order D     INNER JOIN dfto_order2 O ON D.ORDER_ID = O.ORDER_ID GROUP BY   MONTHNAME(Order_Date) ORDER BY      total_revenue DESC LIMIT 1;"
,"8 Which state sold most number of phones" : "SELECT      State,     SUM(Quantity) AS Total_Quantity FROM      dfto_order D     INNER JOIN dfto_order2 O ON D.ORDER_ID = O.ORDER_ID WHERE      Sub_Category = 'Phones' GROUP BY   State ORDER BY      Total_Quantity DESC LIMIT 1;"
,"9 What is the most sold product in Georgia" : "SELECT      Category, Sub_Category,Product_Id,     SUM(Quantity) AS total_quantity_sold FROM      dfto_order D     INNER JOIN dfto_order2 O ON D.ORDER_ID = O.ORDER_ID WHERE      State = 'Georgia' GROUP BY   Category, Sub_Category,Product_Id ORDER BY      total_quantity_sold DESC LIMIT 1;"
,"10 Which State has used more Same Day delivery" : "SELECT      State,     Count(d.Order_ID) AS Total_Orders FROM      dfto_order d WHERE      Ship_Mode = 'Same Day' GROUP BY      State ORDER BY      Total_Orders DESC LIMIT 1;"
}

# Streamlit App
st.title("Retail Orders: Requests provided from Self")
st.write("Select a query from the dropdown and click 'Run Query' to see the results or click 'View Query' to view the query.")


# Query Dropdown
query_title = st.selectbox("Select Query", list(QUERIES.keys()))

# Action Buttons
col1, col2 = st.columns(2)

# View Query Button
if col1.button("View Query"):
    query = QUERIES[query_title]
    st.write("**Selected Query:**")
    st.code(query, language="sql")  # Display the query in formatted SQL

# Run Query Button
if col2.button("Run Query"):
    try:
        # Connect to the Database
        engine = create_engine(DB_URL)
        with engine.connect() as connection:
            query = QUERIES[query_title]  # Get the selected query
            result = connection.execute(text(query))
            results = result.fetchall()  # Fetch all rows
            columns = result.keys()  # Get column names

        # Display Results
        if results:
            df = pd.DataFrame(results, columns=columns)  # Convert results to a DataFrame
            st.write("Query Results:")
            st.dataframe(df)  # Display the results
        else:
            st.write("No results found for this query.")
    except Exception as e:
        st.error(f"Error: {e}")