"""
Call function to read file and call function to prompt
"""

from src.file_operations import list_raw_files_in_folder
from src.api import send_prompt

import openai
import os
import time
import tiktoken
from dotenv import load_dotenv

load_dotenv()
# Access the API key using the key name from the .env file
API_KEY_OPENAI= os.getenv("OPENAI_API_KEY")

def main():

    list_files_conjunto1 = list_raw_files_in_folder("data/sentencas/Conjunto1", ext="txt")


    input_prompt = open("data/prompts/prompt.txt", "r").read()

    print("Files found:", len(list_files_conjunto1))

    for file_path in list_files_conjunto1:
        print("="*50)
        print("Reading file:", file_path)
        text = open(file_path, "r").read()


        full_prompt = input_prompt + "[" + text + "]"

        print("Sending request to OpenAI")
        
        t1 = time.time()
        response, input_tokens, output_tokens = send_prompt(
            full_prompt, 
            api_key=API_KEY_OPENAI, 
            model="gpt-4-1106-preview", 
            temperature=1.0
        )
        t2 = time.time()

        print("Response:     ", response)
        print("Response time:", round(t2-t1, 2), "seconds")
        print("Input tokens: ", input_tokens)
        print("Output tokens:", output_tokens)

        
        
    
if __name__ == "__main__":
    main()