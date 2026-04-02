import streamlit as st
import sqlite3
import datetime
import pandas as pd

def conectar_gastos():
    return sqlite3.connect("assets/gastos.db")

def insert_movement(amount: float, description: str, cat: str, date: str, money: float):
    con = conectar_gastos()
    cursor = con.cursor()

    cursor.execute('INSERT INTO gastos (descrição, amount, type, date) VALUES (?,?,?,?)', (description, amount, cat, date))

    if cat == 'Expense':
        amount = amount * (-1)
    
    amountNew: float = money + amount

    with open('assets/money.txt', 'w') as file:
        file.write(str(amountNew))
        file.close()
    
    con.commit()
    cursor.close()
    con.close()

today: datetime = datetime.datetime.today()

with open('assets/money.txt', 'r') as file:
    text = file.read().strip()

st.markdown(
        """
        <style>
        .vl {
            border-left: 3px solid white;
            height: 250px; /* Altura da linha */
            position: absolute;
            left: 50%; /* Alinhamento horizontal */
            margin-left: -1px; /* Centralização */
            top: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
)

money: float = float(text)
st.header(f'**Expense Tracker** - **R${money:,.2f}**', divider=True)

cols = st.columns([49,2,49])

with cols[0]:
    subcols = cols[0].columns(2)
    with subcols[0]:
        date = st.date_input('Bank Movement Date', format='DD/MM/YYYY', max_value=datetime.datetime.today(), value=datetime.datetime.today())
        amount = st.number_input('Amount', min_value=1.0, max_value=money)

    with subcols[1]:
        cat = st.selectbox('Category', ['Expense', 'Entry'])
        description = st.text_input('Description', placeholder='What kind of movement happened?')
    
    if st.button('Launch Movement 💵', type='primary',use_container_width=True):
        if date and amount < money and cat and description:
            insert_movement(amount, description, cat, date, money)
            st.toast('Bank Movement inserted into database successfully')
            st.rerun()
        else:
            st.warning('Informations are missing!')

with cols[1]:
    st.markdown('<div class = "vl"></div>', unsafe_allow_html=True)

with cols[2]:
    subcols2 = cols[2].columns(2)
    with subcols2[0]:
        init_date = st.date_input('From: ')
    with subcols2[1]:
        if init_date:
            end_date = st.date_input('Until: ',min_value=init_date, max_value=today)

con = conectar_gastos()
df = pd.read_sql_query('SELECT * FROM gastos', con)
con.close()

st.subheader('Bank History', divider=True)

st.table(df[['date', 'type', 'amount', 'descrição']])
