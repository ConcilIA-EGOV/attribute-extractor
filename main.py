"""
Call function to read file and call function to prompt
"""
import os
import time

import tqdm

from config import sentence_repetitions, time_between_requests, alternative_save, output_types, verbose
from src.api import send_prompt, get_api_key
from src.file_operations import list_raw_files_in_folder, read_txt_file, store_output_results, get_set_of_files_path, \
    get_list_of_prompts, get_results_path, get_log_path, convert_csv_to_xlsx, get_formatted_results_path
from src.time_converter import convert_time_to_numeric

PATH_RAW_DOCUMENTS_FOLDERS = "data/sentencas"
PATH_PROMPTS = "data/prompts"
PATH_BASE_OUTPUT = "data/resultados"
PATH_LOG = "data/log"
PATH_RESULTS = "resultados"


def merge_prompt_and_document(document_text, prompt):
    """
    In this way, we are sure that we follow the same pattern all the time.
    """
    return prompt + os.linesep + "[ " + document_text + " ]"

def apply_prompt_to_files(target_files_paths, prompt_path, output_path=""):
    if alternative_save:
        list_outputs = []

    # Abrindo arquivo com log das responses
    log_path = get_log_path(target_files_paths, prompt_path, PATH_LOG)
    log = open(log_path + ".txt", "w")
    log.write("Responses\n\n")

    # Abrindo arquivo de resultados
    results_path = get_results_path(target_files_paths, prompt_path, PATH_RESULTS)
    resultados = open(results_path, "w")
    resultados.write("Sentença,direito de arrependimento,descumprimento de oferta,extravio definitivo,extravio temporário,intervalo de extravio,violação,cancelamento (sem realocação)/alteração de destino,atraso de voo,intervalo de atraso,culpa exclusiva do consumidor,inoperabilidade do aeroporto,no show,overbooking,assistência da companhia aérea,agência de viagem,hipervulnerabilidade\n")

    try:
        # teste = 0
        for file_path in tqdm.tqdm(target_files_paths):
            
            # Repetições de cada sentença
            for request in range(sentence_repetitions):
                file_results = {}

                if verbose:
                    print("=" * 50)
                    print(f"Reading file: {file_path}")

                document_text = read_txt_file(file_path)
                prompt_text = read_txt_file(prompt_path)
                full_prompt = merge_prompt_and_document(document_text, prompt_text)

                if verbose:
                    print("Sending request to OpenAI")

                t1 = time.time()
                response, input_tokens, output_tokens = send_prompt(
                    full_prompt,
                    api_key=get_api_key(),
                    model="gpt-4-1106-preview",
                    temperature=1.0
                )
                t2 = time.time()

                # if teste == 6:
                #     raise Exception("Testando interrupções")

                # Extraindo resultado
                response = response.replace("```", "").strip()
                response_for_db = response.split('\n')
                arquivo = list(file_path[:-4])
                arquivo.reverse()
                limite = arquivo.index('/')
                temp = arquivo[:limite]
                temp.reverse()
                sentenca = "".join(temp) + ','

                # Salvando response no arquivo de log
                log.write("Sentença " + sentenca[:-1] + ":\n")
                log.write(response + "\n\n")
                # log.write("Response Time: " + str(round(t2 - t1, 4)) + "\n")
                # log.write("Input tokens: " + str(input_tokens) + "\n")
                # log.write("Output tokens: " + str(output_tokens) + "\n")
                # log.write("Total tokens: " + str(input_tokens + output_tokens) + "\n")

                # Pegando a linha com os resultados
                result_index = None
                for i, row in enumerate(response_for_db):
                    row_elements = row.split(',')[:4]
                    if (len(row_elements) > 3 and any(element == "S" or element == "N" for element in row_elements)):
                        result_index = i
                        break
                
                if (result_index == None):
                    csv_block = sentenca + "-,"*15 + '-' + "\n"
                else:
                    csv_block = sentenca + response_for_db[result_index] + "\n"

                # Salvando Resultado
                resultados.write(csv_block)

                if alternative_save:
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

                if verbose:
                    print("Response:")
                    print("-" * 10)
                    print(response.replace("```", "").strip())
                    print("-" * 10)
                    print(f"Response time: {round(t2 - t1, 3)} seconds")
                    print(f"Input tokens: {input_tokens}")
                    print(f"Output tokens: {output_tokens}")
                
                if time_between_requests:
                    time.sleep(time_between_requests)
            
                # teste += 1
    
    except Exception as e:
        print(e)
    finally:      
        resultados.close()
        log.close()

    if alternative_save:
        prompt_name = prompt_path.split(os.sep)[-1].replace(".txt", "")
        documents_folder_name = target_files_paths[0].split(os.sep)[-2]
        base_file_name = "_".join(["experiment", prompt_name, documents_folder_name]).replace(" ", "-")

        for output_type in output_types:
            store_output_results(list_outputs, output_path, base_file_name, output_type)

    if verbose:
        print("Converting csv to xlsx file.")
    convert_csv_to_xlsx(results_path)

    if verbose:
        print("Formatting time variables")
    formatted_res_dir_path = get_formatted_results_path(results_path)
    convert_time_to_numeric(results_path, formatted_res_dir_path)
    
    if verbose:
        print("End of execution.")

def run_all_experiments():
    list_set_of_experiments = get_set_of_files_path(base_path=PATH_RAW_DOCUMENTS_FOLDERS)
    list_prompts = get_list_of_prompts(prompt_base_path=PATH_PROMPTS)

    # The experiments are the individual folders with raw txt files.
    for experiment in list_set_of_experiments:
        print("=" * 50)
        print("Running experiment:", experiment)

        # Apply each available prompt for each experiment
        for prompt in list_prompts:
            print("-" * 50)
            print("Using prompt: ", prompt)
            raw_files_path = list_raw_files_in_folder(experiment)

            # Apply the prompt
            print("Applying to files:", len(raw_files_path))
            apply_prompt_to_files(raw_files_path, prompt, PATH_BASE_OUTPUT)


def main():
    run_all_experiments()


if __name__ == "__main__":
    main()
