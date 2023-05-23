import mysql.connector
import streamlit as st
import pandas as pd


def create_table():
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS `dbt`.`sites`(
            `site_id` INT NOT NULL AUTO_INCREMENT,
            `site_name` VARCHAR(128) NOT NULL,
            `address` VARCHAR(256) NOT NULL,
            `entry_fee` FLOAT NOT NULL,
            PRIMARY KEY (site_id)
        ) ENGINE = InnoDB;
    """)

def add_data(values):
    c.execute('INSERT INTO sites(site_name, address, entry_fee) VALUES(%s, %s, %s)', values)
    db.commit()


def view():
    c.execute('select * from sites')
    return c.fetchall()

def delete_record(site_id):
    c.execute(f'delete from sites where site_id = %s', (site_id, ))
    db.commit()

def update(attribute, new_value, site_id):
    c.execute(f'update sites SET `{attribute}` = "{new_value}" where site_id="{site_id}"')
    db.commit()

def get_user(user_id):
    c.execute(f'select * from sites where site_id = "{user_id}"')
    return c.fetchall()


def create():
    site_name = st.text_input("Site name: ")
    address = st.text_input("Address: ")
    entry_fee = st.number_input("Entry Fee: ")
    if st.button("Add Site"):
        add_data((site_name, address, entry_fee))
        st.success("Successfully added record!")


def delete():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ["site_id", "site_name", "address", "entry_fee"]))
    site_ids = [i[0] for i in data]
    choice = st.selectbox('Select site to delete', site_ids)
    if st.button('Delete Record'):
        delete_record(choice)
        st.experimental_rerun()


def edit():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ["site_id", "site_name", "address", "entry_fee"]))
    site_ids = []
    for i in data:
        if (site_id := i[0]) not in site_ids:
            site_ids.append(site_id)


    site_id_choice = st.selectbox('Select site_id', site_ids)

    data = get_user(site_id_choice)
    if data:
        attribute_choices = ["site_name", "address", "entry_fee"]
        attribute = st.selectbox('Select attribute to update', attribute_choices)
        new_value = st.text_input(f"Enter a new value for {attribute}")
        if st.button("Update"):
            update(attribute, new_value, site_id_choice)
            st.success("Updated!")


def main():
    st.title("Travel Agency")
    menu = ["Add", "View", "Edit", "Remove"]
    choice = st.sidebar.selectbox("Menu", menu)
    create_table()
    if choice == 'Add':
        st.subheader("Enter details")
        try:
            create()
        except Exception as e:
            raise e
    elif choice == 'View':
        st.subheader("Information in Table")
        try:
            data = view()
        except Exception as e:
            raise e
        df = pd.DataFrame(data, columns = ["site_id", "site_name", "address", "entry_fee"])
        st.dataframe(df)
    
    elif choice == 'Remove':
        st.subheader('Select row to delete')
        delete()
    elif choice == 'Edit':
        st.subheader('Select row to update')
        edit()


if __name__ == '__main__':
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'dbt',
        password = 'dbt',
        database = 'dbt'
    )
    c = db.cursor()

main()