from datetime import datetime
import pandas as pd

meses = {
    'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
    'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
    'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
}

# Função para converter a data
def converter_data(data_hora_str):
    if pd.isnull(data_hora_str):
        return None  # Handle null values

    # Replace the Portuguese month with the corresponding number
    for mes, numero in meses.items():
        data_hora_str = data_hora_str.replace(mes, numero)

    # Try to convert the string to datetime format (ISO or custom)
    try:
        # First, try the ISO format (e.g., '2024-10-09 00:00:00')
        data_hora = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        # If that doesn't work, try the format with the Portuguese date structure
        try:
            data_hora = datetime.strptime(data_hora_str, "%d de %m de %Y %H:%M hs.")
        except ValueError:
            return None  # Return None if the date is invalid or cannot be parsed

    # Return the date in the desired format
    return data_hora.strftime("%d/%m/%Y")