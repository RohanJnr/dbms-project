import mysql.connector
import streamlit as st
import pandas as pd


def create_table():
    c.execute(f"""CREATE TABLE IF NOT EXISTS `dbt`.`travel_packs`(
    `pack_id` INT NOT NULL AUTO_INCREMENT,
    `origin` VARCHAR(128) NOT NULL,
    `destination` VARCHAR(128) NOT NULL,
    `num_days` INT NOT NULL,
    `iteneary_costs` INT NOT NULL,
    `departure_timestamp` DATE NOT NULL,
    `return_timestamp` DATE NOT NULL,
    `slots_left` INT NOT NULL DEFAULT 3,
    PRIMARY KEY(`pack_id`)
) ENGINE = InnoDB;""")

def add_data(values):
    c.execute('INSERT INTO travel_packs(origin, destination, num_days, iteneary_costs, departure_timestamp, return_timestamp, slots_left) VALUES(%s, %s, %s, %s, %s, %s, %s)', values)
    db.commit()


def view():
    c.execute('select * from travel_packs')
    return c.fetchall()

def delete_record(user_id):
    c.execute(f'delete from travel_packs where pack_id = %s', (user_id, ))
    db.commit()

def update(choice, attrichoice, updated_attri):
    c.execute(f'update travel_packs SET `{attrichoice}` = "{updated_attri}" where user_id = "{choice}"')
    db.commit()

def get_user(user_id):
    c.execute(f'select * from travel_packs where pack_id = "{user_id}"')
    return c.fetchall()


def create():
    origin = st.text_input("Origin(Departure Flight): ")
    destination = st.text_input("Destination: ")
    num_days = st.number_input("Number of Days: ", value=0)
    iteneary_costs = st.number_input("Estimated Iteneary Costs(in Rs): ")
    departure_timestamp = st.date_input("Departure Date and Time: ")
    return_timestamp = st.date_input("Return Date and Time: ")
    slots_left = st.number_input("Enter number of slots: ", value=3)
    if st.button("Add Travel Pack"):
        add_data((origin, destination, num_days, iteneary_costs, departure_timestamp, return_timestamp, slots_left))
        st.success("Successfully added record!")


def delete():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ["pack_id", "origin", "destination", "num_days", "iteneary_costs", "departure_timestamp", "return_timestamp", "slots_left"]))
    user_ids = [i[0] for i in data]
    choice = st.selectbox('Select user to delete', user_ids)
    if st.button('Delete Record'):
        delete_record(choice)
        st.experimental_rerun()


def edit():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ["pack_id", "origin", "destination", "num_days", "iteneary_costs", "departure_timestamp", "return_timestamp", "slots_left"]))
    user_ids = [i[0] for i in data]
    choice = st.selectbox('Select user_id', user_ids)
    data = get_user(choice)
    if data:
        attri = ["pack_id", "origin", "destination", "num_days", "iteneary_costs", "departure_timestamp", "return_timestamp", "slots_left"]
        attrichoice = st.selectbox('Select attribute to update', attri)
        updated_attri = st.text_input(f"Enter a new value for {attrichoice}")
        if updated_attri == '':
            updated_attri = data[0][attri.index(attrichoice)]
        if st.button("Update"):
            update(choice, attrichoice, updated_attri)
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
        df = pd.DataFrame(data, columns = ["pack_id", "origin", "destination", "num_days", "iteneary_costs", "departure_timestamp", "return_timestamp", "slots_left"])
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