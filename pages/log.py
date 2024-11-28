import streamlit as st
from langchain.agents import AgentType
from utils.AplyFilters import apply_filters
from langchain.chat_models import ChatOpenAI
from utils.GoogleSheetManager import GoogleSheetManager
from utils.AplyPandas import format_data, format_prices
from langchain.callbacks import StreamlitCallbackHandler
from langchain_experimental.agents import create_pandas_dataframe_agent
from utils.AplyClassifications import classify_editions, classify_items, get_condition, get_categories_ID, get_imgs

##############################################################################################
##############################################################################################

# get the url of google sheets
gs_manager = GoogleSheetManager()
url = "https://docs.google.com/spreadsheets/d/1gq1sgOmUDyU5hn5P5BYWzqQ2I8RuB2Al-NzaMYIq-Jg/edit?usp=sharing"

##############################################################################################
##############################################################################################

if url:
    # Set up Google Sheets manager
    gs_manager.set_url(url)

    # products worksheets
    gs_manager.add_worksheet(url, "EDICOES")
    gs_manager.add_worksheet(url, "CONTROLES")
    # gs_manager.add_worksheet(url, "IMAGENS")
    # gs_manager.add_worksheet(url, "CONDITIONS")

    # Read worksheets
    products = gs_manager.read_sheet(url, "EDICOES")
    controles = gs_manager.read_sheet(url, "CONTROLES")
    # imgs = gs_manager.read_sheet(url, "IMAGENS")
    # conditions = gs_manager.read_sheet(url, "CONDITIONS")


##############################################################################################
##############################################################################################



    # st.dataframe(
    #     data,
    #     column_config={
    #         "IMG": st.column_config.ImageColumn(
    #             "Preview", help="Preview da imagem", width='small'
    #         )
    #     }, use_container_width=True
        
    # )

##############################################################################################
##############################################################################################


# Exibição da galeria

# Define o número de colunas por linha
cols_per_row = 10

# Cria as colunas dinamicamente
rows = [products.iloc[i:i+cols_per_row] for i in range(0, len(products), cols_per_row)]

for row in rows:
    cols = st.columns(cols_per_row)
    for col, (_, item) in zip(cols, row.iterrows()):
        with col:
            st.image(item["IMG"], caption=item["TITLE"], width=100)


st.divider()

rows = [controles.iloc[i:i+cols_per_row] for i in range(0, len(controles), cols_per_row)]

for row in rows:
    cols = st.columns(cols_per_row)
    for col, (_, item) in zip(cols, row.iterrows()):
        with col:
            st.image(item["IMG"], caption=item["TITLE"], width=50)