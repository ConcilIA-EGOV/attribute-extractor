"""
Call function to read file and call function to prompt
"""
import os
import time

import tqdm

from config import VERBOSE, CABECALHOS, PATH_LOG, PATH_RESULTS
from config import PATH_RAW_DOCUMENTS_FOLDERS, PATH_PROMPTS, PATH_BASE_OUTPUT

from src.api import send_prompt, get_api_key
from src.file_operations import list_raw_files_in_folder, read_txt_file, get_set_of_files_path, \
    get_list_of_prompts, get_results_path, get_log_path #, convert_csv_to_xlsx, get_formatted_results_path
# from src.time_converter import convert_time_to_numeric


def merge_prompt_and_document(document_text, prompt):
    """
    In this way, we are sure that we follow the same pattern all the time.
    """
    return prompt + os.linesep + "[ " + document_text + " ]"

# Formata a resposta para ser salva no arquivo de resultados
# como uma lista e obtém o número da sentença
def get_sentence(file_path:str) -> str:
    arquivo = list(file_path[:-4])
    arquivo.reverse()
    limite = arquivo.index('/')
    temp = arquivo[:limite]
    temp.reverse()
    sentenca = "".join(temp) + ','
    return sentenca


# Pegando a linha com os resultados
def find_results(response_for_db:list[str]) -> tuple[str, list]:
    result_index = None
    for i, row in enumerate(response_for_db):
        row_elements = row.split(',')
        if (any(el == "S" or el == "N" or el == '"S"' or el == '"N"' for el in row_elements)):
            result_index = i
            break
    
    if (result_index == None):
        result_index = 0
        response_for_db[result_index] = ""

    return response_for_db[result_index] + "\n"


def apply_prompt_to_files(experiment, list_prompts, output_path=""):    
    for p, prompt_path in enumerate(list_prompts):
        print("-" * 50)
        prompt_text = read_txt_file(prompt_path)
        print("Using prompt: ", prompt_path)
        target_files_paths = list_raw_files_in_folder(experiment)

        # Apply the prompt
        print("Applying to files:", len(target_files_paths))

        # Abrindo arquivo de resultados
        results_path = get_results_path(target_files_paths, prompt_path, PATH_RESULTS)
        resultados = open(results_path, "w")
        cabecalho = CABECALHOS[p]
        resultados.write(cabecalho)

        # Abrindo arquivo com log das responses
        log_path = get_log_path(target_files_paths, prompt_path, PATH_LOG)
        
        log = open(log_path + ".txt", "w")
        log.write("Responses\n\n")

        total_tokens = 0
        # teste = 0
        for file_path in tqdm.tqdm(target_files_paths):            
            try:
                file_results = {}

                if VERBOSE:
                    print("=" * 50)
                    print(f"Reading file: {file_path}")

                document_text = read_txt_file(file_path)
                full_prompt = merge_prompt_and_document(document_text, prompt_text)

                if VERBOSE:
                    print("Sending request to OpenAI")

                t1 = time.time()
                responses, input_tokens, output_tokens = send_prompt(full_prompt)
                t2 = time.time()

                # Extraindo resultado
                # Somando quantidade de tokens utilizados
                total_tokens += input_tokens + output_tokens
                for response in responses:
                    response = response.replace("```", "").strip()
                    response_for_db = response.split('\n')
                    sentenca = get_sentence(file_path)

                    # Salvando response no arquivo de log
                    log.write("Sentença " + sentenca[:-1] + ":\n")
                    log.write(response + "\n\n")

                    # Pegando a linha com os resultados
                    result = find_results(response_for_db)
                    csv_block = sentenca + result

                    # Salvando Resultado
                    resultados.write(csv_block)

                if VERBOSE:
                    print("Response:")
                    print("-" * 10)
                    print(response.replace("```", "").strip())
                    print("-" * 10)
                    print(f"Response time: {round(t2 - t1, 3)} seconds")
                    print(f"Input tokens: {input_tokens}")
                    print(f"Output tokens: {output_tokens}")
            
                # teste += 1
            except Exception as e:
                print("Erro em apply_prompt_to_files:", e)
        log.write("Tokens utilizados no experimento: " + str(total_tokens)) 
        resultados.close()
        log.close()

        if VERBOSE:
            print("End of execution.")

def run_all_experiments():
    list_set_of_experiments = get_set_of_files_path(base_path=PATH_RAW_DOCUMENTS_FOLDERS)
    
    path_prompt = PATH_PROMPTS
    
    list_prompts = get_list_of_prompts(prompt_base_path=path_prompt)
    
    # The experiments are the individual folders with raw txt files.
    for experiment in list_set_of_experiments:
        print("=" * 50)
        print("Running experiment:", experiment)

        # Apply each available prompt for each experiment
        apply_prompt_to_files(experiment, list_prompts, PATH_BASE_OUTPUT)


def main():
    run_all_experiments()


if __name__ == "__main__":
    main()
