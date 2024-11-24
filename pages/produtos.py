import numpy as np
import streamlit as st
from utils.GoogleSheetManager import GoogleSheetManager
from utils.AplyFilters import apply_filters
from utils.AplyPandas import format_data

from utils.AplyClassifications import classify_editions, classify_items, get_condition, get_categories_ID,  get_imgs, display_column_data

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
    # gs_manager.add_worksheet(url, "CONDITIONS")

    # Read worksheets
    products = gs_manager.read_sheet(url, "ANUNCIOS")
    categorias = gs_manager.read_sheet(url, "CATEGORIAS")
    imgs = gs_manager.read_sheet(url, "IMAGENS")
    
    # conditions = gs_manager.read_sheet(url, "CONDITIONS")


    # imgs = gs_manager.read_sheet(url, "IMAGENS")

    data = products.copy()

    # data['SKU'] = data['SKU'].where(~data['SKU'].duplicated(), np.nan)
    # data['STATUS'] = data['STATUS'].str.strip()
    # data = data.drop_duplicates(subset='ITEM_ID', keep='first')

    
    data = get_categories_ID(products, categorias)
    data = get_imgs(data, imgs)
    data = classify_items(data)
    data = classify_editions(data)
    filtered = apply_filters(data, categorias)
    data = format_data(filtered)

    data['URL'] = data.apply(
        lambda row: f"https://www.collectorsguardian.com.br/{row['ITEM_ID'][:3]}-{row['ITEM_ID'][3:]}-{row['TITLE'].replace(' ', '-').lower()}-_JM#item_id={row['ITEM_ID']}", 
        axis=1
    )
    # data = format_prices(data)
    # data = get_condition(data, conditions)

    # data['SKU'] = data['SKU'].str.replace('-', '', regex=False)

    # Display filtered DataFrame with link column
    # st.dataframe(data, 
    # column_config={"URL": st.column_config.LinkColumn( display_text="Anúncio")})

    # Display filtered DataFrame with link column
    st.dataframe(
    data, 
    column_config={"URL": st.column_config.LinkColumn( display_text="Editar Anúncio"),
                   "IMG": st.column_config.ImageColumn(
                      "Preview ", help="Streamlit app preview screenshots", width=150
        )})

    # st.dataframe(data)
    

    # Calculando totais
    total_quantity = filtered['QUANTITY'].sum().astype(int)
    total_value = filtered['MSHOPS_PRICE'].sum()


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
    # col1, col2, col3, col4, col5 = st.columns(5)

    # # Exibir as categorias
    # with col1:
    #     display_column_data(filtered, 'CATEGORY', "Categorias (Não Filtrado)")

    # # Exibir as subcategorias
    # with col2:
    #     display_column_data(filtered, 'SUBCATEGORY', "Subcategorias (Filtrado)")


    # # Exibir os status
    # with col3:
    #     display_column_data(filtered, 'STATUS', "Status (Filtrado)")



    # st.divider()