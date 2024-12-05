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

##############################################################################################
# Inicializar a conexão com o Google Sheets
##############################################################################################

# Em algum lugar no seu código
df_final = load_and_process_data()

# Se quiser exibir no Streamlit
st.dataframe(
df_final,
column_config={
    "URL": st.column_config.LinkColumn(display_text="Link do Produto"),
    "ITEM_LINK": st.column_config.LinkColumn(display_text="Editar Anúncio"),
    "IMG": st.column_config.ImageColumn(
        "Preview", help="Preview da imagem", width=130
    )
}
)

st.divider()
gs_manager = GoogleSheetManager()
url = st.secrets["product_url"]

if url:
    # Configura o gerenciador de Google Sheets
    gs_manager.set_url(url)

    # Adicionar a worksheet
    gs_manager.add_worksheet(url, "ANUNCIOS")

    # Ler os dados da worksheet
    products = gs_manager.read_sheet(url, "ANUNCIOS")

##############################################################################################
# Função para selecionar itens do Google Sheets
##############################################################################################

def select_items(data):
    # Criar uma coluna para exibição combinada de SKU e TITLE
    data['item_display'] = data['ITEM_ID'].astype(str) + ' - ' + data['SKU'].astype(str) + ' - ' + data['TITLE']

    # Criar uma caixa de seleção múltipla para escolher itens
    item_options = data[['SKU', 'item_display']].set_index('SKU')['item_display'].to_dict()
    selected_display_names = st.multiselect("Selecione os itens (SKU - Nome)", options=list(item_options.values()))

    # Mapear nomes de exibição selecionados de volta para SKU
    selected_skus = [key for key, value in item_options.items() if value in selected_display_names]

    # Filtrar o DataFrame para obter as linhas correspondentes
    selected_items_df = data[data['SKU'].isin(selected_skus)]

    # Exibir o DataFrame dos itens selecionados
    if not selected_items_df.empty:
        st.write("Itens selecionados:")
        st.dataframe(selected_items_df[['ITEM_ID', 'SKU', 'TITLE']])

    return selected_items_df

##############################################################################################
# Classe personalizada para gerar código de barras sem texto
##############################################################################################

class CustomImageWriter(ImageWriter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = False  # Remove o texto do código de barras

# Função para gerar código de barras
def generate_barcode(code_text):
    writer = CustomImageWriter()
    code = Code128(code_text, writer=writer)
    buffer = BytesIO()
    code.write(buffer)
    buffer.seek(0)
    return buffer

# Função para cortar a imagem do código de barras
def crop_barcode_image(barcode_img, crop_percentage_top=0.1, crop_percentage_bottom=0.4):
    img = Image.open(barcode_img)
    width, height = img.size
    top = int(height * crop_percentage_top)
    bottom = int(height * (1 - crop_percentage_bottom))
    return img.crop((0, top, width, bottom))

# Função para criar uma etiqueta individual com código de barras
def create_single_label_with_barcode(name, ad_code, sku, config):
    label_width, label_height = 738, 250  # Ajustado para 33 etiquetas por página
    label = Image.new('RGB', (label_width, label_height), 'white')
    draw = ImageDraw.Draw(label)

    fonts = {}
    try:
        fonts['name'] = ImageFont.truetype("arial.ttf", config['name_font_size'])
        fonts['small'] = ImageFont.truetype("arial.ttf", config['small_font_size'])
    except IOError:
        fonts['name'] = ImageFont.load_default()
        fonts['small'] = ImageFont.load_default()

    # Adicionar o nome
    draw.text((config['name_x'], config['name_y']), name, font=fonts['name'], fill='black')

    # Adicionar o código do anúncio
    draw.text((config['ad_code_x'], config['ad_code_y']), f"ID: {ad_code}", font=fonts['small'], fill='black')
    
    # Adicionar o código de barras
    barcode_img = generate_barcode(sku)
    cropped_barcode_img = crop_barcode_image(barcode_img).resize((config['barcode_width'], config['barcode_height']))
    label.paste(cropped_barcode_img, (config['barcode_x'], label_height - config['barcode_height'] - config['barcode_bottom_padding']))

    return label

# Função para criar etiquetas a partir de um DataFrame com códigos de barras
def create_labels_from_dataframe_with_barcode(df, config):
    page_width, page_height = 2480, 3508  # Tamanho A4 em DPI 300
    label_width, label_height = 738, 250  # Tamanho ajustado das etiquetas
    labels_per_row = 3  # 3 etiquetas por linha
    labels_per_column = 11  # 11 etiquetas por coluna
    labels_per_page = labels_per_row * labels_per_column  # Total de etiquetas por página

    num_pages = -(-len(df) // labels_per_page)  # Arredonda para cima
    pdf_images = []

    x_offset = 60  # Deslocamento horizontal

    for page_num in range(num_pages):
        sheet = Image.new('RGB', (page_width, page_height), 'white')
        current_x = config['margin_left'] + x_offset
        current_y = config['margin_top']
        start_idx = page_num * labels_per_page
        end_idx = min(start_idx + labels_per_page, len(df))

        for idx in range(start_idx, end_idx):
            row = df.iloc[idx]

            label = create_single_label_with_barcode(
                row['TITLE'], row['ITEM_ID'], row['SKU'], config
            )
            sheet.paste(label, (current_x, current_y))
            current_x += label_width + config['spacing_horizontal']

            if (idx + 1) % labels_per_row == 0:
                current_x = config['margin_left'] + x_offset
                current_y += label_height + config['spacing_vertical']

        pdf_images.append(sheet.convert('RGB'))

    output_dir = 'etiquetas-33'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_path = os.path.join(output_dir, 'etiquetas_barcode_33_a4.pdf')
    pdf_images[0].save(pdf_path, save_all=True, append_images=pdf_images[1:], resolution=300)
    return pdf_path

##############################################################################################
# Função principal do Streamlit
##############################################################################################

def main():

    st.write("Selecione os itens para gerar etiquetas.")

    # Selecionar itens
    df = select_items(products)

    # Configurações para etiquetas
    config = {
        'margin_top': 70,
        'margin_bottom': 50,
        'margin_left': 70,
        'margin_right': 50,
        'spacing_horizontal': 40,
        'spacing_vertical': 55,
        'name_font_size': 25,
        'small_font_size': 25,
        'name_x': 55,
        'name_y': 50,
        'ad_code_x': 55,
        'ad_code_y': 100,
        'barcode_x': 10,
        'barcode_bottom_padding': 10,
        'barcode_width': 650,
        'barcode_height': 100
    }

    if st.button("Gerar PDF e Baixar"):
        if df.empty:
            st.warning("Por favor, selecione pelo menos um item!")
        else:
            pdf_path = create_labels_from_dataframe_with_barcode(df, config)
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Baixar PDF",
                    data=pdf_file,
                    file_name="etiquetas_barcode_33_a4.pdf",
                    mime="application/pdf"
                )
main()

