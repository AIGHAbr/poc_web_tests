
import os
import httpx
import NELL.ai.prompts as prompts

api_key = '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'
os.environ["OPENAI_API_KEY"]=api_key

def generate_robot(logs):
    api_key = 'sua_chave_de_api'
    os.environ["OPENAI_API_KEY"] = api_key
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "gpt-4-0125-preview",  # Substitua pelo modelo de chat correto, se necessário
        "messages": [{"role": "system", "content": "Seu prompt inicial aqui"}, {"role": "user", "content": logs}]
    }
    
    response = httpx.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        return result

    raise Exception("Falha na requisição da API", response.text)

