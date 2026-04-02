import streamlit as st

st.set_page_config(layout="wide")

pages = {
    'MY INFO': [st.Page(page = "views/aboutMe2.py", title = "About me", icon = ":material/info:", default=True)
                ],
    'STREAMLIT PROJECTS': [st.Page(page = 'views/dashboard_housing.py', title = 'USA Housing Dashboard', icon='📊'),
        ]
         
         }

pg = st.navigation(pages)  
# Compartilhamento entre páginas
st.logo("assets/ALENC LOGO.png")

with st.sidebar:
    st.link_button('LinkedIn', "https://www.linkedin.com/in/galencastro-pasqualette/", type='secondary', use_container_width=True, icon=':material/group:')
    st.link_button('WhatsApp', url='https://wa.me/5521992696959', type='secondary', use_container_width=True, icon=':material/call:')
    st.link_button('GitHub', 'https://github.com/gapasqualette', type='secondary', use_container_width=True, icon=':material/computer:')
    st.divider()

    st.text("Logo feita por Vitté Papelaria!")
    btnInsta = st.button("Instagram", icon=":material/heart_check:", use_container_width=True)

    if btnInsta: 
        st.link_button("https://www.instagram.com/vittepapelaria")

# Executar navegação

pg.run()