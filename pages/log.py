import random
from io import BytesIO
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
from barcode.codex import Code128
from barcode.writer import ImageWriter
import os  # Para manipular diretórios e arquivos
from utils.LoadDataFrame import load_and_process_data

from utils.GoogleSheetManager import GoogleSheetManager
from utils.Selectors import select_items

##############################################################################################
# Inicializar a conexão com o Google Sheets
##############################################################################################

st.write("Tabela de Consulta")

# Em algum lugar no seu código
data = load_and_process_data()

##############################################################################################

select = select_items(data)

##############################################################################################
##############################################################################################
st.write("")

if not select.empty:

    # Calcula o número total de itens
    total_items = select['CATEGORY'].value_counts().sum()
    st.write(f"Total de Itens: {total_items}")

    # Exibe o resumo
    # st.markdown(f"#### Resumo")
    # # Criação de colunas para exibição das tabelas e resumo
    # col1, col2, col3, col4, col5 = st.columns(5)

    # # Coluna 1: Informações de preço e total de itens
    # with col1:
    #     st.markdown(f"**Total de Itens:** {total_items}")
    #     # Soma total dos preços e formatação
    #     price_counts = select["MSHOPS_PRICE"].sum().astype(int)
    #     formatted_price = f"R$ {price_counts:,.2f}"

    #     # Exibe o valor total e o total de itens
    #     st.markdown(f"**Valor Total:**\n **{formatted_price}**")
        

    #     # Adiciona um divisor visual
    #     st.divider()

    # Colunas 2 a 5: Exibição de contagens de categorias
    # for col, label, data in zip([col2, col3, col4, col5], 
    #                             ["Categorias", "Subcategorias", "Edições", "Condições"], 
    #                             ["CATEGORY", "SUBCATEGORY", "EDITION", "CONDITION"]):
    #     with col:
    #         st.markdown(f"**{label}**")
    #         # Conta os valores únicos de cada categoria e transforma em uma tabela HTML
    #         counts = select[data].value_counts().reset_index()
    #         counts.columns = [label[:-1], 'Total']  # Remove 's' do final do label para singular
    #         counts_html = counts.to_html(index=False, header=False, escape=False, justify='left', border=0)     
            
    #         # Exibe a tabela no formato HTML
    #         st.markdown(counts_html, unsafe_allow_html=True)
    #     # Seleção de categoria para atualização de tabela
    
    # st.sidebar.divider()
    # st.sidebar.warning("Ao subir a tabela atual, todos os valores serão substituídos.")
    # category = st.radio("Selecione para subir a tabela para Google Sheets", ["Essentials", "Prime", "Leilões"])
    

    
    # # Verifica a categoria selecionada e faz o upload correspondente
    # if category == "Essentials":
    #     update_worksheet(select, "ESSENCIALS", 4, to_send_url)
    # elif category == "Prime":
    #     update_worksheet(select, "PRIME", 5, to_send_url)
    # elif category == "Leilões":
    #     update_worksheet(select, "LEILOES", 6, to_send_url)



##############################################################################################
##############################################################################################
        
        # Create tabs for different data views


#     st.divider()
#     st.markdown("##### 🔍 Tabela de")
#     st.markdown("""
#                 - Para ordenar os valores basta clicar no nome da coluna.
#                 - Na parte superior direita da tabela é possível expandir e pesquisar valores.
#                 - Clique na imagem para ampliar.
#                 - Filtros estão na barra lateral esquerda,
#                 """)

#     # Display filtered DataFrame with link column
#     st.dataframe(
#     renamed_df, 
#     column_config={"URL": st.column_config.LinkColumn( display_text="Editar Anúncio"),
#                    "IMG": st.column_config.ImageColumn(
#                       "Preview ", help="Streamlit app preview screenshots", width=110
#         )})


# # Initial display mode flag
#     # if 'edit_mode' not in st.session_state:
#     #     st.session_state.edit_mode = False

#     # # Button to toggle between display modes
#     # if st.button("Switch to Edit Mode" if not st.session_state.edit_mode else "Switch to View Mode"):
#     #     st.session_state.edit_mode = not st.session_state.edit_mode

#     # # Logic to switch between views
#     # if st.session_state.edit_mode:
#     #     edited_df = st.data_editor(renamed_df)
#     #     st.write("Data edited successfully!")
#     # else:
#     #     st.dataframe(
#     #         renamed_df, 
#     #         column_config={
#     #             "URL": st.column_config.LinkColumn(display_text="Acessar Anúncio"),
#     #             "IMG": st.column_config.ImageColumn(
#     #                 "Preview", help="Streamlit app preview screenshots", width=110
#     #             )
#     #         }
#     #     )

#     st.divider()




#     # st.divider()

#     # # Display total quantity of items
#     # total_quantity = filtered['QUANTITY'].sum().astype(int)
#     # st.write(f"##### **Total de Itens Filtrados:** {total_quantity}")

#     # price_counts = filtered["MSHOPS_PRICE"].sum().astype(int)
#     # formatted_price = f"**Valor total dos itens Filtrados R$ {price_counts:,.2f}**"
#     # st.write(f"##### {formatted_price}")

#     # st.divider()

#     # # Create columns for organized displa

#     # # Criar as colunas para exibir os dados
#     # col1, col2, col3, col4 = st.columns(4)

#     # # Exibir as categorias
#     # with col1:
#     #     display_column_data(filtered, 'CATEGORY', "Categorias (Não Filtrado)")

#     # # Exibir as subcategorias
#     # with col2:
#     #     display_column_data(filtered, 'SUBCATEGORY', "Subcategorias (Filtrado)")

#     # # Exibir as condições
#     # with col3:
#     #     display_column_data(filtered, 'CONDITION', "Condições (Filtrado)")

#     # # Exibir os status
#     # with col4:
#     #     display_column_data(filtered, 'STATUS', "Status (Filtrado)")



#     # st.divider()
