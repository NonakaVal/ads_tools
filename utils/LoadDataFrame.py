import pandas as pd
import streamlit as st
from langchain.agents import AgentType
from utils.AplyFilters import apply_filters
from langchain.chat_models import ChatOpenAI
from utils.GoogleSheetManager import GoogleSheetManager
from utils.AplyPandas import format_data, format_prices
from langchain.callbacks import StreamlitCallbackHandler
from langchain_experimental.agents import create_pandas_dataframe_agent
from utils.AplyClassifications import classify_items, get_condition, get_categories_ID

def load_and_process_data():
    # Get the url of Google Sheets
    gs_manager = GoogleSheetManager()
    url = st.secrets["product_url"]

    if url:
        # Set up Google Sheets manager
        gs_manager.set_url(url)

        # products worksheets
        gs_manager.add_worksheet(url, "ANUNCIOS")
        gs_manager.add_worksheet(url, "CATEGORIAS")
        gs_manager.add_worksheet(url, "IMAGENS")
        gs_manager.add_worksheet(url, "CONDITIONS")

        # Read worksheets
        products = gs_manager.read_sheet(url, "ANUNCIOS")
        categorias = gs_manager.read_sheet(url, "CATEGORIAS")
        imgs = gs_manager.read_sheet(url, "IMAGENS")
        conditions = gs_manager.read_sheet(url, "CONDITIONS")

        # Prepare data
        data = products.copy()

        # Renomeando as colunas para exibição em português (se necessário)
        # data.rename(
        #     columns={
        #         "IMG": "Imagem",
        #         "ITEM_ID": "ID do Item",
        #         "SKU": "Código SKU",
        #         "TITLE": "Título",
        #         "MSHOPS_PRICE": "Preço MercadoShops",
        #         "QUANTITY": "Quantidade",
        #         "STATUS": "Status",
        #         "URL": "Link",
        #         "ITEM_LINK": "LinkEdit",
        #         "CATEGORY": "Categoria",
        #         "CONDITION": "Condição",
        #         "DESCRIPTION": "Descrição",
        #         "MARKETPLACE_PRICE": "Preço MercadoLivre",
        #     },
        #     inplace=True,
        # )

        # Processar a exibição das colunas
        all_columns = data.columns.tolist()
        default_columns = ['IMG', 'ITEM_ID', 'SKU', 'TITLE', 'MSHOPS_PRICE', 'QUANTITY', 'STATUS', 'URL', 'ITEM_LINK','CATEGORY', "DESCRIPTION"]

        # Widget multiselect para escolher as colunas
        selected_columns = st.sidebar.multiselect(
            "Selecione as colunas para exibição:",
            options=all_columns,
            default=default_columns,
        )

        # Garantir que a ordem das colunas seja respeitada
        select_data = data[selected_columns]
        select_data['MSHOPS_PRICE'] = select_data['MSHOPS_PRICE'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        
        # Aplicar filtros e categorizar
        select_data = apply_filters(select_data, categorias)

        return select_data
    else:
        st.error("URL do Google Sheets não configurada corretamente!")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro
