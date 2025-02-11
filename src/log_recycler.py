import os
from file_operations import list_raw_files_in_folder, get_set_of_files_path, read_txt_file, ensure_directory_exists
import sys
sys.path.append('../config.py')
# from config import CABECALHOS
CABECALHOS = [
    [
        "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,cancelamento/alteracao_destino,atraso,intervalo_atraso,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel",
        "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,violacao_furto_avaria,cancelamento/alteracao_destino,atraso,noshow,overbooking,assistencia_cia_aerea,hipervulneravel,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,intervalo_extravio_temporario,intervalo_atraso"
     ],
    ""
]

def reorder_results(current_header:list[str],
                    intended_header:list[str],
                    values:list[str]) -> list[str]:
    """
    Reorder the values to match the intended header.
    """
    if not (len(current_header) == len(values) == len(intended_header)):
        limit = len(intended_header)
        if len(values) < limit:
            limit = len(values)
        return values[:limit]
    result = []
    for header in intended_header:
        index = current_header.index(header)
        result.append(values[index])
    return result


def recycle(file: str, output_path: str, cabecalho):
    print(f'Processing --> {file} -> {output_path}')
    resultados = open(output_path, "w")
    if type(cabecalho) == list:
        resultados.write(cabecalho[0] + '\n')
    else:
        resultados.write(cabecalho + '\n')
    sentence_prev = ''
    csv_block = ''
    first = True
    content = read_txt_file(file)
    cases = content.split('\n\nSentença ')
    cases.pop(0) # removendo linha 'Responses'
    last = cases[-1] # removendo linha 'Tokens utilizados no experimento: x'
    print(f'Last: {last}')
    cases[-1] = "\n".join(last.split()[:-5])
    print(f'Last: {cases[-1]}')
    cases += ['END']
    for case in cases:
        lines = case.split('\n')
        sentence = lines[0].replace(':', '')
        lines = lines[2:]
        if first:
            first = False
            csv_block = sentence
            sentence_prev = sentence
            print('FIRST:', sentence, '->', lines, '-->', csv_block)
        if sentence != sentence_prev:
            print(f">> Sentence changed from {sentence_prev} to {sentence}")
            if type(cabecalho) == list:
                csv_block = reorder_results(current_header=cabecalho[1].split(","),
                                            intended_header=cabecalho[0].split(","),
                                            values=csv_block.split(","))
                csv_block = ",".join(csv_block)
            print(f'FINAL: {sentence_prev} --> {csv_block}\n')
            # Salvando Resultado
            resultados.write(csv_block + "\n")
            csv_block = sentence
            sentence_prev = sentence
        csv_block += ',' + ",".join(lines)
        print(sentence, '->', lines, '-->', csv_block)
    


def recycler(base_path: str, cabecalho: list, ext='csv'):
    output_path_base = 'logs_reciclados'
    ensure_directory_exists(output_path_base)
    output_path_base = f'logs_reciclados/{base_path}'
    ensure_directory_exists(output_path_base)

    folders = get_set_of_files_path(base_path)
    # print(f'Folders --> {folders}')
    for folder in folders:
        file = list_raw_files_in_folder(folder)[0]
        # print(f'\nProcessing folder --> {folder}')
        # print(f'\nFile --> {file}')
        output_path = os.path.join(output_path_base, os.path.basename(folder)) + f'.{ext}'
        # print(f'\nProcessing --> {file} -> {output_path}')
        recycle(file, output_path, cabecalho)


if __name__ == '__main__':
    base_path = 'resultados_requisicao-1'
    cabecalho = CABECALHOS[0]
    recycler(base_path, cabecalho, 'csv')
