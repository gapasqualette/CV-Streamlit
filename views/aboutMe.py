import streamlit as st

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
    
    cols = st.columns(3)
    with cols[0]:
        st.link_button('LinkedIn', "https://www.linkedin.com/in/galencastro-pasqualette/")
    
    with cols[1]:
        st.link_button('Whatsapp', url='https://wa.me/5521992696959')
    
    with cols[2]:
        st.link_button("Instagram", url='https://www.instagram.com/g.pasqualette/', icon=":material/camera:")
    
with col2:
    st.image("assets/FotoCasamento.jpeg", width=200)

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

box = st.selectbox("Curiosidades", list(perguntas.keys()), placeholder="Escolha uma opção")
    
if box == "Níveis de idiomas":
    img_pop = st.checkbox("Mostrar Certificado de Inglês")
    if img_pop:
        st.image("assets/EnglishCertificate.jpg", width=800)

elif box != "": 
    st.write(perguntas[box]) 
       
        
        