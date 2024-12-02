import streamlit as st
import webbrowser as wbb

aboutMe_page = st.Page(page = "views/aboutMe.py", title = "About me", icon = "😄", default=True)

chatbot_page = st.Page(page = "views/chatbot.py", title = "Chatbot", icon = "🤖")

# Navegação de páginas

pg = st.navigation(
    {
        "Informações": [aboutMe_page],
        "Chat": [chatbot_page]
    }
)

# Compartilhamento entre páginas
st.logo("assets/ALENC LOGO.png")

st.sidebar.text("Logo feita por Vitté Papelaria!")
btnInsta = st.sidebar.button("Instagram", icon=":material/heart_check:")

if btnInsta: 
    wbb.open("https://www.instagram.com/vittepapelaria")

# Executar navegação

pg.run()