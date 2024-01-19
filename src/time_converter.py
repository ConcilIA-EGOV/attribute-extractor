import csv
import pandas as pd
import os

from src.file_operations import ensure_directory_exists


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
    result_xlsx_file = os.path.join(res_dir_path, "resultados_formatados.xlsx")

    origin_file = open(csv_origin_path, "r")
    formatted_file = open(result_csv_path, "w")

    csv_reader = csv.DictReader(origin_file)
    csv_writer = csv.writer(formatted_file)

    # Escreve o cabeçalho
    csv_writer.writerow(csv_reader.fieldnames)
    for row in csv_reader:
        # Intervalo de extravio
        list_extravio = row['intervalo de extravio'].split(':')
        if (len(list_extravio) == 2):
            extravio = int(list_extravio[0]) + round(int(list_extravio[1])/60, 2)
        else:
            extravio = ':'.join(list_extravio)

        # Intervalo de atraso
        list_atraso = row['intervalo de atraso'].split(':')
        if (len(list_atraso) == 2):
            atraso = int(list_atraso[0]) + round(int(list_atraso[1])/60, 2)
        else:
            atraso = ':'.join(list_atraso)

        row['intervalo de extravio'] = extravio
        row['intervalo de atraso'] = atraso

        # Salva os resultados com os novos valores para
        # os intervalos de extravio e de atraso
        csv_writer.writerow(row.values())

    origin_file.close()
    formatted_file.close()

    # Convertendo para xlsx
    data_frame = pd.read_csv(result_csv_path)
    data_frame.to_excel(result_xlsx_file, index=False)

def main():
    convert_time_to_numeric()

if __name__ == "__main__":
    main()