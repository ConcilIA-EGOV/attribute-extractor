# API call to OpenAI

"""
Uma função que faça chamadas para a API do OpenAI

Parametros
    Prompt [String]
    Modelo [GPT3 GPT4 - STRING]
    API_KEY [String, que está no .env]
    Formato do Output [csv, JSON, txt]
"""
from utils.mock_res import mock_response
import os
import time

import openai
import tiktoken
import sys
from dotenv import load_dotenv
sys.path.append('../config.py')
from config import API_ACCESS, TIME_BETWEEN_REQUESTS, MODEL, TEMPERATURE


# Pegando a linha com os resultados
def find_results(response_for_db:list[str]) -> str:
    result_index = None
    for i, row in enumerate(response_for_db):
        row_elements = row.split(',')
        if any((el in ["S","N",'"S"','"N"','-','null', ' ', ''] or (
            len(el) in [5, 8] and ':' in el)) for el in row_elements):
            result_index = i
            break
    
    if (result_index == None):
        result_index = 0
        response_for_db = [",".join(response_for_db)]

    return response_for_db[result_index]


def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    # Chamada:
    # num_tokens_from_string("tiktoken is great!", "cl100k_base")
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))

    return num_tokens

id = -1
def send_prompt(prompt:str, retries=1) -> tuple[str, str, int, int]:
    api_key = get_api_key()
    if len(api_key) == 0:
        raise Exception("API Key is required.")
    if len(prompt) == 0:
        raise Exception("Prompt is empty.")

    # Set your OpenAI API key
    openai.api_key = api_key

    for retry in range(retries):
        try:
            if API_ACCESS:
                # Generate a response using the OpenAI API
                response = openai.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=TEMPERATURE
                )
                if TIME_BETWEEN_REQUESTS:
                    time.sleep(TIME_BETWEEN_REQUESTS)
            else:
                global id
                id = (id + 1) % 3
                response = mock_response['choices'][id]
            break
        except Exception as e:
            response = None
            print("Error while sending request to OpenAI: ", e)
            # print("Trying again in 1 minute")
            # time.sleep(60)

    if response is None:
        raise Exception("OpenAI did not respond.")

    if API_ACCESS:
        # Extract and count tokens in the generated text from the API response
        log_response = response.choices[0].message.content.replace("```", "").strip()
        generated_tokens = response.usage.completion_tokens
        prompt_tokens = response.usage.prompt_tokens
    else:
        # Response simulada (para desenvolvimento), devido ao não acesso à API
        log_response = response['message']['content'].replace("```", "").strip()
        prompt_tokens = num_tokens_from_string(prompt)
        generated_tokens = 0
        for text in log_response:
            generated_tokens += num_tokens_from_string(text)
    response = find_results(log_response.split('\n'))
    return log_response, response, prompt_tokens, generated_tokens


def get_api_key():
    load_dotenv()
    # Access the API key using the key name from the .env file
    return os.getenv("OPENAI_API_KEY")


def main():
    """
    A test-bed to check whether the OpenAI API is available.
    """

    while True:
        # Example usage:
        prompt_example = input("\n\nInsira o prompt: ")
        api_key_openai = get_api_key()

        response_example, prompt_tokens, output_tokens = send_prompt(prompt_example, api_key_openai)

        print("Prompt:", prompt_example)
        print("Response:", response_example)
        print("Total tokens:", prompt_tokens + output_tokens)


if __name__ == "__main__":
    main()
