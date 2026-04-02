import streamlit as st
import base64
from streamlit_pdf_viewer import pdf_viewer

st.header("📄 My CV | Portfolio ", divider=True)
path = 'assets/CV.pdf'

projects_links = {
    "Olympic Athletes Analysis": 'https://github.com/gapasqualette/Athletes-Events-Data-Analysis',
    "Housing Dashboard": 'https://github.com/gapasqualette/Housing_Dashboard',
    "Credit Card Transactions": "https://github.com/gapasqualette/credit-card-transactions"
}

NUM_PROJECTS = len(projects_links)

cols = st.columns([70,5,25])

# with cols[0]:
    # with st.expander('My Curriculum', icon='📃'):
    #     pdf_viewer(path, width=700)

with cols[1]:
    st.html(
        f"""<div style="
                border-left: 3px solid red;
                height: {100+60*NUM_PROJECTS}px;
                margin: auto
                "></div>
        """ 
        )
   
# with cols[2]:
    
    # with open(path, 'rb') as file:
    #     file_bytes = file.read()
    #     file.close()

    # st.download_button('PDF', data=file_bytes, file_name='Guilherme Pasqualette - CV.pdf', type='primary', use_container_width=True, icon=':material/download:', mime='application/pdf')

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