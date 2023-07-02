import mysql.connector
import streamlit as st
import pandas as pd


def create_table():
    c.execute(f"""CREATE TABLE IF NOT EXISTS `dbms`.`users`(
    `user_id` INT NOT NULL AUTO_INCREMENT,
    `first_name` VARCHAR(128) NOT NULL,
    `last_name` VARCHAR(128) NOT NULL,
    `date_of_birth` DATE NOT NULL,
    `gender` VARCHAR(8) NOT NULL,
    `email` VARCHAR(128) NOT NULL,
    `phone` VARCHAR(15) NOT NULL,
    PRIMARY KEY(`user_id`)
) ENGINE = InnoDB;""")

def add_data(values):
    c.execute('INSERT INTO users(first_name, last_name, date_of_birth, gender, email, phone) VALUES(%s, %s, %s, %s, %s, %s)', values)
    db.commit()


def view():
    c.execute('select * from users')
    return c.fetchall()

def delete_record(user_id):
    c.execute(f'delete from users where user_id = %s', (user_id, ))
    db.commit()

def update(choice, attrichoice, updated_attri):
    c.execute(f'update users SET `{attrichoice}` = "{updated_attri}" where user_id = "{choice}"')
    db.commit()

def get_user(user_id):
    c.execute(f'select * from users where user_id = "{user_id}"')
    return c.fetchall()


def create():
    first_name = st.text_input("First name: ")
    last_name = st.text_input("Last name: ")
    date_of_birth = st.date_input("Date of Birth: ")
    phone = st.text_input("Phone Number: ")
    gender = st.text_input("Gender(male/female): ")
    email = st.text_input("Email: ")
    if st.button("Add User"):
        add_data((first_name, last_name, date_of_birth, gender, email, phone))
        st.success("Successfully added record!")


def delete():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ["user_id", "first_name", "last_name", "date_of_birth", "phone", "gender", "email"]))
    user_ids = [i[0] for i in data]
    choice = st.selectbox('Select user to delete', user_ids)
    if st.button('Delete Record'):
        delete_record(choice)
        st.experimental_rerun()


def edit():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ["user_id", "first_name", "last_name", "date_of_birth", "phone", "gender", "email"]))
    user_ids = [i[0] for i in data]
    choice = st.selectbox('Select user_id', user_ids)
    data = get_user(choice)
    if data:
        attri = ["user_id", "first_name", "last_name", "date_of_birth", "phone", "gender", "email"]
        attrichoice = st.selectbox('Select attribute to update', attri)
        updated_attri = st.text_input(f"Enter a new value for {attrichoice}")
        if updated_attri == '':
            updated_attri = data[0][attri.index(attrichoice)]
        if st.button("Update"):
            update(choice, attrichoice, updated_attri)
            st.success("Updated!")


def main():
    st.title("Travel Agency ")
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
        df = pd.DataFrame(data, columns = ["user_id", "first_name", "last_name", "date_of_birth", "phone", "gender", "email"])
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