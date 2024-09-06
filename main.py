"""
Call function to read file and call function to prompt
"""
import os
import time

import tqdm

from config import SENTENCE_REPETITIONS, REPEAT_N, ALTERNATIVE_SAVE
from config import OUTPUT_TYPES, VERBOSE, GROUPS_VARIABLES, CABECALHOS
from src.api import send_prompt, get_api_key
from src.file_operations import list_raw_files_in_folder, read_txt_file, store_output_results, get_set_of_files_path, \
    get_list_of_prompts, get_results_path, get_log_path, convert_csv_to_xlsx, get_formatted_results_path
from src.time_converter import convert_time_to_numeric

PATH_RAW_DOCUMENTS_FOLDERS = "data/sentencas"
PATH_PROMPTS = "data/prompts"
PATH_PROMPTS_GRUPOS = "data/prompts/grupos"
PATH_BASE_OUTPUT = "data/resultados_requisicao"
PATH_LOG = "resultados_requisicao"
PATH_RESULTS = "resultados_requisicao"


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
    
    if GROUPS_VARIABLES:
        indices = response_for_db[result_index - 1].split(',')
        return response_for_db[result_index], indices

    return response_for_db[result_index] + "\n"


def apply_prompt_to_files(experiment, list_prompts, output_path=""):    
    for p, prompt_path in enumerate(list_prompts):
        print("-" * 50)
        prompt_text = read_txt_file(prompt_path)
        print("Using prompt: ", prompt_path)
        target_files_paths = list_raw_files_in_folder(experiment)

        # Apply the prompt
        print("Applying to files:", len(target_files_paths))

        if ALTERNATIVE_SAVE:
            list_outputs = []

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
            
            for request in range(SENTENCE_REPETITIONS):
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

                    if ALTERNATIVE_SAVE:
                        # Saving info for later output handling (json, csv, etc.)
                        file_results["raw_file_path"] = file_path
                        file_results["prompt_path"] = prompt_path
                        # file_results["raw_text"] = document_text
                        file_results["output_text"] = response
                        file_results["response_time"] = round(t2 - t1, 4)
                        file_results["input_tokens"] = input_tokens
                        file_results["output_tokens"] = output_tokens
                        file_results["total_tokens"] = input_tokens + output_tokens
                        list_outputs.append(file_results)

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

        if ALTERNATIVE_SAVE:
            prompt_name = prompt_path.split(os.sep)[-1].replace(".txt", "")
            documents_folder_name = target_files_paths[0].split(os.sep)[-2]
            base_file_name = "_".join(["experiment", prompt_name, documents_folder_name]).replace(" ", "-")

            for output_type in OUTPUT_TYPES:
                store_output_results(list_outputs, output_path, base_file_name, output_type)

            if VERBOSE:
                print("Converting csv to xlsx file.")
            convert_csv_to_xlsx(results_path)

            if VERBOSE:
                print("Formatting time variables")
            formatted_res_dir_path = get_formatted_results_path(results_path)
            convert_time_to_numeric(results_path, formatted_res_dir_path)
        
        if VERBOSE:
            print("End of execution.")

"""
TODO: Adaptar para usar o parâmetro n.
"""

