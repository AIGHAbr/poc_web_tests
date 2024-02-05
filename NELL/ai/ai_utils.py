import os
import NELL.ai.prompts as prompts
from langchain_openai import OpenAI

def generate_robot(logs):
    os.environ["OPENAI_API_KEY"]='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'
    llm = OpenAI()
    prompt = prompts.prompt_robot + logs

    response = llm.generate(
        [prompt], 
        temperature=0.1,
    )

    return response.generations[0][0].text