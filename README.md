# (Coming Soon) Auto-GPT-Plugin-Template
A starting point for developing your own plug-in for Auto-GPT

# loading .env variables

Add the template to the autogpt repo
```
API_KEY_NAME=YOUR-API-KEY
```

Example of loading the .env in huggingface.py
```python
import dotenv

class HuggingFaceHostedInferenceModel(HuggingFaceModel):
    def query(self, model, payload: dict, temperature, max_tokens) -> dict:
        headers = {
            "Authorization": "Bearer " + dotenv.get_key(".env", "HUGGINGFACE_TOKEN")
        }
        host = dotenv.get_key(".env", "HUGGINGFACE_HOSTED_URL")
        if host:
            payload["options"] = {"use_cache": False, "wait_for_model": True}
            payload["parameters"] = {
                "top_p": 1.0,
                "temperature": temperature,
                "max_length": max_tokens,
                "return_full_text": True,
            }
            response = requests.post(host, headers=headers, json=payload)
            return response.json()
        else:
            return [{"generated_text": "Missing Hostname!"}]
```


## Testing workflow

Create something like this 
```
cd ../Auto-GPT-Plugins && zip -ru ../Auto-GPT/plugins/Auto-GPT-Plugins.zip . ; ../Auto-GPT && python3 -m autogpt --debug
```