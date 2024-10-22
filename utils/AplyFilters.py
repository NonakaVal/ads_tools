import streamlit as st
from utils.Get_Link import get_link, get_link_edit



# Initialize connection to Google Sheets
# conn = st.connection("gsheets", type=GSheetsConnection)

##############################################################################################
##############################################################################################

# get the url of google sheets
url = st.secrets["product_url"]


# Filter Functions
def filter_by_category(df, categories):
    """Filter the DataFrame by the selected categories."""
    return df[df['CATEGORY'].isin(categories)] if categories else df

def filter_by_subcategory(df, subcategories):
    """Filter the DataFrame by the selected subcategories."""
    return df[df['SUBCATEGORY'].isin(subcategories)] if subcategories else df

def filter_by_status(df, status):
    """Filter the DataFrame by the selected status (Active/Inactive)."""
    return df[df['STATUS'] == status] if status != "Todos" else df

def filter_by_condition(df, conditions):
    """Filter the DataFrame by the selected conditions."""
    
    return df[df['CONDITION'].isin(conditions)] if conditions else df


def filter_by_edition(df, editions):
    """Filter the DataFrame by the selected editions."""
    return df[df['EDITION'].isin(editions)] if editions else df

def filter_by_quantity(df, min_qty, max_qty):
    """Filter the DataFrame by the selected quantity range."""
    return df[(df['QUANTITY'] >= min_qty) & (df['QUANTITY'] <= max_qty)]

# Item selection and display
def select_items(df):
    """Allow the user to select items from the DataFrame, displaying SKU, ITEM_ID, and TITLE."""
    df['item_display'] = df['ITEM_ID'].astype(str) + ' - ' + df['TITLE']
    item_options = df[['SKU', 'item_display', 'IMG']].set_index('SKU')['item_display'].to_dict()
    
    st.write("")

    st.write("Selecione os itens a serem editados:")
    selected_display_names = st.multiselect(
        "Nome, SKU ou código Mercado Livre", 
        options=list(item_options.values()), 
        key=1, 
        placeholder="Pesquisar por Nome, SKU ou código Mercado Livre", 
        label_visibility="collapsed"
    )
    
    # Map selected display names to SKUs
    selected_skus = [key for key, value in item_options.items() if value in selected_display_names]
    selected_items_df = df[df['SKU'].isin(selected_skus)]

    # Apply the get_link function to the selected items
    selected_items_df = get_link(selected_items_df)

    # Display selected items with URLs and image previews
    if not selected_items_df.empty:
        st.data_editor(
            selected_items_df, 
            column_config={
                "URL": st.column_config.LinkColumn(),
                "IMG": st.column_config.ImageColumn(
                    "Preview", 
                    help="Streamlit app preview screenshots", 
                    width=90
                )
            }
        )
    
    return selected_items_df
# Applying filters
def apply_filters(df, categories_df):
    """Apply multiple filters to the DataFrame based on user selections."""
    df_filtered = df.copy()  # Create a copy to avoid modifying the original DataFrame

    # Status filter
    all_status = ['Todos', 'Ativo', 'Inativo']
    selected_status = st.sidebar.selectbox("Status", all_status, index=1)
    df_filtered = filter_by_status(df_filtered, selected_status)

    # Category filter
    all_categories = categories_df['CATEGORY'].unique().tolist()
    selected_categories = st.sidebar.multiselect(
        "Categoria e Sub-categoria", 
        ['Todas'] + all_categories, 
        placeholder="Categorias Mercado Livre", 
        label_visibility="collapsed"
    )
    if selected_categories and "Todas" not in selected_categories:
        df_filtered = filter_by_category(df_filtered, selected_categories)

    # Subcategory filter
    all_subcategories = sorted(df['SUBCATEGORY'].unique().tolist(), reverse=True)
    selected_subcategories = st.sidebar.multiselect(
        "Escolha uma Subcategoria", 
        ['Todas'] + all_subcategories, 
        placeholder="Subcategorias", 
        label_visibility="collapsed"
    )
    if selected_subcategories and "Todas" not in selected_subcategories:
        df_filtered = filter_by_subcategory(df_filtered, selected_subcategories)

    # Condition filter
    all_conditions = df['CONDITION'].unique().tolist()
    selected_conditions = st.sidebar.multiselect(
        "Condição", 
        ['Todas'] + all_conditions, 
        placeholder="Condição", 
        label_visibility="collapsed"
    )
    if selected_conditions and "Todas" not in selected_conditions:
        df_filtered = filter_by_condition(df_filtered, selected_conditions)
    st.sidebar.markdown("[Acessar Condições](https://share.note.sx/c7iihkct#OdTU3s9gCjJe+GF03Ff3SZct+sI/iTJsd4+EyVkCz4I)")

    # Edition filter
    all_editions = df['EDITION'].unique().tolist()
    selected_editions = st.sidebar.multiselect(
        "Edição", 
        ['Todas'] + all_editions, 
        placeholder="Edições", 
        label_visibility="collapsed"
    )
    if selected_editions and "Todas" not in selected_editions:
        df_filtered = filter_by_edition(df_filtered, selected_editions)

    # Quantity filter
    min_quantity = st.sidebar.number_input(
        "Quantidade mínima", min_value=0, value=1, step=1
    )
    # max_quantity = st.sidebar.number_input(
    #     "Quantidade máxima", min_value=1, value=10, step=1, label_visibility="collapsed"
    # )

    max_quantity = min_quantity + 10
    df_filtered = filter_by_quantity(df_filtered, min_quantity, max_quantity)
    df_filtered = get_link_edit(df_filtered)
    

    return df_filtered



