import os
import NELL.ai.roles as roles
import NELL.ai.logs_sample as logs
from openai import OpenAI

def generate_robot(logs):

    api_key = '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'
    os.environ["OPENAI_API_KEY"]=api_key

    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": roles.dev_robot},
        {"role": "user", "content": f"utilize esses logs abaixo e retorne somente os scripts, nada mais. \nlogs:\n{logs}"}
    ])
    return completion.choices[0].message.content