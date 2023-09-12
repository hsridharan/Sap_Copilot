from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

class AzCogSearch():
    def __init__(self, user_query: str):
        self.user_query = user_query
        # Define your Azure Cognitive Search endpoint and admin API key
        self.search_service_endpoint = "https://acsscognitivesearch.search.windows.net"
        self.admin_api_key = "yBSF8UjVARbVva6noCnlMUCFGXcUvsZF3QYKW4f8zIAzSeDi1TvP"
        self.index_name = "acsstsgword"
        # create an empty list to store the search results
        self.search_results = []
        self.search_client = None
        self.search_query = None
        self.results = None

    def search_data(self) -> list:
        # Create a search_client
        self.search_client = SearchClient(
            endpoint=self.search_service_endpoint,
            index_name=self.index_name,
            credential=AzureKeyCredential(self.admin_api_key))
        # Define your search query
        self.search_query = self.user_query
        # Execute the search query
        self.results = self.search_client.search(search_text=self.search_query)
        # Print the search results
        for result in self.results:
            self.search_results.append(result['content'])
        return self.search_results
