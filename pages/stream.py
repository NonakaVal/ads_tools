# import locale
# import streamlit as st
# import pandas as pd
# from utils.SalesFunctions import format_sales
# from utils.GoogleSheetManager import GoogleSheetManager, update_worksheet
# from utils.DateConverter import converter_data
# from utils.Selectors import select_items
# from streamlit_gsheets import GSheetsConnection

# # Configuração de locale para formatação de moeda
# locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# # Initialize connection to Google Sheets
# gs_manager = GoogleSheetManager()
# url = st.secrets.get("sales_url")

# def select_client(df):
#     """Permite ao usuário selecionar clientes a partir de um DataFrame."""
#     client_options = df['Comprador'].unique()
#     selected_client = st.selectbox("Selecione um Cliente (opcional):", options=["Nenhum"] + list(client_options))
#     return selected_client

# def display_selected_products(col, items_df):
#     """Exibe informações dos produtos selecionados."""
#     col.write("Produtos selecionados:")
#     for _, row in items_df.iterrows():
#         col.markdown(f"""
#         **Produto:** {row['TITLE']}  
#         **ID do Item:** {row['ITEM_ID']}  
  
#         """)

# def display_Comprador_info(sales_df, products, clientes):
#     """Exibe informações sobre compradores e produtos selecionados."""
#     selected_items_df = select_items(products)
#     selected_item_ids = selected_items_df['ITEM_ID'].tolist()

#     if selected_item_ids:
#         selected_sales_df = sales_df[sales_df['ITEM_ID'].isin(selected_item_ids)]
#         if not selected_sales_df.empty:
#             Compradors = selected_sales_df[['Comprador', 'ITEM_ID']].drop_duplicates()
#             Comprador_info_df = clientes[clientes['Comprador'].isin(Compradors['Comprador'].unique())]

#             if not Comprador_info_df.empty:
#                 col1, col2 = st.columns(2)
#                 display_selected_products(col1, selected_items_df)
#                 display_Comprador_details(col2, Comprador_info_df)
#             else:
#                 st.warning("Nenhuma informação do cliente encontrada para os produtos selecionados.")
#         else:
#             st.warning("Nenhuma venda encontrada para os produtos selecionados.")
#     else:
#         st.warning("Nenhum produto selecionado.")

# def display_Comprador_details(col, Comprador_info_df):
#     """Exibe detalhes dos compradores."""
#     col.write("Informações do cliente:")
#     for _, row in Comprador_info_df.iterrows():
#         col.markdown(f"""
#         **Nome:** {row['Comprador']}  
#         **CPF:** {row['CPF']}  
#         **Cidade:** {row['Cidade']}  
#         **Endereço:** {row['Endereço']}  
#         **Canal de Venda:** {row['CHANNEL']}  
#         """)

# def sales_data_formatting(data):
#     """Formata dados de vendas, anúncios e clientes."""
#     vendas = data.iloc[:, 1:11]
#     anuncios = data.iloc[:, 12:16]
#     clientes = data.iloc[:, 16:]
#     clientes["Receita por produtos (BRL)"] = vendas["Receita por produtos (BRL)"]

#     return vendas, anuncios, clientes

# def display_sales_data(sales_df, products):
#     """Exibe dados de vendas com e sem anúncios."""
#     with st.expander("Vendas"):

#         tab1, tab2 = st.tabs(["Com anúncio", "Sem anúncio"])

#         with tab1:
#             st.markdown("##### Vendas sem anúncio cadastrado")
#             no_advertisement = sales_df[~sales_df['ITEM_ID'].isin(products['ITEM_ID'])].copy()
#             display_sales(no_advertisement, products)

#         with tab2:
#             st.markdown("##### Vendas com anúncio cadastrado")
#             with_advertisement = sales_df[sales_df['ITEM_ID'].isin(products['ITEM_ID'])].copy()
#             display_sales(with_advertisement, products)
#         st.markdown("---")
#         st.dataframe(sales_df)

# def display_sales(dataframe, df2):
#     """Exibe informações de vendas formatadas."""
#     # dataframe = dataframe.iloc[:, [0,10, 11, 13, 14, 17, 18, 19, 21, 5]]

