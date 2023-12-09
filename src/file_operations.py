# Reading and writing files
import json
import os
import glob
import pandas as pd


def list_raw_files_in_folder(path_to_folder, ext="txt"):
    # List files
    list_files_paths = glob.glob(path_to_folder + os.sep + "*." + ext)
    return sorted(list_files_paths)


def read_txt_file(target_file, enc="utf-8"):
    return open(target_file, "r", encoding=enc).read()


def ensure_directory_exists(path):
    os.makedirs(path, exist_ok=True)


def store_output_results(list_outputs, output_path, base_folder_name, output_type):
    print("Saving results to " + output_path + "using " + output_type)

    final_output_path = os.path.join(output_path, base_folder_name)
    ensure_directory_exists(final_output_path)

    if output_type.lower() not in ["csv", "log", "json", "txt"]:
        raise Exception("Output type not recognized")

    if output_type.lower() == "csv":
        df = pd.DataFrame(list_outputs)
        df.to_csv(os.path.join(final_output_path, "csv", "output.csv"), index=False)
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

