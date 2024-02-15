import os
import traceback
from openai import OpenAI
import NELL.ai.roles as roles


def get_open_ai_key():
    API_KEY = os.getenv("OPENAI_API_KEY", None)
    if API_KEY is None:
        API_KEY = input("OpenAI API Key: ")
        os.environ["OPENAI_API_KEY"] = API_KEY


def generate_robot(logs):
    try:
        client = OpenAI()
        completion = client.chat.completions.create(
            temperature=0.1,
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": roles.dev_robot},
                {"role": "user",
                 "content": f"utilize esses logs abaixo e retorne somente os scripts, nada mais. \nlogs:\n{logs}"}
            ])
        return completion.choices[0].message.content

    except Exception as ex:
        ex2 = Exception()
        ex2.__cause__ = ex
        ex2.error = f"{traceback.format_exc()}"
        raise ex2
    

def convert_to_selenium(logs):
    try:
        client = OpenAI()
        completion = client.chat.completions.create(
            temperature=0.1,
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "user",
                 "content": f"""
                    converta esses logs de navegação numa implementação python com selenium. 
                    somente o caminho feliz, o código mais simples que você conseguir. sem multiplos métodos!
                    preste atenção nos logs porque pode haver mais de uma janela aberta.
                    talvez vc tenha que controlar o handle das janelas abertas, olhe os atributos 'window_handle'.
                    mude a janela ativa se precisar. 
                    segue os logs de uso: \n
                    {logs}
                """}
            ])
        return completion.choices[0].message.content

    except Exception as ex:
        ex2 = Exception()
        ex2.__cause__ = ex
        ex2.error = f"{traceback.format_exc()}"
        raise ex2