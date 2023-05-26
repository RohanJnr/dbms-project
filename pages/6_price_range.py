import mysql.connector
import streamlit as st
import pandas as pd


db = mysql.connector.connect(
    host = 'localhost',
    user = 'dbms',
    password = 'dbms',
    database = 'dbms'
)

c = db.cursor()


Procedure = """
DELIMITER //

CREATE PROCEDURE GetPriceRangeData(IN input_price DECIMAL(10, 2), IN range_value DECIMAL(10, 2))
BEGIN
    DECLARE min_price DECIMAL(10, 2);
    DECLARE max_price DECIMAL(10, 2);

    SET min_price = input_price - range_value;
    SET max_price = input_price + range_value;

    SELECT * FROM travel_packs
    WHERE iteneary_costs >= min_price AND iteneary_costs <= max_price;
END //

DELIMITER ;
"""


base_price = st.number_input("Enter the first integer:", value=0, step=1)
price_range = st.number_input("Enter the second integer:", value=0, step=1)

if st.button("Get packs in price range"):

    c.callproc("GetPriceRangeData", [base_price, price_range])
    results = []
    for result in c.stored_results():
        results.extend(result.fetchall())


    # for row in results:
    #     print(row)
    #     st.write(row)

    df = pd.DataFrame(results, columns = ["pack_id", "origin", "destination", "num_days", "iteneary_costs", "departure_timestamp", "return_timestamp", "slots_left"])
    st.dataframe(df)



