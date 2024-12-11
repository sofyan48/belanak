from mistralai import Mistral

class MistraClient():
    def __init__(self, apikey):
        self.apikey =  apikey

    def client(self):
        return Mistral(api_key=self.apikey)
