import locale
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.GoogleSheetManager import GoogleSheetManager
from utils.DateConverter import converter_data
from utils.Selectors import select_items
from streamlit_gsheets import GSheetsConnection

# get the url of google sheets
gs_manager = GoogleSheetManager()

url = st.secrets["product_url"]
sales_url = st.secrets["sales_url"]
inside_sales = st.secrets["inside_sales"]

##############################################################################################
##############################################################################################


# def select_client(df):
#     """Permite ao usuário selecionar clientes a partir de um DataFrame."""
#     client_options = df['BUYER'].unique()
#     selected_client = st.selectbox("Selecione um Cliente (opcional):", options=["Nenhum"] + list(client_options))
#     return selected_client

# def display_buyer_info(sales_df, products, clientes):
#     """Exibe informações sobre compradores e produtos selecionados."""
#     selected_items_df = select_items(products)
#     selected_item_ids = selected_items_df['ITEM_ID'].tolist()

#     if selected_item_ids:
#         selected_sales_df = sales_df[sales_df['ITEM_ID'].isin(selected_item_ids)]
#         if not selected_sales_df.empty:
#             buyers = selected_sales_df[['BUYER', 'ITEM_ID']].drop_duplicates()
#             buyer_info_df = clientes[clientes['BUYER'].isin(buyers['BUYER'].unique())]

#             if not buyer_info_df.empty:
#                 col1, col2 = st.columns(2)
#                 display_selected_products(col1, selected_items_df)
#                 display_buyer_details(col2, buyer_info_df)
#             else:
#                 st.warning("Nenhuma informação do cliente encontrada para os produtos selecionados.")
#         else:
#             st.warning("Nenhuma venda encontrada para os produtos selecionados.")
#     else:
#         st.warning("Nenhum produto selecionado.")

# def display_selected_products(col, items_df):
#     """Exibe informações dos produtos selecionados."""
#     col.write("Produtos selecionados:")
#     for _, row in items_df.iterrows():
#         col.markdown(f"""
#         **Produto:** {row['TITLE']}  
#         **ID do Item:** {row['ITEM_ID']}  
#         **Categoria:** {row['CATEGORY']}  
#         """)

# def display_buyer_details(col, buyer_info_df):
#     """Exibe detalhes dos compradores."""
#     col.write("Informações do cliente:")
#     for _, row in buyer_info_df.iterrows():
#         col.markdown(f"""
#         **Nome:** {row['BUYER']}  
#         **CPF:** {row['CPF']}  
#         **Cidade:** {row['CITY']}  
#         **Endereço:** {row['ADDRESS']}  
#         **Canal de Venda:** {row['CHANNEL']}  
#         """)

def sales_data_formatting(data):
    """Formata dados de vendas, anúncios e clientes."""
    vendas = data.iloc[:, 1:12]
    anuncios = data.iloc[:, 12:16]
    clientes = data.iloc[:, 16:]
    # clientes["REVENUE_BRL"] = vendas["PRODUCT_REVENUE_BRL"]
    # vendas['PRODUCT_REVENUE_BRL'].fillna(anuncios['UNIT_SALE_PRICE_BRL'], inplace=True)
    return vendas, anuncios, clientes

def display_sales_data(sales_df, products):
    """Exibe dados de vendas com e sem anúncios."""
    with st.expander("Vendas"):

        tab1, tab2 = st.tabs(["Com anúncio", "Sem anúncio"])

        with tab1:
            st.markdown("##### Vendas sem anúncio cadastrado")
            no_advertisement = sales_df[~sales_df['ITEM_ID'].isin(products['ITEM_ID'])].copy()
            display_sales(no_advertisement, products)

        with tab2:
            st.markdown("##### Vendas com anúncio cadastrado")
            with_advertisement = sales_df[sales_df['ITEM_ID'].isin(products['ITEM_ID'])].copy()
            display_sales(with_advertisement, products)
        st.markdown("---")
        st.dataframe(sales_df)

