import mysql.connector
import streamlit as st
import pandas as pd
from mysql.connector.errors import IntegrityError


def create_table():
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS `dbms`.`user_packs`(
            `pack_id` INT NOT NULL,
            `user_id` INT NOT NULL,
            FOREIGN KEY (pack_id) REFERENCES travel_packs(pack_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            PRIMARY KEY (pack_id, user_id)
        ) ENGINE = InnoDB;"""
    )

def add_data(values):
    c.execute('INSERT INTO user_packs(pack_id, user_id) VALUES(%s, %s)', values)
    db.commit()


def view():
    c.execute('select * from user_packs')
    return c.fetchall()

def delete_record(pack_id, user_id):
    c.execute(f'delete from user_packs where pack_id = %s and user_id = %s', (pack_id, user_id))
    db.commit()

def update(attribute, new_value, pack_id, user_id):
    c.execute(f'update user_packs SET `{attribute}` = "{new_value}" where pack_id="{pack_id}" and user_id = "{user_id}"')
    db.commit()

def get_user(pack_id, user_id):
    c.execute('select * from user_packs where pack_id = %s and user_id = %s', (pack_id, user_id))
    return c.fetchall()


def create():
    pack_id_choice = st.number_input('Enter pack id', value=0)
    user_id_choice = st.number_input('Enter user id', value=0)
    if st.button("Add User"):
        try:
            add_data((pack_id_choice, user_id_choice))
        except Exception as e:
            if isinstance(e, IntegrityError):
                st.error(f"ERROR: {e}")
            else:
                raise e
        else:
            st.success("Successfully added record!")


def delete():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ["pack_id", "user_id"]))
    pack_ids = []
    user_ids = []

    for i in data:
        if (pack_id := i[0]) not in pack_ids:
            pack_ids.append(pack_id)
        
        if (user_id := i[1]) not in user_ids:
            user_ids.append(user_id)
    
    pack_id_choice = st.selectbox('Select user to delete', pack_ids)
    user_id_choice = st.selectbox('Select user to delete', user_ids)
    if st.button('Delete Record'):
        delete_record(pack_id_choice, user_id_choice)
        st.experimental_rerun()


def edit():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ["pack_id", "user_id"]))
    pack_ids = []
    user_ids = []

    for i in data:
        if (pack_id := i[0]) not in pack_ids:
            pack_ids.append(pack_id)
        
        if (user_id := i[1]) not in user_ids:
            user_ids.append(user_id)


    pack_id_choice = st.selectbox('Select pack_id', pack_ids)
    user_id_choice = st.selectbox('Select user_id', user_ids)

    data = get_user(pack_id_choice, user_id_choice)
    if data:
        attribute_choices = ["pack_id", "user_id"]
        attribute = st.selectbox('Select attribute to update', attribute_choices)
        new_value = st.number_input(f"Enter a new value for {attribute}", value=0)
        if st.button("Update"):
            update(attribute, new_value, pack_id_choice, user_id_choice)
            st.success("Updated!")

def viewList():
    c.execute('select pack_id, GROUP_CONCAT(CONCAT(users.user_id, " | ", users.first_name)) from user_packs join users on users.user_id=user_packs.user_id group by pack_id;')
    return c.fetchall()
    

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
            data = viewList()
        except Exception as e:
            raise e
        df = pd.DataFrame(data, columns = ["pack_id", "user_id"])
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
        user = 'dbms',
        password = 'dbms',
        database = 'dbms'
    )
    c = db.cursor()

main()