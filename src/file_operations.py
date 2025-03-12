# Reading and writing files
import json
import os
import glob
import pandas as pd

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

def merge_prompt_and_document(document_text, prompt):
    """
    combine the prompt and the document text in a fixed way
    """
    # In this way, we are sure that we follow the same pattern all the time.
    return prompt + os.linesep + "[ " + document_text + " ]"


def get_set_of_files_path(base_path):
    '''
    return a folder list
    '''
    folders = [os.path.join(base_path,f)
               for f in os.listdir(base_path)
                if os.path.isdir(
                    os.path.join(base_path, f))]
    if len(folders) > 0:
        # It's important to sort the folders for output consistency
        return sorted(folders)
    raise Exception("No experiments found")


def get_list_of_prompts(prompt_base_path):
    """
    List all files in the prompt folder
    """
    list_files = glob.glob(os.path.join(prompt_base_path, "*"))
    if list_files and len(list_files) > 0:
        # It's important to sort the files for output consistency
        return sorted(list_files)
    return []


def list_raw_files_in_folder(path_to_folder, ext="txt"):
    """
    List all files in the folder with a specific extension,
    default is txt
    """
    list_files_paths = glob.glob(os.path.join(path_to_folder, "*." + ext))
    if list_files_paths and len(list_files_paths):
        # It's important to sort the files for output consistency
        return sorted(list_files_paths)
    raise Exception("No raw files found")


def read_txt_file(target_file, enc="utf-8"):
    return open(target_file, "r", encoding=enc).read()

def read_prompt(prompt_file, enc="utf-8"):
    """
    Read the prompt file path and return a list of prompts
    """
    # verifies if is a directory
    if os.path.isdir(prompt_file):
        # returns a list of files in the directory
        prompt_list = list_raw_files_in_folder(prompt_file)
        return [read_txt_file(p, enc) for p in prompt_list]
    return [read_txt_file(prompt_file, enc)]


def ensure_directory_exists(path):
    os.makedirs(path, exist_ok=True)


def store_output_results(list_outputs, output_path, base_folder_name, output_type):
    print("Saving results to " + output_path + " using " + output_type.upper() + " format")

    final_output_path = os.path.join(output_path, base_folder_name)
    ensure_directory_exists(final_output_path)

    if output_type.lower() not in ["csv", "log", "json", "txt"]:
        raise Exception("Output type not recognized")

    if output_type.lower() == "csv":
        df = pd.DataFrame(list_outputs)
        path_to_csv = os.path.join(final_output_path, "csv")
        ensure_directory_exists(path_to_csv)
        file_path = os.path.join(path_to_csv, "output.csv")

        df.to_csv(file_path, index=False)

    elif output_type.lower() == "log":

        raise Exception("Output type 'log' not implemented")
    elif output_type.lower() == "txt":
        # Create a folder just the raw files
        raw_files_folder = os.path.join(final_output_path, "txt")
        ensure_directory_exists(raw_files_folder)

        # Just the text file is saved
        for output in list(list_outputs):
            raw_file_name = output["raw_file_path"].split(os.sep)[-1]
            text = output["output_text"]

            file_path = os.path.join(raw_files_folder, raw_file_name)
            with open(file_path, "w") as fp:
                fp.write(text)
    elif output_type.lower() == "json":
        file_path = os.path.join(final_output_path, "csv", "output.csv")
        with open(file_path, 'w') as json_file:
            json.dump(list_outputs, json_file, indent=4)


def get_results_path(target_files_paths, prompt_path, PATH_BASE_OUTPUT):
    """
    Local onde será salvo o arquivo csv com o resultado das requisições
    """
    prompt_name = prompt_path.split(os.sep)[-1].replace(".txt", "")
    documents_folder_name = target_files_paths[0].split(os.sep)[-2]

    base_dir_name = "_".join([prompt_name, documents_folder_name]).replace(" ", "-")

    dir_path = os.path.join(PATH_BASE_OUTPUT, base_dir_name)
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    results_path = os.path.join(dir_path, prompt_name + ".csv")

    return results_path

def get_sentence(file_path:str) -> str:
    """
    Get the sentence number from the file path
    """
    # file path until the '.txt'
    arquivo = list(file_path[:-4])
    arquivo.reverse()
    # limit is the index of the last (originally) '/'
    limite = arquivo.index('/')
    # the sentence number is the string between the last '/' and the '.'
    # (the file name)
    temp = arquivo[:limite]
    temp.reverse()
    sentenca = "".join(temp)
    return sentenca


def get_log_path(target_files_paths, prompt_path, PATH_LOG):
    """
    Retorna o caminho onde será salvo o log com as responses do experimento
    """
    prompt_name = prompt_path.split(os.sep)[-1].replace(".txt", "")
    documents_folder_name = target_files_paths[0].split(os.sep)[-2]

    base_dir_name = "_".join([prompt_name, documents_folder_name]).replace(" ", "-")

    dir_path = os.path.join(PATH_LOG, base_dir_name)
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    log_path = os.path.join(dir_path, "log_requisicao")

    return log_path
