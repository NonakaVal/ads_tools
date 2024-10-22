import streamlit as st
from utils.GoogleSheetManager import GoogleSheetManager, update_worksheet
import pandas as pd

def data_normalization(data):
    data = data[["ITEM_ID", "SKU", "TITLE", "DESCRIPTION", 'MSHOPS_PRICE', 'MARKETPLACE_PRICE', 'CATEGORY', 'STATUS', 'QUANTITY']]
    data['MSHOPS_PRICE'] = data['MSHOPS_PRICE'].astype(float)
    data['MARKETPLACE_PRICE'] = data['MARKETPLACE_PRICE'].astype(float)
    data['STATUS'] = data['STATUS'].str.strip() 

    return data

def compare_dataframes(new_data, old_data):
    """
    Compara dois DataFrames e retorna as diferenças, incluindo:
    - Itens adicionados
    - Mudanças de preço (MSHOPS_PRICE e MARKETPLACE_PRICE)
    - Alterações de quantidade (QUANTITY)
    - Alterações de status (STATUS)
    """
    
    new_data['QUANTITY'] = new_data['QUANTITY'].fillna(0).astype(int)
    old_data['QUANTITY'] = old_data['QUANTITY'].fillna(0).astype(int)

    # Itens adicionados: presentes na tabela 1 (df1), mas não na tabela 2 (df2)
    items_added = new_data[~new_data['ITEM_ID'].isin(old_data['ITEM_ID'])]
    # Itens comuns: presentes em ambas as tabelas, para comparação de preços, quantidade e status
    common_items = pd.merge(new_data, old_data, on='ITEM_ID', suffixes=('_new', '_old'))
    
    # Mudanças de preço: verifica se os preços (MSHOPS_PRICE e MARKETPLACE_PRICE) mudaram
    price_changes = common_items[
        (common_items['MSHOPS_PRICE_new'] != common_items['MSHOPS_PRICE_old']) | 
        (common_items['MARKETPLACE_PRICE_new'] != common_items['MARKETPLACE_PRICE_old'])
    ]
    

    # Alterações de quantidade: verifica se a quantidade mudou
    quantity_changes = common_items[common_items['QUANTITY_new'] != common_items['QUANTITY_old']]
    
    # Alterações de status: verifica se o status mudou
    status_changes = common_items[common_items['STATUS_new'] != common_items['STATUS_old']]
    
    return items_added, price_changes, quantity_changes, status_changes


def format_prices(data):
    if 'MSHOPS_PRICE' in data.columns:
        data['MSHOPS_PRICE'] = pd.to_numeric(data['MSHOPS_PRICE'], errors='coerce')
        data['MSHOPS_PRICE'] = data['MSHOPS_PRICE'].apply(lambda x: f"R$ {x:,.2f}" if pd.notnull(x) else 'R$ 0.00')
    # Formatação de MARKETPLACE_PRICE
    if 'MARKETPLACE_PRICE' in data.columns:
        data['MARKETPLACE_PRICE'] = pd.to_numeric(data['MARKETPLACE_PRICE'], errors='coerce')
        data['MARKETPLACE_PRICE'] = data['MARKETPLACE_PRICE'].apply(lambda x: f"R$ {x:,.2f}" if pd.notnull(x) else 'R$ 0.00')
    return data

def fill_sku_from_df1(df_with_sku, df_without_sku):
    """
    Fill the SKU column in df_without_sku with values from df_with_sku based on ITEM_ID.
    Always use the SKU from df_with_sku where there is a matching ITEM_ID.

    Parameters:
    df_with_sku (pd.DataFrame): DataFrame containing 'ITEM_ID' and 'SKU'.
    df_without_sku (pd.DataFrame): DataFrame containing 'ITEM_ID' and SKU values.

    Returns:
    pd.DataFrame: Updated df_without_sku with SKU values filled from df_with_sku.
    """
    # Check if 'SKU' column exists in df_with_sku
    if 'SKU' not in df_with_sku.columns:
        print("SKU column not found in df_with_sku. Returning df_without_sku without modifications.")
        return df_without_sku

    # Merge df_without_sku with df_with_sku on ITEM_ID
    merged_data = df_without_sku.merge(df_with_sku[['ITEM_ID', 'SKU']], on='ITEM_ID', how='left', suffixes=('', '_from_df1'))

    # Update SKU in df_without_sku to always take from df_with_sku
    merged_data['SKU'] = merged_data['SKU_from_df1']

    # Drop the auxiliary column
    merged_data.drop(columns=['SKU_from_df1'], inplace=True)

    return merged_data

