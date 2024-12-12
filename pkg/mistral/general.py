from mistralai import Mistral


class General():
    def __init__(self, client: Mistral):
        self.client = client

    def list_model(self):
        return self.client.models.list()

    def chat(self, agent_id: str, msg: str):
        return self.client.agents.complete(
            
            agent_id=agent_id,
            messages=[
                {
                    "role": "user",
                    "content": msg,
                },
            ],
            
        )