def apply_group_prompts_to_files(experiment, list_prompts, output_path=""):
    target_files_paths = list_raw_files_in_folder(experiment)

    # Abrindo arquivo de resultados
    results_path = get_results_path(target_files_paths, "prompt_grupos.txt", PATH_RESULTS)
    resultados = open(results_path, "w")
    cabecalho = CABECALHOS[0]
    resultados.write(cabecalho)

    # Abrindo arquivo com log das responses
    log_path = get_log_path(target_files_paths, "prompt_grupos.txt", PATH_LOG)
    
    log = open(log_path + ".txt", "w")
    log.write("Responses\n\n")

    if ALTERNATIVE_SAVE:
        list_outputs = []

    total_tokens = 0
    # teste = 0
    for file_path in tqdm.tqdm(target_files_paths):
        # Repetições de cada sentença
        for request in range(SENTENCE_REPETITIONS):
            sentenca = get_sentence(file_path)

            # Salvando response no arquivo de log
            log.write("Sentença " + sentenca[:-1] + ":\n")
            
            resultados.write(sentenca)
            
            csv_block = ["" for i in range(len(cabecalho.split(',')) - 1)]
            for prompt_path in list_prompts:
                try:
                    print("-" * 50)
                    print("Using prompt: ", prompt_path)

                    file_results = {}

                    if VERBOSE:
                        print("=" * 50)
                        print(f"Reading file: {file_path}")

                    document_text = read_txt_file(file_path)
                    prompt_text = read_txt_file(prompt_path)
                    full_prompt = merge_prompt_and_document(document_text, prompt_text)

                    if VERBOSE:
                        print("Sending request to OpenAI")

                    t1 = time.time()
                    responses, input_tokens, output_tokens = send_prompt(full_prompt)
                    t2 = time.time()

                    # Extraindo resultado
                    response = responses[0]
                    response = response.replace("```", "").strip()
                    response_for_db = response.split('\n')
                    log.write(response + "\n\n")

                    # Somando quantidade de tokens utilizados
                    total_tokens += input_tokens + output_tokens

                    # Pegando a linha com os resultados
                    result, indices = find_results(response_for_db)
                    if result == "":
                        continue
                    
                    unordered_block = result.split(',')
                    for i in range(len(indices)):
                        if len(indices[i]) > 0 and indices[i][0] == '"':
                            indices[i] = indices[i][1:-1]
                        idx = int(indices[i]) - 1
                        csv_block[idx] = unordered_block[i]

                    if ALTERNATIVE_SAVE:
                        # Saving info for later output handling (json, csv, etc.)
                        file_results["raw_file_path"] = file_path
                        file_results["prompt_path"] = prompt_path
                        # file_results["raw_text"] = document_text
                        file_results["output_text"] = response
                        file_results["response_time"] = round(t2 - t1, 4)
                        file_results["input_tokens"] = input_tokens
                        file_results["output_tokens"] = output_tokens
                        file_results["total_tokens"] = input_tokens + output_tokens
                        list_outputs.append(file_results)

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
                    print("Erro em apply_group_prompts_to_files:", e)

            # Salvando Resultado
            resultados.write(",".join(csv_block) + "\n")
    
    log.write("Tokens utilizados no experimento: " + str(total_tokens)) 
    resultados.close()
    log.close()

    if ALTERNATIVE_SAVE:
        prompt_name = prompt_path.split(os.sep)[-1].replace(".txt", "")
        documents_folder_name = target_files_paths[0].split(os.sep)[-2]
        base_file_name = "_".join(["experiment", prompt_name, documents_folder_name]).replace(" ", "-")

        for output_type in OUTPUT_TYPES:
            store_output_results(list_outputs, output_path, base_file_name, output_type)

    if VERBOSE:
        print("Converting csv to xlsx file.")
    convert_csv_to_xlsx(results_path)

    if VERBOSE:
        print("Formatting time variables")
    formatted_res_dir_path = get_formatted_results_path(results_path)
    convert_time_to_numeric(results_path, formatted_res_dir_path)
    
    if VERBOSE:
        print("End of execution.")

def run_all_experiments():
    list_set_of_experiments = get_set_of_files_path(base_path=PATH_RAW_DOCUMENTS_FOLDERS)
    
    path_prompt = PATH_PROMPTS_GRUPOS if GROUPS_VARIABLES else PATH_PROMPTS
    
    list_prompts = get_list_of_prompts(prompt_base_path=path_prompt)
    
    # The experiments are the individual folders with raw txt files.
    for experiment in list_set_of_experiments:
        print("=" * 50)
        print("Running experiment:", experiment)

        # Apply each available prompt for each experiment
        if GROUPS_VARIABLES:
            apply_group_prompts_to_files(experiment, list_prompts, PATH_BASE_OUTPUT)
        else:
            apply_prompt_to_files(experiment, list_prompts, PATH_BASE_OUTPUT)


def main():
    run_all_experiments()


if __name__ == "__main__":
    main()
