"""This module is used to handle search response from Azure search endpoint
"""
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Replace these with your own values, either in environment variables or directly here
AZURE_SEARCH_SERVICE = os.environ.get("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX")
AZURE_ADMIN_API_KEY = os.environ.get("AZURE_ADMIN_API_KEY")

class AzCogSearch():
    """This class is used to handle search response from Azure search endpoint
    """
    def __init__(self, user_query: str):
        self.user_query = user_query
        # create an empty list to store the search results
        self.search_results = []
        self.search_client = None
        self.search_query = None
        self.results = None

    def search_data(self) -> list:
        """This method is used to get search response from Azure search endpoint
        """
        try:
            # Create a search_client
            self.search_client = SearchClient(
                endpoint=AZURE_SEARCH_SERVICE,
                index_name=AZURE_SEARCH_INDEX,
                credential=AzureKeyCredential(AZURE_ADMIN_API_KEY))

            # Define your search query
            self.search_query = self.user_query
            top = 3
            # Execute the search query
            self.results = self.search_client.search(search_text=self.search_query,
                                        semantic_configuration_name="default",
                                        top=top)
            for result in self.results:
                self.search_results.append(result['content'])
            return self.search_results
        except Exception as err:
            raise err
