import csv
import pandas as pd
import os

from src.file_operations import ensure_directory_exists, convert_csv_to_xlsx
from config import INTERVALO_EXTRAVIO, INTERVALO_ATRASO

""" 
TODO:
Tratar os casos em que a resposta veio em formato com erro
""" 

def format_interval(interval: str) -> float:
    """
    Formata o intervalo de tempo para um valor numérico
    """
    list_interval = interval.split(':')
    if (len(list_interval) == 2):
        return int(list_interval[0]) + round(int(list_interval[1])/60, 2)
    else:
        return ':'.join(list_interval)

def convert_time_to_numeric(csv_origin_path, res_dir_path):    
    # Verificando se o arquivo origem existe
    if not os.path.exists(csv_origin_path):
        print("O arquivo de resultados (sem formatação) não foi encontrado")
        return

    # Verificando se o diretório destino
    if not os.path.exists(res_dir_path):
        print("O diretório de resultados (formatados) não foi encontrado")
        return

    # Path dos arquivos formatados
    result_csv_path = os.path.join(res_dir_path, "resultados_formatados.csv")
    # result_xlsx_file = os.path.join(res_dir_path, "resultados_formatados.xlsx")

    origin_file = open(csv_origin_path, "r")
    formatted_file = open(result_csv_path, "w")

    csv_reader = csv.DictReader(origin_file)
    csv_writer = csv.writer(formatted_file)

    # Escreve o cabeçalho
    csv_writer.writerow(csv_reader.fieldnames)
    for row in csv_reader:
        try:
            # Intervalo de extravio
            extravio = format_interval(row[INTERVALO_EXTRAVIO])
            # Intervalo de atraso
            atraso = format_interval(row[INTERVALO_ATRASO])
            '''
            list_extravio = row[INTERVALO_EXTRAVIO].split(':')
            if (len(list_extravio) == 2):
                extravio = int(list_extravio[0]) + round(int(list_extravio[1])/60, 2)
            else:
                extravio = ':'.join(list_extravio)
            '''
            '''
            list_atraso = row[INTERVALO_ATRASO].split(':')
            if (len(list_atraso) == 2):
                atraso = int(list_atraso[0]) + round(int(list_atraso[1])/60, 2)
            else:
                atraso = ':'.join(list_atraso)
            '''
        except Exception as e:
            print("Erro", e, "ao converter o tempo para numérico")
            extravio = row[INTERVALO_ATRASO]
            atraso = row[INTERVALO_EXTRAVIO]

        # Salva os resultados com os novos valores para
        # os intervalos de extravio e de atraso
        row[INTERVALO_EXTRAVIO] = extravio
        row[INTERVALO_ATRASO] = atraso
        csv_writer.writerow(row.values())
        

    origin_file.close()
    formatted_file.close()

    # Convertendo para xlsx
    convert_csv_to_xlsx(result_csv_path, "resultados_formatados.xlsx")

def main():
    convert_time_to_numeric()

if __name__ == "__main__":
    main()
