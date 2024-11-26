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
url = st.secrets["product_url"]

##############################################################################################
##############################################################################################

if url:
    # Set up Google Sheets manager
    gs_manager.set_url(url)

    # products worksheets
    gs_manager.add_worksheet(url, "ANUNCIOS")
    gs_manager.add_worksheet(url, "CATEGORIAS")
    gs_manager.add_worksheet(url, "IMAGENS")
    gs_manager.add_worksheet(url, "CONDITIONS")

    # Read worksheets
    products = gs_manager.read_sheet(url, "ANUNCIOS")
    categorias = gs_manager.read_sheet(url, "CATEGORIAS")
    imgs = gs_manager.read_sheet(url, "IMAGENS")
    conditions = gs_manager.read_sheet(url, "CONDITIONS")


##############################################################################################
##############################################################################################

    data = products.copy()

    data = get_categories_ID(products, categorias)
    data = get_condition(data, conditions)
    data = get_imgs(data, imgs)
    
    data = classify_items(data)
    data = classify_editions(data)
    filtered = apply_filters(data, categorias)
    data = format_data(filtered)
    data = format_prices(data)

##############################################################################################
##############################################################################################

# Renomeando as colunas para exibição em português
    data.rename(
        columns={
            "IMG": "Imagem",
            "ITEM_ID": "ID do Item",
            "SKU": "Código SKU",
            "TITLE": "Título",
            "MSHOPS_PRICE": "Preço MercadoShops",
            "QUANTITY": "Quantidade",
            "STATUS": "Status",
            "URL": "Link",
            "ITEM_LINK": "LinkEdit",
            "CATEGORY": "Categoria",
            "CONDITION": "Condição",
            "DESCRIPTION": "Descrição",
            "MARKETPLACE_PRICE": "Preço MercadoLivre",
        },
        inplace=True,
    )


    
    st.sidebar.divider()
    # Opções de colunas disponíveis para exibição
    all_columns = data.columns.tolist()
    default_columns = ['Imagem', 'ID do Item', 'Código SKU', 'Título', 'Preço MercadoShops', 'Quantidade', 'Status', 'Link', 'LinkEdit']

    # Widget multiselect para escolher as colunas
    selected_columns = st.sidebar.multiselect(
        "Selecione as colunas para exibição:",
        options=all_columns,
        default=default_columns,
    )

    # Garantir que a ordem das colunas seja respeitada
    select_data = data[selected_columns]

    # Display dataframe com as colunas selecionadas
    
    # Título da seção


    # st.sidebar.header("Pesquisar Produtos")

    # # Estado inicial para armazenar os resultados da busca
    # if "filtered_data" not in st.session_state:
    #     st.session_state["filtered_data"] = data  # Inicialmente, a tabela completa é exibida

    # # Criação do formulário
    # with st.form("search_form"):
    #     search_term = st.text_input("Digite o termo para buscar (nome ou descrição):", "")
    #     submit_button = st.form_submit_button("Pesquisar")

    # # Lógica para filtrar os dados
    # if submit_button:
    #     if search_term.strip():
    #         # Filtro pelo termo no Título e na Descrição, insensível a maiúsculas/minúsculas
    #         filtered_data = data[
    #             data["Título"].str.contains(search_term, case=False, na=False)
    #             | data["Descrição"].str.contains(search_term, case=False, na=False)
    #         ]
    #         # Atualiza o estado com os resultados
    #         st.session_state["filtered_data"] = filtered_data

    #         if filtered_data.empty:
    #             st.warning(f"Nenhum resultado encontrado para '{search_term}'.")
    #     else:
    #         st.warning("Por favor, digite um termo de busca.")

    # # Botão para limpar a busca
    # if st.button("Limpar Busca"):
    #     st.session_state["filtered_data"] = data  # Restaura a tabela completa

    # # Exibição da tabela com os resultados filtrados ou completos
    # st.markdown(f"**Resultados encontrados: {len(st.session_state['filtered_data'])}**")
    # st.dataframe(
    #     st.session_state["filtered_data"][selected_columns],  # Exibe apenas as colunas selecionadas
    #     column_config={
    #         "Link": st.column_config.LinkColumn(display_text="Link do Produto"),
    #         "LinkEdit": st.column_config.LinkColumn(display_text="Editar Anúncio"),
    #         "Imagem": st.column_config.ImageColumn(
    #             "Preview", help="Preview da imagem", width=130
    #         ),
    #     },
    # )

    st.dataframe(
        select_data,
        column_config={
            "Link": st.column_config.LinkColumn(display_text="Link do Produto"),
            "LinkEdit": st.column_config.LinkColumn(display_text="Editar Anúncio"),
            "Imagem": st.column_config.ImageColumn(
                "Preview", help="Preview da imagem", width=130
            )
        }
    )

##############################################################################################
##############################################################################################

    # # Calculando totais
    # total_quantity = filtered['QUANTITY'].sum().astype(int)
    # total_value = filtered['MSHOPS_PRICE'].sum()

    # st.sidebar.divider()
    # col1, col2 = st.columns(2)
    # with col1:
    #     st.sidebar.metric("Quantidade Total de Itens", total_quantity,)
    # with col2:
    #     st.sidebar.metric("Valor Total dos Itens (R$)", f"{total_value:,.2f}")
    

##############################################################################################
##############################################################################################

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

st.markdown("Assistente por chat: ")


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
        products,
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
st.error("Ainda em desenvolvimento, não é tão esperto", icon="🫏")

st.sidebar.divider()    


st.sidebar.page_link("pages/update.py", label="Atualizar com Tabela Excel Mercado Livre")