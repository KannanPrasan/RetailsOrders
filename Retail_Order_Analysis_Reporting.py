import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd

# Database Connection URL
DB_URL = "mysql+pymysql://jup1user:Jup12user@localhost/retails_orders"  # Update with your credentials

# Predefined Queries
QUERIES = {
        "1. Find top 10 highest revenue generating products" : "SELECT PRODUCT_ID , SUM(SALE_PRICE) FROM dfto_order2 group by PRODUCT_ID order by 2 desc limit 10;"
        , "2. Find the top 5 cities with the highest profit margins" : "SELECT City 	,SUM((List_Price - cost_price) * Quantity) / SUM(List_Price * Quantity) AS profit_margin FROM dfto_order2 E INNER JOIN dfto_order D ON (D.ORDER_ID = E.ORDER_ID) GROUP BY City ORDER BY profit_margin DESC LIMIT 5;"
        , "3. Calculate the total discount given for each category": "SELECT CATEGORY ,SUM(DISCOUNTED_AMOUNT) AS TOTAL_DISCOUNT FROM DFTO_ORDER2 GROUP BY CATEGORY;"
        , "4. Find the average sale price per product category" : "SELECT CATEGORY ,AVG(SALE_PRICE) AS AVERAGE_SALE_PRICE FROM DFTO_ORDER2 GROUP BY CATEGORY;"
        , "5. Find the region with the highest average sale price" : "SELECT REGION ,AVG(SALE_PRICE) AS AVERAGE_SALE_PRICE FROM dfto_order2 E INNER JOIN dfto_order D ON (D.ORDER_ID = E.ORDER_ID) GROUP BY REGION ORDER BY 2 DESC LIMIT 1 ;"
        , "6. Find the total profit per category" : "SELECT CATEGORY ,SUM(SALE_PRICE-COST_PRICE) AS TOTAL_PROFIT FROM DFTO_ORDER2 GROUP BY CATEGORY;"
        , "7. Identify the top 3 segments with the highest quantity of orders" : "SELECT SEGMENT ,SUM(QUANTITY) AS AVERAGE_SALE_PRICE FROM dfto_order2 E INNER JOIN dfto_order D ON (D.ORDER_ID = E.ORDER_ID) GROUP BY SEGMENT ORDER BY 2 DESC LIMIT 3;"
        , "8. Determine the average discount percentage given per region" : "SELECT REGION ,AVG(DISCOUNT_PERCENT) AS AVERAGE_DP FROM dfto_order2 E INNER JOIN dfto_order D ON (D.ORDER_ID = E.ORDER_ID) GROUP BY REGION ORDER BY 2 DESC ;"
        , "9. Find the product category with the highest total profit" : "SELECT CATEGORY ,SUM(SALE_PRICE-COST_PRICE) AS TOTAL_PROFIT FROM DFTO_ORDER2 GROUP BY CATEGORY LIMIT 1;"
        , "10.Calculate the total revenue generated per year": "SELECT SUBSTRING(ORDER_DATE, 1,4) ,sum(sale_price) AS AVERAGE_DP FROM dfto_order2 E INNER JOIN dfto_order D ON (D.ORDER_ID = E.ORDER_ID) GROUP BY SUBSTRING(ORDER_DATE, 1,4) ORDER BY 2 DESC ;"

}

# Streamlit App
st.title("Retail Orders: Requests provided from GUVI")
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