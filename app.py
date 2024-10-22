import streamlit as st


st.set_page_config(page_title="collectorsguardian", page_icon="🎮", layout='wide')
# Navegação de páginas

# Navegação de páginas
home = st.Page("pages/home.py", title="Home", icon=":material/home:", default=True)
update = st.Page("pages/update.py", title="Update", icon=":material/update:")
stream = st.Page("pages/stream.py", title="Stream", icon=":material/dashboard:")
# new = st.Page("pages/new.py", title="New", icon=":material/dashboard:")
# update = st.Page("pages/update.py", title="Update", icon=":material/dashboard:")
# qtd = st.Page("pages/qtd.py", title="Quantidade", icon=":material/dashboard:")
# sales = st.Page("pages/sales.py", title="Sales", icon=":material/dashboard:")

# test =  st.Page("pages/test.py", title="Test", icon=":material/dashboard:")
# test2 =  st.Page("pages/test2.py", title="Test 2", icon=":material/dashboard:")
# labels = st.Page("pages/labels.py", title="Etiquetas Simples", icon=":material/dashboard:")
# inventario = st.Page("pages_controle/inventario_itens_de_envio.py", title="Inventario", icon=":material/history:")
# labels = st.Page("pages_controle/labels.py", title="Gerar Etiquetas Simples", icon=":material/dashboard:")
st.write("atualizado 22-10-24")
anuncio = st.Page("pages/ad_selector.py", title="Criar Seleção de Produtos", icon=":material/dashboard:")
# Configuração das páginas
pg = st.navigation(
    {
        # "Controle": [], 
        # "Home" : [home],
        "": [],
        "": [home, anuncio],
      
        
    }
)

pg.run()


# import streamlit as st
# import mysql.connector
# from tools.app_config import login, logout


# # Configuração da página do Streamlit
# st.set_page_config(page_title="collectorsguardian", page_icon="📦")

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False


# # Navegação de páginas
# login_page = st.Page(login, title="Log in", icon=":material/login:")
# logout_page = st.Page(logout, title="Log out", icon=":material/logout:")


# # chat = st.Page("consultas/Chat.py", title="Agente AI", icon=":material/bug_report:")
# home = st.Page("pages_controle/home.py", title="Home", icon=":material/home:", default=True)
# consulta = st.Page("pages_produtos/search_product.py", title="Buscar", icon=":material/search:")
# product_table = st.Page("pages_produtos/table_products.py", title="Tabela de produtos", icon=":material/dashboard:")
# new_product = st.Page("pages_produtos/new_product.py", title="Registrar e Atualizar", icon=":material/dashboard:")
# inventario = st.Page("pages_controle/inventario_itens_de_envio.py", title="Inventario", icon=":material/history:")
# historico = st.Page("pages_controle/historico.py", title="Historico de Atividades", icon=":material/history:")

# # Estabeleça uma conexão com o servidor MySQL usando os secrets do Streamlit
# try:
#     mydb = mysql.connector.connect(
#         host=st.secrets["DB_HOST"],
#         user=st.secrets["DB_USER"],
#         password= st.secrets["DB_PASSWORD"],
#         database=st.secrets["DB_DATABASE"]
#     )
#     mycursor = mydb.cursor()
#     # st.info("Conexão Estabelecida")
# except mysql.connector.Error as err:
#     st.error(f"Erro ao conectar ao banco de dados: {err}")



# # Configuração das páginas
# if st.session_state.logged_in:
#     pg = st.navigation(
#         {
#             "Account":  [logout_page, home],
#             "Produtos": [product_table, consulta, new_product],
#             "Controle": [inventario, historico], 
#         }
#     )
# else:
#     pg = st.navigation([login_page])

# pg.run()