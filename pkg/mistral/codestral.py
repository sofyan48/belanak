from mistralai import Mistral

class Codestral():
    def __init__(self, client: Mistral):
        self. client = client

    def chat(self, msg: str):
        model = "codestral-latest"
        prompt = """
        Your names is IankAI,
        Question:
        Helpful answer:
        """

        return self.client.fim.complete(
            model=model, 
            prompt=prompt, 
            suffix=msg,
        )