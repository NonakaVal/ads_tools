import streamlit as st
import pandas as pd
import os
from utils.GoogleSheetManager import GoogleSheetManager, update_worksheet
from utils.UpdateFunctions import data_normalization, compare_dataframes, fill_sku_from_df1
from utils.UploadFile import load_data, file_formats
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)
def update_worksheet(df, worksheet_title, key, url, button_text="Enviar lista"):
    if st.button(button_text, key=key):
        # url = st.secrets["url"]
        conn.update(spreadsheet=url, worksheet=worksheet_title, data=df)
        st.success("Subir itens para tabela 🤓")

# Inicializando o gerenciador de planilhas
gs_manager = GoogleSheetManager()
url = st.secrets["product_url"]
col1, col2 = st.columns(2)

with col1:
    st.write("Atualizar Dados internos pela tabela de Anúncios do mercadolivre ")
    st.write("##### [Baixar Tabela](https://www.mercadolivre.com.br/anuncios/edicao-em-excel) ↩️ ")
    st.markdown("""
- Itens adicionados e removidos, 
- Precos e quantidades alterados, 
- Status alterado
                """)
    
with col2:   
    uploaded_file = st.file_uploader("Envie o arquivo do Google Sheets para 'Anúncios'", type=["csv", "xls", "xlsx", "xlsm", "xlsb"])



if uploaded_file:
    # Lendo dados do arquivo carregado
    data_ml = load_data(uploaded_file)
    
    # Configurando o gerenciador de planilhas e lendo dados de produtos
    gs_manager.set_url(url)
    gs_manager.add_worksheet(url, "CATEGORIAS")
    gs_manager.add_worksheet(url, "ANUNCIOS")
    products = gs_manager.read_sheet(url, "ANUNCIOS")

    # Normalizando e mesclando dados
    data_ml = data_normalization(data_ml)
    products = data_normalization(products)
    data = fill_sku_from_df1(products, data_ml)

    st.divider()
    st.write("###### Resumo")
    # Comparando DataFrames e obtendo totais
    items_added, items_removed, price_changes, quantity_changes, status_changes, total_price_active, total_quantity_active = compare_dataframes(data_ml, products)

    # Exibindo os resultados no Streamlit
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Itens Adicionados")
        st.dataframe(items_added)
    with col2:
        st.write("Itens Removidos")
        st.dataframe(items_removed)

    col1, col2 = st.columns(2)
    with col1:
        st.write("Alterações de Quantidade")
        st.dataframe(quantity_changes[['ITEM_ID', 'TITLE', 'QUANTITY_novo', 'QUANTITY_antigo']])
    with col2:
        st.write("Mudanças de Preço")
        st.dataframe(price_changes[['ITEM_ID', "TITLE", 'MSHOPS_PRICE_novo', 'MSHOPS_PRICE_antigo', 'MARKETPLACE_PRICE_novo', 'MARKETPLACE_PRICE_antigo']])

    col1, col2 = st.columns(2)
    

    with col1:

        st.metric(label="Total MSHOPS_PRICE (Ativos)", value=f"R$ {total_price_active:,.2f}")
        st.metric(label="Total Quantidade (Ativos)", value=f"{total_quantity_active:,}")

    with col2:
        st.write("Itens Adicionados")
        st.metric(label="Total de Itens Adicionados", value=f"{len(items_added)}")

    st.divider()    
    edited_df = st.data_editor(data)
    st.divider()    
    # Atualizando os dados no Google Sheets
    st.divider()    
    update_worksheet(data, 'ANUNCIOS', 1, url=url)
    st.divider()    

