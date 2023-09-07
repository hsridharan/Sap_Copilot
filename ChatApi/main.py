import openai
import azure.functions as func
import json
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    openai.api_type = "azure"
    openai.api_base = "https://ado-openai.openai.azure.com/"
    openai.api_version = "2023-03-15-preview"
    openai.api_key = "045d4425d72a49d896f52a734ace9e38"
    chat_reply = get_chat_response()
    return func.HttpResponse(chat_reply)

def get_chat_metadata() -> str:
    # Get the current directory of the script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Navigate to the parent directory
    parent_directory = os.path.join(current_directory, 'DataFiles')
    # Specify the relative path to the file you want to open (data.json in this case)
    file_path = os.path.join(parent_directory, 'VISMetadata.json')
    # Open the JSON file for reading
    with open(file_path, 'r') as json_file:
        # Load the JSON data from the file
        data = json.load(json_file)
    # Convert the loaded JSON data to a string
    json_string = json.dumps(data, indent=4)
    return json_string

def get_chat_response() -> str:
    try:
        response_data = get_chat_metadata()
        # Define the input messages
        input_messages = [
            {"role": "assistant", "content": response_data},
            {"role": "user", "content": "I want to know the disk configuration of my database server"}
        ]
        # Call chat endpoint
        response = openai.ChatCompletion.create(
            engine="test-deployment",
            messages=input_messages
        )
        # Get the response from the chat endpoint
        instance_reply = response['choices'][0]['message']['content']
        return instance_reply
    except Exception as err:
        print(err)
