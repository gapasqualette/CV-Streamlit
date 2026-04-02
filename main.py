import streamlit as st

st.set_page_config(layout="wide")

pages = {
    'My info': [st.Page(page = "views/aboutMe.py", title = "About me", icon = ":material/info:", default=True)
                ],
    'Projects': [st.Page(page = 'views/dashboard_housing.py', title = 'USA Housing Dashboard', icon='📊'),
                 st.Page(page = 'views/expenseTracker.py', title = 'Expense Tracker', icon='💳'),
                 st.Page(page = 'views/imdb_scrap.py', title = 'IMDB Web Scrapper', icon='🎬')]
         
         }

pg = st.navigation(pages)  
# Compartilhamento entre páginas
st.logo("assets/ALENC LOGO.png")

st.sidebar.text("Logo feita por Vitté Papelaria!")
btnInsta = st.sidebar.button("Instagram", icon=":material/heart_check:")

if btnInsta: 
    st.link_button("https://www.instagram.com/vittepapelaria")

# Executar navegação

pg.run()