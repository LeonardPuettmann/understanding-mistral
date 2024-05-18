# Import required libraries
import os
import time
import json
import requests
from colorama import Fore, Back, Style

# Set up API URL and headers
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

api_key = os.getenv("HUGGINGFACE_API_KEY")
if not api_key: 
    api_key = input(Fore.YELLOW + "Please provide your HuggingFace API key: ")
headers = {"Authorization": f"Bearer {api_key}"}

# Define functions for streaming and querying the API
def stream_response(response):
    for line in response.iter_lines():
        if line:  # filter out keep-alive new lines
            yield json.loads(line)

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload, stream=True)
        response.raise_for_status()  # raise an exception if the API returned an error
        return stream_response(response)
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return None

# Define the chat function and the chat history
def chat(message):
    global chat_history

    # Add the new message to the chat history
    chat_history += f"\n[INST] {message} [/INST]"

    # Make the API call
    output = query({
        "past_user_inputs": chat_history,
        "inputs": f"[INST] {message} [/INST]",
        "parameters": {
            "return_full_text": False,
            "temperature": 0.01,
            "max_new_tokens": 256,
            "stream_output": True
        }
    })

    if output is None:
        return "An error occurred. Please try again later."

    response_message = ""
    for data in output:
        response_message += data[0]["generated_text"]
        yield response_message

    # Update the chat history with the AI's response
    chat_history += f"\n{response_message}"

# Initialize chat history (this is kind the system prompt)
chat_history = "[INST] You are an AI-Assistant called Mistral. Be friendly and helpful. Keep your answer short! [/INST]"

# Define the function for printing characters in chunks
def print_characters_in_chunks(text, chunk_size=3):
    for i in range(0, len(text), chunk_size):
        print(text[i:i + chunk_size], end="", flush=True)
        time.sleep(0.05)

# Main loop for the chat interface
print(Fore.YELLOW + "Welcome to Mistral AI!" + Style.RESET_ALL + " Type 'quit' to end the conversation.")

while True:
    user_input = input(Fore.RED + "\nYou: " + Style.RESET_ALL)

    if user_input.lower() == "quit":
        print(Fore.RED + "Goodbye!" + Style.RESET_ALL)
        break

    if len(user_input) > 256:
        print("Your message is too long. Please limit it to 256 characters.")
        continue

    response = chat(user_input)
    final_response = ""
    for partial_response in response:
        final_response = partial_response
    print(Fore.YELLOW + "Mistral: " + Style.RESET_ALL, end="", flush=True)
    print_characters_in_chunks(final_response)
    print()
