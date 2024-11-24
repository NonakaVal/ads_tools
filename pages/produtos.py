import numpy as np
import streamlit as st
from utils.GoogleSheetManager import GoogleSheetManager
from utils.AplyFilters import apply_filters
from utils.AplyPandas import format_data, format_prices

from utils.AplyClassifications import classify_editions, classify_items, get_condition, get_categories_ID, get_imgs

# Initialize connection to Google Sheets
# conn = st.connection("gsheets", type=GSheetsConnection)

##############################################################################################
##############################################################################################

# get the url of google sheets
gs_manager = GoogleSheetManager()
url = st.secrets["product_url"]
to_send_url = st.secrets["to_send_url"]

##############################################################################################
##############################################################################################

if url:
    # Set up Google Sheets manager
    gs_manager.set_url(url)

    # products worksheets
    gs_manager.add_worksheet(url, "ANUNCIOS")
    gs_manager.add_worksheet(url, "CATEGORIAS")
    gs_manager.add_worksheet(url, "IMAGENS")

    # Read worksheets
    products = gs_manager.read_sheet(url, "ANUNCIOS")
    categorias = gs_manager.read_sheet(url, "CATEGORIAS")
    imgs = gs_manager.read_sheet(url, "IMAGENS")

    data = products.copy()

    data = get_categories_ID(products, categorias)
    data = get_imgs(data, imgs)
    data = classify_items(data)
    data = classify_editions(data)
    filtered = apply_filters(data, categorias)
    data = format_data(filtered)
    data = format_prices(data)

    # Adiciona coluna de URL para exibição nos links
    data['URL'] = data.apply(
        lambda row: f"https://www.collectorsguardian.com.br/{row['ITEM_ID'][:3]}-{row['ITEM_ID'][3:]}-{row['TITLE'].replace(' ', '-').lower()}-_JM#item_id={row['ITEM_ID']}", 
        axis=1
    )

    # Opções de colunas disponíveis para exibição
    all_columns = data.columns.tolist()
    default_columns = ['IMG', 'ITEM_ID', 'SKU'  ,'TITLE',  'MSHOPS_PRICE', 'QUANTITY',  'URL', "STATUS"]

    # Widget multiselect para escolher as colunas
    selected_columns = st.multiselect(
        "Selecione as colunas para exibição:",
        options=all_columns,
        default=default_columns,
    )

    # Garantir que a ordem das colunas seja respeitada
    data = data[selected_columns]

    # Display dataframe com as colunas selecionadas
    st.dataframe(
        data, 
        column_config={
            "URL": st.column_config.LinkColumn(display_text="Editar Anúncio"),
            "IMG": st.column_config.ImageColumn(
                "Preview", help="Streamlit app preview screenshots", width=150
            )
        }
    )

    # Calculando totais
    total_quantity = filtered['QUANTITY'].sum().astype(int)
    total_value = filtered['MSHOPS_PRICE'].sum()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Quantidade Total de Itens", total_quantity)
    with col2:
        st.metric("Valor Total dos Itens (R$)", f"{total_value:,.2f}")
