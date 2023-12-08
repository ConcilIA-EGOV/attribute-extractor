# API call to OpenAI

"""
Uma função que faça chamadas para a API do OpenAI

Parametros
    Prompt [String]
    Modelo [GPT3 GPT4 - STRING]
    API_KEY [String, que está no .env]
    Formato do Output [csv, JSON, txt]
"""

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



def send_prompt(prompt, api_key, model="text-davinci-003", temperature=0.7):
    
    # Set your OpenAI API key
    openai.api_key = api_key

    # Count tokens in the prompt
    prompt_tokens = num_tokens_from_string(prompt)
    print(f"Tokens in prompt: {prompt_tokens}")

    # Generate a response using the OpenAI API
    response = openai.completions.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=500,  # You can adjust this based on your desired response length
    )

    # Extract and count tokens in the generated text from the API response
    generated_text = response.choices[0].text.strip()
    generated_tokens = num_tokens_from_string(generated_text)
    print(f"Tokens in generated text: {generated_tokens}")

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