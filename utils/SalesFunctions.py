from datetime import datetime
import pandas as pd 

from utils.UploadFile import load_data
meses = {
    'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
    'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
    'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
}

# Função para converter a data
def converter_data(data_hora_str):
    # Substituir o mês em português pelo número correspondente
    for mes, numero in meses.items():
        data_hora_str = data_hora_str.replace(mes, numero)
    # Converter a string para datetime
    try:
        data_hora = datetime.strptime(data_hora_str, "%d de %m de %Y %H:%M hs.")
        return data_hora.strftime("%d/%m/%Y")
    except ValueError:
        return None  # Caso a data seja inválida ou nula

def sales_data_cleaning(data, x):
    # Processar o DataFrame 'vendas'
    vendas = data.iloc[:, :11]  # Seleciona as primeiras 11 colunas
  
    vendas['Unidades'] = vendas['Unidades'].fillna(2).astype(int)
    vendas = vendas.drop(columns=['Receita por envio (BRL)', 'Status', 'Descrição do status', 'Pacote de diversos produtos'], errors='ignore')
    vendas['Receita por produtos (BRL)'] = vendas['Receita por produtos (BRL)'].fillna(data['Preço unitário de venda do anúncio (BRL)'])
    vendas['Cancelamentos e reembolsos (BRL)'] = vendas['Cancelamentos e reembolsos (BRL)'].fillna(0)
    vendas['Tarifa de venda e impostos'] = vendas['Tarifa de venda e impostos'].fillna(0)
    vendas['Tarifas de envio'] = vendas['Tarifas de envio'].fillna(0)

    # Processar o DataFrame 'compradores'
    compradores = data.iloc[:, [0]].join(data.iloc[:, 26:33])  # Seleciona a primeira coluna e as colunas 26 a 32

    # Converter a data na coluna 'Data da venda'
    vendas['Data da venda'] = data['Data da venda'].apply(converter_data).fillna(0)

    # Mesclar DataFrames 'vendas' e 'compradores'
    df_merged = pd.merge(vendas, compradores, on='N.º de venda', how='inner')
    
    df_merged['CHANNEL'] = x
    
    # Adicionar as colunas nas posições 15 (índice 14) e 16 (índice 15)
    if data.shape[1] > 15:  # Verifica se a coluna 15 existe
        df_merged.insert(15, 'ITEM_ID', data.iloc[:, 15])  # Adiciona a coluna do DataFrame original na posição 15
    if data.shape[1] > 16:  # Verifica se a coluna 16 existe
        df_merged.insert(16, 'TITLE', data.iloc[:, 16])  # Adiciona a coluna do DataFrame original na posição 16

    # Retornar o DataFrame final processado
    return df_merged

def format_sales(data,channel):
    data = load_data(data, "Vendas BR", header=5)  # Passa o arquivo carregado como argumento
    data = sales_data_cleaning(data, channel)
    data = data.rename(columns={"Endereço.1": "Endereço", "Status.1": "UF"})
    return data