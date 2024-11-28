# Reading and writing files
import json
import os
import glob
import pandas as pd

def get_set_of_files_path(base_path):
    folders = [os.path.join(base_path, f) for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    if len(folders) > 0:
        return sorted(folders)
    raise Exception("No experiments found")


def get_list_of_prompts(prompt_base_path, ext="txt"):
    list_files = glob.glob(os.path.join(prompt_base_path, "*." + ext))
    if list_files and len(list_files) > 0:
        return sorted(list_files)
    raise Exception("No prompts found")


def list_raw_files_in_folder(path_to_folder, ext="txt"):
    # List files
    list_files_paths = glob.glob(os.path.join(path_to_folder, "*." + ext))
    if list_files_paths and len(list_files_paths):
        return sorted(list_files_paths)
    raise Exception("No raw files found")


def read_txt_file(target_file, enc="utf-8"):
    return open(target_file, "r", encoding=enc).read()


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

    results_path = os.path.join(dir_path, "resposta_gpt.csv")

    return results_path

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
