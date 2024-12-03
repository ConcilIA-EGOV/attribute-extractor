"""
Call function to read file and call function to prompt
"""
import time

import tqdm

from config import CABECALHOS, SENTENCES_REPETITIONS
from config import PATH_RAW_DOCUMENTS_FOLDERS, PATH_PROMPTS, PATH_BASE_OUTPUT

from src.api import send_prompt
from src.file_operations import list_raw_files_in_folder, read_prompt, read_txt_file, merge_prompt_and_document
from src.file_operations import get_list_of_prompts, get_results_path, get_log_path, get_set_of_files_path


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


# Formata a resposta para ser salva no arquivo de resultados
# como uma lista e obtém o número da sentença
def get_sentence(file_path:str) -> str:
    arquivo = list(file_path[:-4])
    arquivo.reverse()
    limite = arquivo.index('/')
    temp = arquivo[:limite]
    temp.reverse()
    sentenca = "".join(temp)
    return sentenca


def apply_prompt_to_files(experiment, list_prompts, output_path):    
    for p, prompt_path in enumerate(list_prompts):
        print("-" * 50)
        prompt_list = read_prompt(prompt_path)
        print("Using prompt: ", prompt_path)
        target_files_paths = list_raw_files_in_folder(experiment)

        # Apply the prompt
        print("Applying to %d files:" % len(target_files_paths))

        # Abrindo arquivo de resultados
        results_path = get_results_path(target_files_paths, prompt_path, output_path)
        resultados = open(results_path, "w")
        cabecalho = CABECALHOS[p]
        if type(cabecalho) == list:
            resultados.write(cabecalho[0] + '\n')
        else:
            resultados.write(cabecalho + '\n')

        # Abrindo arquivo com log das responses
        log_path = get_log_path(target_files_paths, prompt_path, output_path)
        
        log = open(log_path + ".txt", "w")
        log.write("Responses\n\n")

        total_tokens = 0
        # teste = 0
        for file_path in tqdm.tqdm(target_files_paths):
            try:
                sentenca = get_sentence(file_path)
                document_text = read_txt_file(file_path)
                csv_block = sentenca
                for prompt in prompt_list:
                    full_prompt = merge_prompt_and_document(document_text, prompt)

                    log_response, result, input_tokens, output_tokens = send_prompt(full_prompt)

                    csv_block += ',' + result
                    # Somando quantidade de tokens utilizados
                    total_tokens += input_tokens + output_tokens
                    # Salvando response no arquivo de log
                    log.write("Sentença " + sentenca + ":\n")
                    log.write(log_response + "\n\n")
                if type(cabecalho) == list:
                    csv_block = reorder_results(current_header=cabecalho[1].split(","),
                                                intended_header=cabecalho[0].split(","),
                                                values=csv_block.split(","))
                    csv_block = ",".join(csv_block) + "\n"
                        

                # Salvando Resultado
                resultados.write(csv_block)
            
                # teste += 1
            except Exception as e:
                print("Erro em apply_prompt_to_files:", e)
        log.write("Tokens utilizados no experimento: " + str(total_tokens)) 
        resultados.close()
        log.close()

def run_all_experiments():
    list_set_of_experiments = get_set_of_files_path(base_path=PATH_RAW_DOCUMENTS_FOLDERS)
    
    path_prompt = PATH_PROMPTS
    
    list_prompts = get_list_of_prompts(prompt_base_path=path_prompt)
    
    # The experiments are the individual folders with raw txt files.
    for i in range(SENTENCES_REPETITIONS):
        for experiment in list_set_of_experiments:
            print("=" * 50)
            print("Running experiment:", experiment)

            # Apply each available prompt for each experiment
            apply_prompt_to_files(experiment, list_prompts, PATH_BASE_OUTPUT + f'-{i+1}')


def main():
    run_all_experiments()


if __name__ == "__main__":
    main()
