import streamlit as st
import os
import nbformat
from nbconvert import HTMLExporter
import streamlit.components.v1 as components

# Configuração visual
st.set_page_config(page_title="Curso Python PET", layout="wide")

# CSS Customizado para melhorar a estética do notebook embutido
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FF4B4B; color: white; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e7bcf,#2e7bcf); color: white; }
    </style>
    """, unsafe_allow_html=True)

# Gerenciamento de Progresso
if 'progresso' not in st.session_state:
    st.session_state.progresso = 1

def carregar_notebook(caminho_file):
    if not os.path.exists(caminho_file):
        return "<p style='color:red;'>Erro: Notebook não encontrado no caminho especificado.</p>"
    
    with open(caminho_file, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        html_exporter = HTMLExporter()
        html_exporter.template_name = 'basic'
        (body, resources) = html_exporter.from_notebook_node(nb)
        return body

# --- SIDEBAR ---
st.sidebar.title("Curso Python PET")
st.sidebar.subheader(f"Seu Progresso: Módulo {st.session_state.progresso}/8")
st.sidebar.progress(st.session_state.progresso / 8)

menu = st.sidebar.radio("Navegação", ["Home", "Curso", "Ajuda"])

# --- CONTEÚDO ---
if menu == "Home":
    st.title("Bem-vindo ao curso de Python!")
    st.markdown("""
    Esta plataforma foi desenhada para levar você do zero à análise de dados.
    
    **O que você vai aprender:**
    1. Fundamentos e Sintaxe.
    2. Estruturas de Decisão e Repetição.
    3. Funções e Modularização.
    4. Bibliotecas de Dados (Pandas).
    
    *Clique em 'Curso' no menu lateral para começar.*
    """)
    if st.button("Começar Agora"):
        st.info("Selecione 'Curso' na barra lateral.")

elif menu == "Curso":
    modulos = {
        1: "Introdução e Ambiente",
        2: "Variáveis e Tipos",
        3: "Operações Matemáticas",
        4: "Condicionais",
        5: "Loops (For, While)",
        6: "Funções",
        7: "Manipulação de Arquivos",
        8: "Introdução ao Pandas"
    }
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.subheader("Módulos")
        escolha = st.radio("Escolha:", [f"{i}. {name}" for i, name in modulos.items()])
        mod_id = int(escolha.split(".")[0])

    with col2:
        if mod_id > st.session_state.progresso:
            st.error(f"🔒 Este módulo está bloqueado. Conclua o Módulo {st.session_state.progresso} primeiro.")
        else:
            st.title(modulos[mod_id])
            
            # Caminho para o notebook
            path_nb = f"notebooks/modulo_{mod_id}.ipynb"
            
            # Renderização
            html_conteudo = carregar_notebook(path_nb)
            components.html(html_conteudo, height=600, scrolling=True)
            
            st.divider()
            if st.button("Marcar como Concluído ✅"):
                if mod_id == st.session_state.progresso and mod_id < 8:
                    st.session_state.progresso += 1
                    st.success("Módulo concluído! Próximo liberado.")
                    st.rerun()
                elif mod_id == 8:
                    st.balloons()
                    st.success("PARABÉNS! Você finalizou o curso de Python!")

elif menu == "Ajuda":
    st.title("Suporte ao Aluno")
    st.write("Dúvidas comuns:")
    with st.expander("Como rodar o código?"):
        st.write("Você pode testar os códigos no seu terminal local ou no VS Code.")