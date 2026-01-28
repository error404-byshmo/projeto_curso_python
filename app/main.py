import streamlit as st
import os
import nbformat
from nbconvert import HTMLExporter
import streamlit.components.v1 as components

# Configuração visual da aba do navegador
st.set_page_config(page_title="Curso Python PET", layout="wide")

# Link oficial fornecido
LINK_DRIVE = "https://drive.google.com/drive/folders/1EB_AhVvvgn8sNecBOtixVhCFyhlE7sMJ?usp=sharing"

# Estilização CSS para uma interface moderna
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #2e7bcf; color: white; font-weight: bold; }
    .drive-box { 
        padding: 20px; 
        border: 2px solid #34a853; 
        border-radius: 12px; 
        background-color: #f1f8f3;
        text-align: center;
        margin: 20px 0px;
    }
    .drive-button {
        display: inline-block;
        padding: 10px 25px;
        background-color: #34a853;
        color: white !important;
        text-decoration: none;
        border-radius: 6px;
        font-weight: bold;
        transition: 0.3s;
    }
    .drive-button:hover {
        background-color: #2d8e47;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Inicialização do estado de progresso
if 'progresso' not in st.session_state:
    st.session_state.progresso = 1

def carregar_notebook(caminho_file):
    """Converte o arquivo .ipynb em HTML para exibição"""
    if not os.path.exists(caminho_file):
        return f"<div style='color:orange; padding:20px; border:1px solid orange;'>⚠️ Módulo em desenvolvimento. O arquivo <b>{caminho_file}</b> será adicionado em breve.</div>"
    
    try:
        with open(caminho_file, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
            html_exporter = HTMLExporter()
            html_exporter.template_name = 'basic'
            (body, resources) = html_exporter.from_notebook_node(nb)
            return body
    except Exception as e:
        return f"<p style='color:red;'>Erro ao carregar o notebook: {e}</p>"

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.title("Curso Python PET")
st.sidebar.markdown(f"**Progresso Atual: Módulo {st.session_state.progresso}/8**")
st.sidebar.progress(st.session_state.progresso / 8)
st.sidebar.divider()
menu = st.sidebar.radio("Navegação Principal", ["Início", "Módulos do Curso", "Suporte ao Aluno"])

# --- PÁGINA INICIAL ---
if menu == "Início":
    st.title("Bem-vindo ao Curso de Python")
    st.markdown("""
    Esta plataforma foi criada para facilitar o seu aprendizado de programação. 
    Aqui você encontrará teoria integrada com prática através de notebooks interativos.
    
    **O que você terá acesso:**
    * **8 Módulos didáticos** (do básico ao Pandas).
    * **Exercícios práticos** dentro de cada aula.
    * **Sistema de progressão** (conclua um para liberar o próximo).
    """)

    # Card de acesso ao Google Drive
    st.markdown(f"""
    <div class="drive-box">
        <p style="margin-bottom: 12px; font-size: 1.1em;"><b>📂 Repositório de Arquivos</b></p>
        <p style="font-size: 0.95em; color: #444; margin-bottom: 15px;">
            Deseja praticar no seu próprio computador? Baixe os notebooks originais no Google Drive:
        </p>
        <a class="drive-button" href="{LINK_DRIVE}" target="_blank">
            ACESSAR PASTA NO DRIVE
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")
    st.info("**Dica:** Use o menu lateral para acessar a área de **'Módulos do Curso'**.")

# --- PÁGINA DO CURSO ---
elif menu == "Módulos do Curso":
    modulos = {
        1: "Introdução e Ambiente", 2: "Variáveis e Tipos", 3: "Operações Matemáticas",
        4: "Condicionais", 5: "Loops (For, While)", 6: "Funções",
        7: "Manipulação de Arquivos", 8: "Introdução ao Pandas"
    }
    
    col_nav, col_cont = st.columns([1, 4])
    
    with col_nav:
        st.subheader("Trilha")
        escolha = st.radio("Selecione a aula:", [f"{i}. {name}" for i, name in modulos.items()])
        mod_id = int(escolha.split(".")[0])

    with col_cont:
        if mod_id > st.session_state.progresso:
            st.warning(f"🔒 **Módulo Bloqueado.** Você precisa concluir o módulo {st.session_state.progresso} para acessar este.")
            st.image("https://cdn-icons-png.flaticon.com/512/565/565547.png", width=100)
        else:
            st.title(modulos[mod_id])
            
            # Carregamento do Notebook
            html_content = carregar_notebook(f"notebooks/modulo_{mod_id}.ipynb")
            components.html(html_content, height=750, scrolling=True)
            
            st.divider()
            if st.button("Concluir Módulo ✅"):
                if mod_id == st.session_state.progresso and mod_id < 8:
                    st.session_state.progresso += 1
                    st.toast(f"Módulo {mod_id} concluído!", icon='🎉')
                    st.rerun()
                elif mod_id == 8:
                    st.balloons()
                    st.success("✨ Sensacional! Você completou toda a jornada Python PET!")

# --- PÁGINA DE SUPORTE ---
elif menu == "Suporte ao Aluno":
    st.title("Ajuda e Materiais")
    st.markdown(f"""
    ### 📂 Arquivos para IDE Local
    Se você prefere usar o **VS Code**, **PyCharm** ou **Jupyter Lab**, faça o download de todos os módulos através do link abaixo:
    * [Clique aqui para abrir a pasta no Google Drive]({LINK_DRIVE})
    
    ### 🛠️ Problemas Técnicos?
    * **O módulo não carrega:** Certifique-se de que os arquivos `.ipynb` estão na pasta `/notebooks` do seu projeto.
    * **Progresso resetou:** O progresso é salvo apenas enquanto a aba do navegador estiver aberta. Em versões futuras, poderemos implementar login com banco de dados!
    """)