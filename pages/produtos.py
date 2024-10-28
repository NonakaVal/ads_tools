import numpy as np
import streamlit as st
from utils.GoogleSheetManager import GoogleSheetManager, update_worksheet
from utils.AplyPandas import get_categories_ID, get_condition, get_imgs, display_column_data
from utils.AplyFilters import apply_filters
from utils.Selectors import select_items
from utils.AplyClassifications import classify_editions, classify_items
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
import plotly.graph_objects as go
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
    gs_manager.set_url(to_send_url)

    # groups worksheets
    gs_manager.add_worksheet(to_send_url,"ESSENCIALS")
    gs_manager.add_worksheet(to_send_url,"PRIME")
    gs_manager.add_worksheet(to_send_url,"LEILOES")

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

##############################################################################################
##############################################################################################

# set dataframes and get informations

    data = get_categories_ID(products, categorias)
    data = classify_items(data)
    data = classify_editions(data)
    data = get_condition(data, conditions)
    data = get_imgs(data, imgs)
    # st.markdown("## Pagina feita para criar lista de seleção de produtos para criação de postagens de anúncios ")

##############################################################################################
##############################################################################################
    with st.sidebar.expander("Links"):

        st.markdown("""
                    

                    
                
                    
    

                - 🤖  [Link do Chat Configurado](https://chatgpt.com/share/6717d5fd-07f8-8007-a32f-a232bae7d170) 
                    
                -  [Link Tabela Google Sheets](https://docs.google.com/spreadsheets/d/1aCRdnOEFD_x4NDSwj6SBfZXJBdPAEJjCvfX-n4PKCsE/edit?usp=sharing)
                

        
                
                    """)

##############################################################################################
##############################################################################################

    # with st.sidebar.expander("Ajuda"):
    #     st.markdown("""
    
    #         - **Status:** Ativo ou Inativo com base na data de atualização.
    #         - **Categorias Mercado Livre:** Categorias específicas criadas pelo Mercado Livre.
    #         - **Subcategorias:** Subcategorias específicas criadas no sistema.
    #         - **Condições:**:                    
    #         [Acessar Sistema de Condição de Produtos](https://share.note.sx/c7iihkct#OdTU3s9gCjJe+GF03Ff3SZct+sI/iTJsd4+EyVkCz4I)

    #         - **Edições:** Sistema de Classificação de diferentes Edições.

    #     """, unsafe_allow_html=True)

##############################################################################################
##############################################################################################    

    # im not considerig the variables of the product
    data['SKU'] = data['SKU'].where(~data['SKU'].duplicated(), np.nan)
    data['STATUS'] = data['STATUS'].str.strip()
    data = data.drop_duplicates(subset='ITEM_ID', keep='first')
    
    # Apply filters to the data
    filtered = apply_filters(data, categorias)

    # cant think in better solution to rename columns just for display, should i fix it?
    renamed_df = filtered.rename(columns={
        'ITEM_ID': 'ID_DO_ITEM',
        'SKU': 'SKU',
        'TITLE': 'TÍTULO',
        'DESCRIPTION': 'DESCRIÇÃO',
        'MSHOPS_PRICE': 'PREÇO_MSHOPS',
        'MARKETPLACE_PRICE': 'PREÇO_MARKETPLACE',
        'CATEGORY': 'CATEGORIA',
        'STATUS': 'STATUS',
        'QUANTITY': 'QUANTIDADE', 
        "CONDITION": "CONDICÃO",
    })

    # not sure why i aways need to change this array as wll the get link list , but it works, for now


    renamed_df = renamed_df[["IMG", "ID_DO_ITEM", "SKU",  "TÍTULO", "PREÇO_MSHOPS", "URL", "DESCRIÇÃO", "STATUS",  "QUANTIDADE", "CONDICÃO"]]
    st.divider()    

##############################################################################################
##############################################################################################

##############################################################################################
##############################################################################################
            
            # Create tabs for different data views



    st.markdown("""
                - Para ordenar os valores basta clicar no nome da coluna.
                - Na parte superior direita da tabela é possível expandir e pesquisar valores.
                - Clique na imagem para ampliar.
                - Filtros estão na barra lateral esquerda,
                """)

    # Display filtered DataFrame with link column
    st.dataframe(
    renamed_df, 
    column_config={"URL": st.column_config.LinkColumn( display_text="Editar Anúncio"),
                   "IMG": st.column_config.ImageColumn(
                      "Preview ", help="Streamlit app preview screenshots", width=110
        )})



    # Calculando totais
    total_quantity = renamed_df['QUANTIDADE'].sum().astype(int)
    total_value = renamed_df['PREÇO_MSHOPS'].sum()

    # Renomear colunas para exibição
    renamed_df = data.rename(columns={
        'ITEM_ID': 'ID_DO_ITEM',
        'SKU': 'SKU',
        'TITLE': 'TÍTULO',
        'MSHOPS_PRICE': 'PREÇO_MSHOPS',
        'CATEGORY': 'CATEGORIA',
        'STATUS': 'STATUS',
        'QUANTITY': 'QUANTIDADE', 
        'CONDITION': 'CONDICÃO'
    })

    # Exibir totais no dashboard
    st.subheader("Visão Geral dos Produtos")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Quantidade Total de Itens", total_quantity)
    with col2:
        st.metric("Valor Total dos Itens (R$)", f"{total_value:,.2f}")


    # renamed_df_C = renamed_df[renamed_df['CONDICÃO'] != '-']

    # fig_status = px.pie(
    #     renamed_df_C, 
    #     names='CONDICÃO', 
    #     title="Distribuição de Produtos por Condição",
    #     values='QUANTIDADE',
    #     color_discrete_sequence=px.colors.qualitative.Pastel
    # )
    # st.plotly_chart(fig_status)
    # # Gráficos

    
    # st.divider()


    
    # Create columns for organized displa

    # Criar as colunas para exibir os dados
    col1, col2, col3, col4 = st.columns(4)

    # Exibir as categorias
    with col1:
        display_column_data(filtered, 'CATEGORY', "Categorias (Não Filtrado)")

    # Exibir as subcategorias
    with col2:
        display_column_data(filtered, 'SUBCATEGORY', "Subcategorias (Filtrado)")

    # Exibir as condições
    with col3:
        display_column_data(filtered, 'CONDITION', "Condições (Filtrado)")

    # Exibir os status
    with col4:
        display_column_data(filtered, 'STATUS', "Status (Filtrado)")



    st.divider()
