import streamlit as st

from utils.GoogleSheetManager import GoogleSheetManager, update_worksheet
from utils.UpdateFunctions import compare_dataframes
from streamlit_gsheets import GSheetsConnection
from utils.AplyClassifications import get_categories_ID
from utils.AplyPandas import update_product_skus
from datetime import datetime
import pandas as pd

conn = st.connection("gsheets", type=GSheetsConnection)
def update_worksheet(df, worksheet_title, key, url, button_text="Enviar lista"):
    if st.button(button_text, key=key):
        # url = st.secrets["url"]
        conn.update(spreadsheet=url, worksheet=worksheet_title, data=df)
        st.success("Subir itens para tabela 🤓")

def load_data(path_excel, sheet_name_value=2):
    data_excel = pd.read_excel(path_excel, 
                                sheet_name= sheet_name_value, 
                                skiprows=range(1, 6))
    data_excel['STATUS'] = data_excel['STATUS'].str.strip()
    data_excel = data_excel.drop_duplicates(subset='ITEM_ID', keep='first')
    data_excel =data_excel.drop(columns=['VARIATIONS' ,'VARIATION_ID'])
    

    return data_excel

def fill_sku_(df_with_sku, df_without_sku):
    """Preenche os SKUs em df_without_sku com base em df_with_sku (usando ITEM_ID como chave)."""
    merged_data = df_without_sku.merge(df_with_sku[['ITEM_ID', 'SKU']], on='ITEM_ID', how='left', suffixes=('', '_from_df1'))
    merged_data['SKU'] = merged_data['SKU_from_df1']
    merged_data.drop(columns=['SKU_from_df1'], inplace=True)
    return merged_data

def update_product_skus(data):
    
    current_year_month = datetime.now().strftime("%y%m")  # Ano e mês atual no formato "yyMM"
    
    # Preparando para rastrear informações adicionais sobre novos SKUs
    new_skus_list = []
    new_skus_details = []  # Lista para armazenar detalhes para novos SKUs incluindo ITEM_ID e TITLE

    # Certifique-se de que CATEGORY_ID tenha 3 dígitos
    data['CATEGORY_ID'] = data['CATEGORY_ID'].str.zfill(3)

    # Dicionário para rastrear o contador por categoria e mês
    category_counters = {}

    for category_id in data['CATEGORY_ID'].unique():
        category_mask = data['CATEGORY_ID'] == category_id

        # Filtra os SKUs existentes dessa categoria e mês
        existing_skus = data.loc[category_mask & data['SKU'].notna(), 'SKU']

        # Verifica o ano/mês atual para a categoria
        year_month = current_year_month

        # Extraímos os contadores do SKU, considerando a categoria e mês
        counters = existing_skus.str.extract(f"^{category_id}-{year_month}-(\\d{{4}})$")[0]
        valid_counters = pd.to_numeric(counters, errors='coerce').dropna().astype(int)
        
        # Define o próximo contador, baseado no maior contador existente, ou inicia em 1
        if not valid_counters.empty:
            next_counter = valid_counters.max() + 1
        else:
            next_counter = 1

        # Filtra os índices dos produtos sem SKU
        null_skus_indices = data.index[category_mask & data['SKU'].isna()]
        for idx in null_skus_indices:
            # Gera um SKU único com base na categoria, ano/mês e o contador
            new_sku = f"{category_id}-{year_month}-{next_counter:04d}"
            data.at[idx, 'SKU'] = new_sku
            new_skus_list.append(new_sku)
            new_skus_details.append({
                'TITLE': data.at[idx, 'TITLE'],
                'SKU': new_sku,
                'ITEM_ID': data.at[idx, 'ITEM_ID'],
            })

            # Incrementa o contador após gerar o SKU para o próximo
            next_counter += 1

    # Converte a lista de dicionários em DataFrame
    new_skus_data = pd.DataFrame(new_skus_details)  # Agora inclui ITEM_ID e TITLE

    return data, new_skus_data


def get_links(data):
    data['ITEM_LINK'] = data['ITEM_ID'].apply(
        lambda x: f"https://www.mercadolivre.com.br/anuncios/lista?filters=OMNI_ACTIVE|OMNI_INACTIVE|CHANNEL_NO_PROXIMITY_AND_NO_MP_MERCHANTS&page=1&search={x[3:]}" if pd.notnull(x) else "")

    data['URL'] = data.apply(
        lambda row: f"https://www.collectorsguardian.com.br/{row['ITEM_ID'][:3]}-{row['ITEM_ID'][3:]}-{row['TITLE'].replace(' ', '-').lower()}-_JM#item_id={row['ITEM_ID']}", 
        axis=1)

    return data

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

    st.dataframe(data_ml)

    # data_ml = data_ml.iloc[5:]
    
    # Configurando o gerenciador de planilhas e lendo dados de produtos
    gs_manager.set_url(url)
    gs_manager.add_worksheet(url, "CATEGORIAS")
    gs_manager.add_worksheet(url, "ANUNCIOS")
    products = gs_manager.read_sheet(url, "ANUNCIOS")
    categorias = gs_manager.read_sheet(url, "CATEGORIAS")

    # # Normalizando e mesclando dados
    # data_ml = data_normalization(data_ml)
    # products = data_normalization(products)
    data = fill_sku_(products, data_ml)
    data = get_categories_ID(products, categorias)
    data, news_skus = update_product_skus(data)

    # st.divider()
    # st.write("###### Resumo")
    # # Comparando DataFrames e obtendo totais
    items_added, items_removed, price_changes, quantity_changes, status_changes, total_price_active, total_quantity_active = compare_dataframes(data_ml, products)
    

    # # Exibindo os resultados no Streamlit
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
        st.write("mewslu")
        # st.dataframe(news_skus)

    # col1, col2 = st.columns(2)
    

    # with col1:

    #     st.metric(label="Total MSHOPS_PRICE (Ativos)", value=f"R$ {total_price_active:,.2f}")
    #     st.metric(label="Total Quantidade (Ativos)", value=f"{total_quantity_active:,}")

    # with col2:
    #     st.write("Itens Adicionados")
    #     st.metric(label="Total de Itens Adicionados", value=f"{len(items_added)}")

    

    # st.divider()    
    # edited_df = st.data_editor(data)
    # st.divider()    
    # Atualizando os dados no Google Sheets
    st.divider()    
    update_worksheet(data, 'ANUNCIOS', 1, url=url)
    st.divider()    

