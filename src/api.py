# API call to OpenAI

"""
Uma função que faça chamadas para a API do OpenAI

Parametros
    Prompt [String]
    Modelo [GPT3 GPT4 - STRING]
    API_KEY [String, que está no .env]
    Formato do Output [csv, JSON, txt]
"""
from openai import OpenAI

import openai
import os
import tiktoken
from dotenv import load_dotenv


def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:    
    """Returns the number of tokens in a text string."""
    # Chamada:
    # num_tokens_from_string("tiktoken is great!", "cl100k_base")
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))

    return num_tokens



def send_prompt(prompt, api_key, model="text-davinci-004", temperature=0.7):
    
    # Set your OpenAI API key
    openai.api_key = api_key
    
    # Count tokens in the prompt
    prompt_tokens = num_tokens_from_string(prompt)
    
    # Generate a response using the OpenAI API
    response =  openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )

    # Extract and count tokens in the generated text from the API response
    
    generated_text = response.choices[0].message.content.strip()
    generated_tokens = num_tokens_from_string(generated_text)
    
    return generated_text, prompt_tokens, generated_tokens


def main():
    print("Loading .env")
    load_dotenv()
    # Access the API key using the key name from the .env file
    API_KEY_OPENAI= os.getenv("OPENAI_API_KEY")

    while True:
        # Example usage:
        prompt_example = input("Insira o prompt:")

        response_example, prompt_tokens, output_tokens = send_prompt(prompt_example, API_KEY_OPENAI)

        print("Prompt:", prompt_example)
        print("Response:", response_example)
        print("Total tokens:", prompt_tokens+output_tokens) 

if __name__ == "__main__":
    main()