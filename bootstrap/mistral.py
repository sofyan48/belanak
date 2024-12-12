from pkg.mistral import MistraClient
from pkg.mistral.codestral import Codestral
from pkg.mistral.finetune import Finetune
from pkg.mistral.general import General
from mistralai import Mistral
import os


def mistral_client():
    client = MistraClient(
        apikey= os.environ.get("MISTRAL_APIKEY")
    )
    return client.client()

def codestral_client(client: Mistral):
    return Codestral(client)

def fine_tuning(client: Mistral):
    return Finetune(client)

def general_chat(client: Mistral):
    return General(client)