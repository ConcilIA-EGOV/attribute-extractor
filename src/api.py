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
import random
import time

import openai
import tiktoken
from dotenv import load_dotenv


def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    # Chamada:
    # num_tokens_from_string("tiktoken is great!", "cl100k_base")
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))

    return num_tokens


def send_prompt(prompt, api_key, model="text-davinci-003", temperature=0.7, retries=3):
    if len(api_key) == 0:
        raise Exception("API Key is required.")
    if len(prompt) == 0:
        raise Exception("Prompt is empty.")

    # Set your OpenAI API key
    openai.api_key = api_key

    # Count tokens in the prompt
    prompt_tokens = num_tokens_from_string(prompt)

    for retry in range(retries):
        try:
            # Generate a response using the OpenAI API
            # response = openai.chat.completions.create(
            #     model=model,
            #     messages=[{"role": "user", "content": prompt}],
            #     temperature=temperature
            # )
            response = mock_response
            break
        except Exception as e:
            response = None
            print("Error while sending request to OpenAI: ", e)
            print("Trying again in 1 minute")
            time.sleep(60)

    if response is None:
        raise Exception("OpenAI did not respond. Stopping.")

    # Código original com a response da OpenAI
    # Extract and count tokens in the generated text from the API response
    # generated_text = response.choices[0].message.content.strip()

    # Response simulada (para desenvolvimento), devido ao não acesso à API
    generated_text = response['choices'][0]['message']['content'].strip()
    generated_tokens = num_tokens_from_string(generated_text)

    return generated_text, prompt_tokens, generated_tokens


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
