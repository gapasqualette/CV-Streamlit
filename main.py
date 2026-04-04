import streamlit as st

st.set_page_config(layout="wide")

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

st.header("📄 My CV | Portfolio ", divider=True)

path = 'assets/Currículo_Guilherme_AnaliseDeDados.pdf'

projects_links = {
    "Olympic Athletes Analysis": 'https://github.com/gapasqualette/Athletes-Events-Data-Analysis',
    "Housing Dashboard": 'https://housingdashboard-gapasqualette.streamlit.app',
    "Credit Card Transactions": "https://github.com/gapasqualette/credit-card-transactions"
}

NUM_PROJECTS = len(projects_links)

cols = st.columns([70,5,25])

with cols[0]:
    st.pdf(path, height=600)

with cols[1]:
    st.html(
        f"""<div style="
                border-left: 3px solid red;
                height: {100+60*NUM_PROJECTS}px;
                margin: auto;
                width: 0;
                "></div>
        """ 
        )
   
with cols[2]:
    st.subheader('Links for Projects', text_alignment='center' ,divider=True)
    with st.container(height='content', width='stretch', border=True):
        for name, link in projects_links.items():
            st.link_button(
                label=name,
                url=link,
                type='secondary',
                icon=':material/deployed_code:',
                use_container_width=True,   
            )

    st.divider()
    with open(path, 'rb') as file:
        file_bytes = file.read()
        file.close()

    st.download_button('CV - PDF', data=file_bytes, file_name='Guilherme Pasqualette - CV.pdf', type='primary', use_container_width=True, icon=':material/download:', mime='application/pdf')