#     dataframe['Receita por produtos (BRL)'] = dataframe['Receita por produtos (BRL)'].apply(lambda x: f"R$ {x:,.2f}" if pd.notnull(x) else 'R$ 0.00')
#     st.dataframe(dataframe)

# def display_product_info(filtered_products):
#     """Exibe informações detalhadas dos produtos filtrados."""
#     for _, row in filtered_products.iterrows():
#         revenue = row['Receita por produtos (BRL)']
#         product_info = f"""
#         <div style="border:1px solid #ddd; padding:10px; margin-bottom:10px;">
#             <h4>Produto: {row['TITLE']}</h4>
#             <p><strong>Categoria:</strong> {row['CATEGORY']}</p>
#             <p><strong>Descrição:</strong> {row.get('DESCRIPTION', 'N/A')}</p>
#             <p><strong>ID do Item:</strong> {row['ITEM_ID']}</p>
#             <p><strong>Data da Compra:</strong> {row.get('Data da venda', 'N/A')}</p>
#             <p><strong>Receita:</strong> R$ {revenue:.2f}</p>
#         </div>
#         """
#         st.markdown(product_info, unsafe_allow_html=True)

# # If URL exists, initialize Google Sheets
# if url:
#     gs_manager.set_url(url)
#     gs_manager.add_worksheet(url, "VENDAS")
#     sales = gs_manager.read_sheet(url, "VENDAS")
#     sales['Data da venda'] = sales['Data da venda'].apply(converter_data)

#     vendas, anuncios, clientes = sales_data_formatting(sales)
#     sales_df = pd.concat([vendas, anuncios, clientes], axis=1)
#     display_sales_data(sales_df, anuncios)
#     display_Comprador_info(sales_df, anuncios, clientes)

#     # Displaying filtered data based on user selection
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         search_term = st.text_input("Buscar Venda por Nome do Produto:")
#     if search_term:
#         search_results = sales_df[sales_df['TITLE'].str.contains(search_term, case=False, na=False)]
#         display_sales(search_results,  anuncios)

#     with col2:

   
#         unique_ufs = clientes['UF'].unique()
#         selected_ufs = st.multiselect("Selecione um ou mais UFs:", unique_ufs)
#         filtered_clients = clientes[clientes['UF'].isin(selected_ufs)] if selected_ufs else clientes
#         filtered_clients['Receita por produtos (BRL)'] = filtered_clients['Receita por produtos (BRL)'].apply(lambda x: f"R$ {x:,.2f}" if pd.notnull(x) else 'R$ 0.00')

#     with col4:
#         selected_client = select_client(filtered_clients)
#         client_products = sales_df[sales_df['Comprador'] == selected_client] 
#         filtered_products = anuncios[anuncios['ITEM_ID'].isin(client_products['ITEM_ID'])].copy()
        
#     col1, col2 = st.columns(2)

#     with col1:
#         if not filtered_products.empty:
#             filtered_products = filtered_products.merge(
#                 sales_df[['ITEM_ID', 'Receita por produtos (BRL)', 'Data da venda']], 
#                 on='ITEM_ID', 
#                 how='left', 
#                 suffixes=('', '_sales')
#             )
#             filtered_products['Receita por produtos (BRL)'].fillna(0, inplace=True)
#             display_product_info(filtered_products)

#     with col2:
#         if not filtered_clients[filtered_clients['Comprador'] == selected_client].empty:
#             client_info = filtered_clients[filtered_clients['Comprador'] == selected_client].iloc[0]
#             client_details = f"""
#             <div style="border:1px solid #ddd; padding:10px; margin-bottom:10px;">
#                 <h4>Informações do Cliente: {client_info['Comprador']}</h4>
#                 <p><strong>CPF:</strong> {client_info['CPF']}</p>
#                 <p><strong>Cidade:</strong> {client_info['Cidade']}</p>
#                 <p><strong>Endereço:</strong> {client_info['Endereço']}</p>
#             </div>
#             """
#             st.markdown(client_details, unsafe_allow_html=True)

# else:
#     st.warning("URL dos segredos não fornecida.")
