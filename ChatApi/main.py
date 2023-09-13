"""Azure Functions HTTP Trigger Python Sample
"""
import azure.functions as func
from ChatApi.chat import AzChat

def main(req: func.HttpRequest) -> func.HttpResponse:
    """This method is used to handle HTTP request from Azure function
    """
    call_chat_api = AzChat(req.get_json().get('user_query'))
    chat_reply = call_chat_api.get_chat_response()
    return func.HttpResponse(chat_reply)
