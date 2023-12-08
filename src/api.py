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
from tiktoken import TokenCounter
from dotenv import load_dotenv

def count_tokens(text):
    # Count tokens using tiktoken
    token_counter = TokenCounter()
    token_counter.count(text)

    return token_counter

def prompt(prompt, api_key, model="text-davinci-003", temperature=0.7):
    
    # Set your OpenAI API key
    openai.api_key = api_key

    # Count tokens in the prompt
    prompt_tokens = count_tokens(prompt).total
    print(f"Tokens in prompt: {prompt_tokens}")

    # Generate a response using the OpenAI API
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=500,  # You can adjust this based on your desired response length
    )

    # Extract and count tokens in the generated text from the API response
    generated_text = response.choices[0].text.strip()
    generated_tokens = count_tokens(generated_text).total
    print(f"Tokens in generated text: {generated_tokens}")

    return generated_text, prompt_tokens, generated_tokens


def main():
    load_dotenv()
    # Access the API key using the key name from the .env file
    API_KEY_OPENAI= os.getenv("OPENAI_API_KEY")

    # Example usage:
    prompt_example = "Translate the following English text to French: 'Hello, how are you?'"

    response_example, prompt_tokens, output_tokens = prompt(prompt_example, API_KEY_OPENAI)

    print("Prompt:", prompt_example)
    print("Response:", response_example)
    print("Total tokens:", prompt_tokens+output_tokens) 