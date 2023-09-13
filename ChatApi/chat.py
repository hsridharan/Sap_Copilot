"""This module is used to handle chat response from OpenAI chat endpoint"""
import os
import openai
from ChatApi.Search.azcogsearch import AzCogSearch

AZURE_OPENAI_API_BASE = os.environ.get("AZURE_OPENAI_API_BASE")
AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENGINE = os.environ.get("AZURE_OPENAI_ENGINE") #gpt-35-turbo-16K

class AzChat():
    """This class is used to handle chat response from OpenAI chat endpoint"""
    def __init__(self, input_data: str):
        self.user_query = input_data
        self.az_cog_search = AzCogSearch(self.user_query)
        self.response_data = self.az_cog_search.search_data()
        self.response_data_str = ", ".join(self.response_data)
        self.response_data_str = \
            self.response_data_str.replace("\n", "").replace(
            "\r", "").replace("\t", "").replace("\'", "")
        openai.api_type = "azure"
        openai.api_base = AZURE_OPENAI_API_BASE
        openai.api_version = AZURE_OPENAI_API_VERSION
        openai.api_key = AZURE_OPENAI_API_KEY
        self.response = None

    def get_chat_response(self) -> str:
        """This method is used to get chat response from OpenAI chat endpoint"""
        try:
            system_prompt = "I am search engine for Azure center for SAP Solutions (ACSS)."
            # Define the input messages
            input_messages = [
                 {"role": "system", "content": system_prompt},
                 {"role": "assistant", "content": self.response_data_str},
                 {"role": "user", "content": self.user_query},
             ]

            # Call chat endpoint
            self.response = openai.ChatCompletion.create(
                 engine="test-deploy",
                 messages=input_messages,
                 max_tokens=500,  # Adjust the maximum response length as needed
                 api_key=openai.api_key,
                 temperature=0
            )

            # Get the response from the chat endpoint
            instance_reply = self.response['choices'][0]['message']['content']
            return instance_reply
        except Exception as err:
            raise err
