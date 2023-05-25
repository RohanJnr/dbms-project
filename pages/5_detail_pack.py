import mysql.connector
import streamlit as st
import pandas as pd
from collections import defaultdict


db = mysql.connector.connect(
    host = 'localhost',
    user = 'dbms',
    password = 'dbms',
    database = 'dbms'
)

c = db.cursor()

c.execute("select travel_packs.pack_id, travel_packs.destination, sites.site_id, sites.site_name, sites.entry_fee from pack_sites join sites on sites.site_id=pack_sites.site_id join travel_packs on travel_packs.pack_id = pack_sites.pack_id;")

data = c.fetchall()

packs = defaultdict(list)

for pack_id, dest, site_id, site_name, price in data:
    packs[f"{pack_id}. {dest}"].append((site_id, site_name, price))

for key, value in packs.items():
    st.header(key)

    num_rows = len(value)

    # Create two columns
    col1, col2, col3 = st.columns(3)

    # Display the table
        
    with col1:
        st.write("Site ID")
        for i in range(num_rows):
            st.write(value[i][0])

    with col2:
        st.write("Visiting Sites")
        for i in range(num_rows):
            st.write(value[i][1])

    with col3:
        st.write("Price")
        for i in range(num_rows):
            st.write(value[i][2])

