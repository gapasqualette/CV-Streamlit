import streamlit as st
import webbrowser as wbb
import pyperclip as ppc
import streamlit.components.v1 as cmp

import time
from forms.contact import contact_form

@st.dialog("Contact Me: ")
def show_contact():
    contact_form()
    
# Criação de duas colunas (Foto de Perfil & Infos Básicas)

col1, col2 = st.columns(2, gap="large", vertical_alignment="center")

with col1: 
    st.title("Guilherme de A. Pasqualette", anchor=False)
    st.write(
        """
            - 28 anos.
            - Grajaú, Rio de Janeiro/RJ - Brasil.
            - Graduando em Engenharia da Computação na Estácio, atualmente estagiando na Transpetro.
        """
    )
    
    col3, col4 = st.columns(2, gap="medium", vertical_alignment="center")
    with col3:
        lnk_btn = st.button("LinkedIn",icon=":material/token:")
        if lnk_btn:
            wbb.open("https://www.linkedin.com/in/galencastro-pasqualette/")
    
    with col4:
        wpp_btn = st.button("WhatsApp", icon=":material/smartphone:")
        if wpp_btn:
            ppc.copy("21992696959")
            warningInfo = st.toast("Número de telefone copiado com sucesso!", icon=":material/phone:")

with col2:
    st.image("assets/FotoCasamento.jpeg", width=200)
    if st.button("📱 Contate-me"):
        show_contact()

# Experiencias

st.write("\n")
st.subheader("Experiências & Qualificações", anchor=False)
st.write(
    """ 
    - 2 anos trabalhando em Óleo & Gás na parte de suporte e desenvolvimento.
    - Conhecimentos em Python, C, Pacote Office.
    - Bom entendimento de análise de dados e otimização.
    - Excelente companheiro de equipe, sempre demonstrando iniciativa a comunicação e cooperação.
    """
)

# Habilidades

st.write("\n")
st.subheader("Hard Skills", anchor=False)
st.write(
    """
    - Programação: Python (Pandas, Scikit-learn, Streamlit), C, SQL, VBA (Básico).
    - PowerBI, Excel, PowerApps para visualização de dados.
    - Banco de Dados: Postgres, Dataverse.
    - Fluência em Inglês e Espanhol intermediário.
    - Automação de processos Low-Code com Power Automate e noções básicas de Arduino.
    """
)

perguntas = {
            "Data de Formatura": "- Fim de 2025.",
            "Meus Hobbies": "- Viajar, sair para comer, fazer projetos por conta própria, assistir séries e filmes de ficção e fantasia",
            "Filme e séries favoritas": "- Senhor dos Anéis (Todos) & Black Mirror",
            "Níveis de idiomas": "- C1 em Inglês (Link Abaixo) e Espanhol Intermediário"
    }

box = st.selectbox("Curiosidades", list(perguntas.keys()))

if box == "Níveis de idiomas":
    img_pop = st.checkbox("Mostrar Certificado de Inglês")
    if img_pop:
        st.image("assets/EnglishCertificate.jpg")

else: 
    st.write(perguntas[box]) 
       
        
        