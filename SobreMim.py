import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.app_logo import add_logo

# Configuração da página
st.set_page_config(page_title="Meu Dashboard Profissional", layout="wide")
st.sidebar.markdown("Desenvolvido por Victor Augusto")


# Título da página
st.title("Bem-vindo ao Meu Dashboard Profissional")

# Seção de Introdução Pessoal
st.header("Sobre Mim")
st.write("""
Olá! Meu nome é Victor Augusto, e sou um(a) profissional na área Cyber Segurança. 
Atualmente, estou focado(a) em aprender novas tecnologias e sistemas operacionais. 
Este dashboard foi criado para compartilhar um pouco sobre meus aprendizados com Data Science.
""")

# Seção de Objetivo Profissional
st.header("Objetivo Profissional")
st.write("""
Meu objetivo é me aprofundar na área de cyber e seguir carreira como pentester. 
Acredito que a combinação de desenvolvimento, redes e dados pode gerar insights e auxiliar no meu objetivo de carreira.
""")

# Seção de Contato (opcional)
st.header("Contato")
st.write("""
Se você quiser entrar em contato comigo, fique à vontade para me enviar uma mensagem por e-mail: victorsantosp10@hotmail.com.
""")

