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
        {"role": "user", "content": f"utilize esses logs e crie o script do robot{logs}"}
    ])
    return completion.choices[0].message.content