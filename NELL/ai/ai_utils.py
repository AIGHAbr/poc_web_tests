import os
import traceback
import NELL.ai.roles as roles
from openai import OpenAI


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