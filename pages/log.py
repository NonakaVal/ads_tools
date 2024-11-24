from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
import streamlit as st
import pandas as pd
import os

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

##############################################################################################
##############################################################################################


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
                "Preview", help="Streamlit app preview screenshots", width=170
            )
        }
    )

    # Calculando totais
    total_quantity = filtered['QUANTITY'].sum().astype(int)
    total_value = filtered['MSHOPS_PRICE'].sum()




def clear_submit():
    """
    Clear the Submit Button State
    """
    st.session_state["submit"] = False


# OpenAI API Key
openai_api_key = st.secrets.get("openai_api_key")
if not openai_api_key:
    st.error("Adicione sua chave de API da OpenAI nas configurações.")
    st.stop()

st.divider()

st.sidebar.divider()

# Histórico de mensagens inicial
if "messages" not in st.session_state or st.sidebar.button("Limpar histórico de conversas"):
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": (
                "Você é um assistente especializado em gestão de produtos e análise de dados. "
                "Os dados fornecidos incluem informações detalhadas sobre produtos, como preço, "
                "quantidade, categorias e imagens. Responda sempre de maneira clara e objetiva, "
                "em português (pt-BR). Certifique-se de que todas as suas respostas estejam no idioma português."
            ),
        },
        {"role": "assistant", "content": "Olá! Como posso ajudar com os dados de produtos hoje?"},
    ]

# Exibir histórico de mensagens no chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# Entrada do usuário
if prompt := st.chat_input(placeholder="Pergunte algo sobre os dados, como valores, categorias ou status dos produtos."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Configurar modelo LLM
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
        openai_api_key=openai_api_key,
        streaming=True,
        verbose=False
    )

    # Configurar o agente com o DataFrame (data deve ser previamente definido)
    pandas_df_agent = create_pandas_dataframe_agent(
        llm,
        data,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        handle_parsing_errors=True,
        allow_dangerous_code=True,  # Opt-in para permitir execução de código
    )

    # Executar a consulta do usuário e registrar a resposta
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        try:
            response = pandas_df_agent.run(prompt, callbacks=[st_cb])

            # Validar se a resposta está em português
            if not response.strip().startswith("Erro") and not response.strip().startswith("Desculpe"):
                response = f"Resposta em português:\n\n{response}"

            # Registrar resposta no histórico
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
        except Exception as e:
            error_message = f"Erro ao processar a consulta: {e}"
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            st.error(error_message)
