from mistralai import Mistral
class General():
    def __init__(self, client: Mistral):
        self.client = client

    def chat(self, msg: str):
        agent_id = "ag:ea58d2f9:20241211:general:c5600bed"
        prompt = """
        Your names is IankAI,
        Question:
        Helpful answer:
        """

        return self.client.agents.complete(
            agent_id=agent_id,
            messages=[
                {
                    "role": "user",
                    "content": msg,
                },
            ],
        )