# Inicializando o gerenciador de planilhas
gs_manager = GoogleSheetManager()

# Permitindo que o usuário insira a URL1
url1 = st.text_input("Digite o link da primeira URL do Google Sheets:", "")
url2 = st.secrets["product_url"]

if url1:
    # Adicionando URLs ao gerenciador
    gs_manager.set_url(url1)
    gs_manager.set_url(url2)

    # Adicionando worksheets
    gs_manager.add_worksheet(url1, "Anúncios")
    gs_manager.add_worksheet(url2, "CATEGORIAS")
    gs_manager.add_worksheet(url2, "ANUNCIOS")

    # Lendo dados das worksheets
    products = gs_manager.read_sheet(url2, "ANUNCIOS")
    data_ml = gs_manager.read_sheet(url1, "Anúncios")
    data_ml = data_ml.iloc[5:]

    data_ml = data_normalization(data_ml)
    products = data_normalization(products)

    data = fill_sku_from_df1(products, data_ml) 
    
    st.divider()

    items_added, price_changes, quantity_changes, status_changes = compare_dataframes(data_ml,products)    

    st.dataframe(data)

    # st.write("Itens adicionados:")
    # st.dataframe(items_added.iloc[:,:6])
    # st.dataframe(price_changes)
    # st.write("Alterações de quantidade:")

    # st.dataframe(quantity_changes)
    # st.write("Alterações de status:")
    # st.dataframe(status_changes)

    # data_anuncios = gs_manager.read_sheet(url2, "products")
    # data_categorias = gs_manager.read_sheet(url2, "categorias")

    # # Comparando as tabelas de anúncios
    # items_added, price_changes, quantity_changes = compare_dataframes(data_ml, data_anuncios)
    # items_added = items_added.drop_duplicates(subset='ITEM_ID', keep='first')

    st.write("Itens Adicionados")
    st.dataframe(items_added)
    st.write("Mudanças de Preço")
    st.dataframe(price_changes[['ITEM_ID', 'TITLE_new', 'MSHOPS_PRICE_new', 'MSHOPS_PRICE_old', 'MARKETPLACE_PRICE_new', 'MARKETPLACE_PRICE_old']])
    st.write("Alterações de Quantidade")
    st.dataframe(quantity_changes[['ITEM_ID', 'TITLE_new', 'QUANTITY_new', 'QUANTITY_old']])

    # # Mesclando os dados dos dois conjuntos de anúncios
    # # Usando `how='outer'` para garantir que itens não sejam removidos
    # data = pd.merge(data_anuncios, data_ml, on=["ITEM_ID", "TITLE", "DESCRIPTION", 'MSHOPS_PRICE', 'MARKETPLACE_PRICE', 'CATEGORY', 'STATUS', 'QUANTITY'], how='outer')
    # data = get_categories_ID(data, data_categorias)

    # # Removendo duplicatas
    # data = data.drop_duplicates(subset='ITEM_ID', keep='first')
    # data = data.iloc[2:]
    # data = data.dropna(subset=['ITEM_ID'])

    # # Processando os dados
    # # processor = DataProcessor(data)
    # # data = processor.clean_data()

    # # Atualizando os SKUs dos produtos
    # new_data, news = update_product_skus(products)

    # # Formatando os dados
    # # st.write("Formatando os dados")
    # # new_data = format_data(new_data)

    # # Exibindo os dados processados no Streamlit
    # if data_categorias is not None:
    #     st.dataframe(new_data)
    #     st.dataframe(news)


    update_worksheet(data, 'ANUNCIOS', 1, url=url2)

