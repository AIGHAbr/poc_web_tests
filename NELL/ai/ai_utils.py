import os
import NELL.ai.prompts as prompts
from langchain_openai import OpenAI

def generate_robot(logs):
    api_key = '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'
    os.environ["OPENAI_API_KEY"]=api_key
    llm = OpenAI(api_key=api_key, model_name="gpt-4-0125-preview")
    prompt = prompts.prompt_robot + logs

    response = llm.generate(
        [prompt],
        temperature=0.1
    )

    return response.generations[0][0].text