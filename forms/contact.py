import streamlit as st
import re
import requests

WEBHOOK_URL= st.secrets["WEBHOOK_URL"]

def emailisValid(email):
    # E.R. para email
    email_padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_padrao, email) is not None

def contact_form():
    with st.form("contact_form"):
        name = st.text_input("Nome:")
        email = st.text_input("Email:")
        message = st.text_area("Escreva sua mensagem:")
        submit_btn = st.form_submit_button("Enviar")

        if submit_btn:
            if not WEBHOOK_URL:
                st.error("Serviço não dispónível. Tente novamente mais tarde.")
                st.stop()
            if not name:
                st.error("Nome em branco...")
                st.stop()
                
            if not email:
                st.error("Email em branco...")
                st.stop()
                
            if not message:
                st.error("Mensagem em branco...")
                st.stop()

            if not emailisValid(email):
                st.error("Email inválido. Verifique a estrutura do email")
                st.stop()

            # Formulário enviado corretamente

            info = {"nome": name, "email": email, "mensagem": message}

            resposta = requests.post(WEBHOOK_URL, json=info)

            if resposta.status_code == 200:
                st.success("Formulário enviado com sucesso!", icon="🎯")
                name.replace(info["nome"], "")
                email.replace(info["email"], "")
                message.replace(info["mensagem"], "")
                
            else: 
                st.error("Ocorreu erro no envio do formulário", icon="😪")
        
             