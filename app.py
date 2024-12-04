import streamlit as st


st.set_page_config(page_title="collectorsguardian", page_icon="🎮", layout='wide')
# Navegação de páginas

# Navegação de páginas
home = st.Page("pages/home.py", title="Home", icon=":material/home:", default=True)
produts = st.Page("pages/products.py", title="Consultar Produtos", icon=":material/dashboard:")
anuncio_select = st.Page("pages/item_selector.py", title="Criar Seleção de Produtos", icon=":material/dashboard:")


labels = st.Page("pages/labels.py", title="Etiquetas Simples", icon=":material/dashboard:")


# update = st.Page("pages/update.py", title="Update", icon=":material/update:")
# stream = st.Page("pages/stream.py", title="Stream", icon=":material/dashboard:")
# sales = st.Page("pages/sales_by_product.py", title="Pesquisar Venda", icon=":material/dashboard:")
# edit_sales = st.Page("pages/update_sales.py", title="Editar Venda", icon=":material/dashboard:")


log = st.Page("pages/log.py", title="TestLog", icon="⚙️")

# new = st.Page("pages/new.py", title="New", icon=":material/dashboard:")
update = st.Page("pages/update.py", title="Atualizar com tabela", icon=":material/dashboard:")
# qtd = st.Page("pages/qtd.py", title="Quantidade", icon=":material/dashboard:")
# sales = st.Page("pages/sales.py", title="Sales", icon=":material/dashboard:")

# test =  st.Page("pages/test.py", title="Test", icon=":material/dashboard:")
# test2 =  st.Page("pages/test2.py", title="Test 2", icon=":material/dashboard:")
# labels = st.Page("pages/labels.py", title="Etiquetas Simples", icon=":material/dashboard:")
# inventario = st.Page("pages_controle/inventario_itens_de_envio.py", title="Inventario", icon=":material/history:")
# labels = st.Page("pages_controle/labels.py", title="Gerar Etiquetas Simples", icon=":material/dashboard:")
st.write("atualizado 04-12-24")
anuncio_select = st.Page("pages/item_selector.py", title="Criar Seleção de Produtos", icon=":material/dashboard:")
# Configuração das páginas
pg = st.navigation(
    {
        # "Controle": [], 
        # "Home" : [home],
        "": [home],
        "Produtos": [produts],
        "Sistema": [update],
        "TestLog": [labels],
        # "Controle": [update],
      
        
    }
)

pg.run()

