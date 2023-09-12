import openai
import azure.functions as func
import json
import os
from azure.storage.blob import BlobServiceClient
from docx import Document
from ChatApi.Search.azcogsearch import AzCogSearch

def main(req: func.HttpRequest) -> func.HttpResponse:
    openai.api_type = "azure"
    openai.api_base = "https://ado-openai.openai.azure.com/"
    openai.api_version = "2023-03-15-preview"
    openai.api_key = "045d4425d72a49d896f52a734ace9e38"
    chat_reply = get_chat_response_new()
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

def read_data_from_az_storage() -> str:
    # Define your Azure Storage Account connection string
    connection_string = "DefaultEndpointsProtocol=https;AccountName=acsscopilotstorage;AccountKey=irIgLwt4dqEGrtakYyzFaUXFmQSL72M8HB5OynKNwPW3SvUrt0haTTqQiukqCM6UU3rCE4KRiz27+AStNRLFbg==;EndpointSuffix=core.windows.net"
    # Define the container name and blob (file) name
    container_name = "fileupload-acsstsgword"
    blob_name = "TestTSGData.docx"
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.join(current_directory, 'TSG')
    local_file_path = os.path.join(parent_directory, '1.docx')
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    with open(local_file_path, "wb") as local_file:
         blob_data = blob_client.download_blob()
         blob_data.readinto(local_file)
    doc = Document(local_file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def get_chat_response_new() -> str:
    try:
        # response_data = get_chat_metadata()
        user_query = "list the errors in v57appvm0 in a bulleted list?"
        az_cog_search = AzCogSearch(user_query)
        response_data = az_cog_search.search_data()
        response_data_str = ", ".join(response_data)
        response_data_str = response_data_str.replace("\n", "")
        response_data_str = response_data_str.replace("'\'", "")
        response_data_str = response_data_str.replace("\t", "")

        # response_data = read_data_from_az_storage()
        # Define the input messages
        # input_messages = [
        #     {"role": "assistant", "content": response_data},
        #     {"role": "user", "content": "what is the root cause of AnsibleUndefinedVariable?"}
        # ]
        # # Call chat endpoint
        # response = openai.ChatCompletion.create(
        #     engine="test-deployment",
        #     messages=input_messages
        # )
        # Combine the prompt and list
        input_text = f"{user_query} {response_data_str}"

        # Call the OpenAI API
        response = openai.Completion.create(
            engine="test-deployment",
            prompt=input_text,
            max_tokens=500,  # Adjust the maximum response length as needed
            api_key=openai.api_key
        )
        # Get the response from the chat endpointresponse
        instance_reply = response.choices[0].text.strip()
        return instance_reply
    except Exception as err:
        print(err)

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
