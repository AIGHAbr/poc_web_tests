from IPython.display import clear_output
from openai import OpenAI

from NELL.ai import prompt_robot

openai_api_key = "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"
llm = OpenAI(api_key=openai_api_key)

def logs2robot(logs):
    logs = logs.replace("<br/>", "")
    input_text = prompt_robot + str(logs)
    response = llm.generate([input_text])
    return response.generations[0][0].text


# sample_logs = """
# {'framework': 'selenium'}
# {'loaded_url': 'https://life.stg.wellzesta.com/login'}
# {'event': 'click', 'tagName': 'input', 'alias': 'txt_email', 'detail': 'value: ', 'eventId': 'txt_email.0'}
# {'event': 'sendkeys', 'tagName': 'input', 'alias': 'txt_email', 'text': 'sandro@gmail.com', 'specialKey': 'Enter', 'eventId': 'txt_email.1'}
# {'loaded_url': 'https://life.stg.wellzesta.com/pin-login?email=sandro%40gmail.com'}
# {'event': 'click', 'tagName': 'input', 'alias': 'txt_pin', 'detail': 'value: ', 'eventId': 'txt_pin.2'}
# {'event': 'sendkeys', 'tagName': 'input', 'alias': 'txt_pin', 'text': '1234', 'specialKey': 'Enter', 'eventId': 'txt_pin.3'}
# {'loaded_url': 'https://life.stg.wellzesta.com/cacau-caregivers-united'}
# {'loaded_url': 'https://life.stg.wellzesta.com/cacau-caregivers-united/home'}"
# """

# clear_output()
# print(logs2robot(sample_logs))