import streamlit as st
import pandas as pd
from utils.SalesFunctions import format_sales
from utils.GoogleSheetManager import GoogleSheetManager, update_worksheet

# Uploader para o primeiro arquivo
uploaded_file = st.sidebar.file_uploader("Envie a tabela de vendas do Mercado Livre", type=["csv", "xls", "xlsx", "xlsm", "xlsb"], key="1")
uploaded_file2 = st.sidebar.file_uploader("Envie a tabela de vendas do Mercado Shops", type=["csv", "xls", "xlsx", "xlsm", "xlsb"], key="2")

# Processar o primeiro arquivo
if uploaded_file:
    ml = format_sales(uploaded_file, "Mercado Livre")

# Processar o segundo arquivo
if uploaded_file2:
    ms = format_sales(uploaded_file2,"Mercado Shops")

# Concatenar os dois DataFrames se ambos foram carregados
if uploaded_file and uploaded_file2:
    sales = pd.concat([ms, ml], ignore_index=True)
    st.dataframe(sales)

sales = sales[sales['Comprador'] != 'Eduardo Correa']

# Initialize connection to Google Sheets
# conn = st.connection("gsheets", type=GSheetsConnection)

##############################################################################################
##############################################################################################

# get the url of google sheets
gs_manager = GoogleSheetManager()
url = st.secrets["sales_url"]

##############################################################################################
##############################################################################################


if url:
    # Set up Google Sheets manager
    gs_manager.set_url(url)


    # Update the Google Sheet with the sales data
    if not sales.empty:
        update_worksheet(sales, "VENDAS", 7, url)
