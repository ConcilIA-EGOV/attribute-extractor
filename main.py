"""
Call function to read file and call function to prompt
"""
import glob
import os
import time

import pandas as pd
import tqdm
from dotenv import load_dotenv

from src.api import send_prompt
from src.file_operations import list_raw_files_in_folder, read_txt_file, store_output_results

load_dotenv()
# Access the API key using the key name from the .env file
API_KEY_OPENAI = os.getenv("OPENAI_API_KEY")


def get_set_of_files_path(base_path):
    folders = [os.path.join(base_path, f) for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    return folders


def get_list_of_prompts(prompt_base_path):
    return glob.glob(os.path.join(prompt_base_path, ".txt"))


def merge_prompt_and_document(document_text, prompt):
    """
    In this way, we are sure that we follow the same pattern all the time.
    """
    return prompt + "[" + document_text + "]"


def apply_prompt_to_files(target_files_paths, prompt_path, output_path="", verbose=False, output_type="csv"):
    list_outputs = []

    for file_path in tqdm.tqdm(target_files_paths):
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
            api_key=API_KEY_OPENAI,
            model="gpt-4-1106-preview",
            temperature=1.0
        )
        t2 = time.time()

        # Saving info for later output handling (json, csv, etc.)
        file_results["raw_file_path"] = file_path
        file_results["prompt_path"] = prompt_path
        # file_results["raw_text"] = document_text
        file_results["output_text"] = response
        file_results["response_time"] = t2 - t1
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

    prompt_name = prompt_path.split(os.sep)[-1]
    documents_folder_name = target_files_paths.split(os.sep)[-1].replace(".txt", "")

    base_file_name = "_".join(["experiment", prompt_name, documents_folder_name])
    store_output_results(list_outputs, output_path, base_file_name, output_type)


def run_experiments():
    list_set_files_path = []
    list_files_conjunto1 = list_raw_files_in_folder("data/sentencas/Conjunto1", ext="txt")

    list_sets_path = get_set_of_files_path("data/sentencas")
    for experiment in list_sets_path:
        print(experiment)

    input_prompt = open("data/prompts/prompt.txt", "r").read()


def main():
    run_experiments()


if __name__ == "__main__":
    main()
