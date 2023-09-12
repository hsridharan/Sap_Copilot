import openai
from ChatApi.Search.azcogsearch import AzCogSearch

class AzChat():
    def __init__(self, input_data: str):
        self.user_query = input_data
        self.az_cog_search = AzCogSearch(self.user_query)
        self.response_data = self.az_cog_search.search_data()
        self.response_data_str = ", ".join(self.response_data)
        self.response_data_str = \
            self.response_data_str.replace("\n", "").replace(
            "\r", "").replace("\t", "").replace("\'", "")
        openai.api_type = "azure"
        openai.api_base = "https://ado-openai.openai.azure.com/"
        openai.api_version = "2023-03-15-preview"
        openai.api_key = "045d4425d72a49d896f52a734ace9e38"
        self.response = None

    def get_chat_response(self) -> str:
        try:
            # Define the input messages
            input_messages = [
                {"role": "assistant", "content": self.response_data_str},
                {"role": "user", "content": self.user_query}
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
            print(err)
