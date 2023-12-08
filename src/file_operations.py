# Reading and writing files

import os
import glob

### Função: Read .txt files in folder
def list_raw_files_in_folder(path_to_folder, ext="txt"):

    # List files
    # Read the files

    list_files_paths = glob.glob(path_to_folder + os.sep + "*." + ext)

    return sorted(list_files_paths)

    # path_to_folder = "data"
    # arquivo: data/1.txt
    # data -> path_to_folder
    # separador -> os.sep (funcionando pra qualquer OS)
    # "*.txt" -: "*." + ext



