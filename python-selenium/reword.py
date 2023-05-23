import requests
import json 

#model: text-babbage-001
#model: text-curie-001
#model: text-ada-001
#model: text-davinci-003

class RewordAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_endpoint = 'https://api.openai.com/v1/chat/completions'

    def reword_paragraph(self, paragraph, words):
        data = {
            "model": "text-davinci-003",
            "prompt": paragraph,
            "temperature": 0.3,
            "max_tokens": words,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        response = requests.post('https://api.openai.com/v1/completions', headers=headers, data=json.dumps(data))
        return response.json()