def display_sales(dataframe, df2):
    """Exibe informações de vendas formatadas."""
    dataframe = dataframe.iloc[:, [0,1,15,2,6,10,12]]
    # dataframe['PRODUCT_REVENUE_BRL'].fillna(df2['UNIT_SALE_PRICE_BRL'], inplace=True)
    # dataframe['PRODUCT_REVENUE_BRL'] = dataframe['PRODUCT_REVENUE_BRL'].apply(lambda x: f"R$ {x:,.2f}" if pd.notnull(x) else 'R$ 0.00')
    st.dataframe(dataframe)

# def display_product_info(filtered_products):
#     """Exibe informações detalhadas dos produtos filtrados."""
#     for _, row in filtered_products.iterrows():
#         revenue = row['PRODUCT_REVENUE_BRL']
#         product_info = f"""
#         <div style="border:1px solid #ddd; padding:10px; margin-bottom:10px;">
#             <h4>Produto: {row['TITLE']}</h4>
#             <p><strong>Categoria:</strong> {row['CATEGORY']}</p>
#             <p><strong>Descrição:</strong> {row.get('DESCRIPTION', 'N/A')}</p>
#             <p><strong>ID do Item:</strong> {row['ITEM_ID']}</p>
#             <p><strong>Data da Compra:</strong> {row.get('SALE_DATE', 'N/A')}</p>
#             <p><strong>Receita:</strong> R$ {revenue:.2f}</p>
#         </div>
#         """
#         st.markdown(product_info, unsafe_allow_html=True)
st.write("Vendas por plataforma")
if url:
    # Set up Google Sheets manager
    gs_manager.set_url(url)
    gs_manager.set_url(sales_url)
    gs_manager.set_url(inside_sales)

    # groups worksheets
    gs_manager.add_worksheet(sales_url,"VENDAS")
    gs_manager.add_worksheet(inside_sales,"vendas")


    # products worksheets
    gs_manager.add_worksheet(url, "ANUNCIOS")
    gs_manager.add_worksheet(url, "CATEGORIAS")
    gs_manager.add_worksheet(url, "CONDITIONS")
    gs_manager.add_worksheet(url, "IMAGENS")

    # Read worksheets
    products = gs_manager.read_sheet(url, "ANUNCIOS")
    categorias = gs_manager.read_sheet(url, "CATEGORIAS")
    conditions = gs_manager.read_sheet(url, "CONDITIONS")
    imgs = gs_manager.read_sheet(url, "IMAGENS")
    sales = gs_manager.read_sheet(sales_url, "VENDAS")  
    inside_sales = gs_manager.read_sheet(inside_sales, "vendas")


    vendas, anuncios, clientes = sales_data_formatting(sales)
    sales_df = pd.concat([vendas, anuncios, clientes], axis=1)


    search_term = st.text_input("Buscar Venda plataforma por Nome do Produto:")
    if search_term:
        search_results = sales_df[sales_df['TITLE'].str.contains(search_term, case=False, na=False)]
        display_sales(search_results,  anuncios)
        # print(search_results.info())
        # st.write(search_results.info())



# Seleção de intervalo de datas com verificação
date_range = st.date_input(
    "Selecione o intervalo de datas:",
    value=[datetime.today(), datetime.today()],  # Use uma lista para um intervalo
    key="date_range"
)



# Verifique se foram selecionadas exatamente duas datas
if len(date_range) == 2:
    start_date, end_date = date_range
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Garantir que 'Data da venda' está no formato datetime no DataFrame
    if 'Data da venda' in sales_df.columns:
        sales_df['Data da venda'] = pd.to_datetime(sales_df['Data da venda'], errors='coerce')

        # Filtrar o DataFrame de vendas pelo intervalo de datas
        filtered_sales = sales_df[
            (sales_df['Data da venda'] >= start_date) & 
            (sales_df['Data da venda'] <= end_date)
        ]

        # Exibir os dados filtrados
        if not filtered_sales.empty:
            display_sales(filtered_sales, anuncios)
        else:
            st.warning("Nenhuma venda encontrada no intervalo de datas selecionado.")
    else:
        st.error("Erro: A coluna 'Data da venda' não foi encontrada no DataFrame.")
else:
    st.error("Por favor, selecione tanto a data de início quanto a data de fim para o intervalo.")

with st.expander("Vendas Internas"):

    st.dataframe(inside_sales)