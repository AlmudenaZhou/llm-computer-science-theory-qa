import json
import traceback

from src.client_modules.llms.openai.openai import OpenAIClient


def llm_message_processing(llm_response):
    text_response = None
    max_tries = 10
    tries = 0
    first_flag = True
    while not text_response:
        try:
            tries += 1
            if not first_flag:
                llm_response = fix_wrong_json(llm_response, error)

            first_flag = False
            llm_response = json.loads(llm_response)
            text_response = llm_response['new_content']

        except json.JSONDecodeError as e:
            error = e
            print(e)
            tb = traceback.format_exc()
        if tries >= max_tries:
            print(tb)
            break
    return text_response


def fix_wrong_json(response, error):

    prompt = """
        Se te va a pasar un contenido de un json y el error que da python al leer el formato.

        Tienes que devolver únicamente el contenido del json corregido para que se pueda leer con un json.loads(content)

        El usuario te va a pasar de input:

        "json": <json to fix>
        "error": <console message of the error>

        Y tienes que devolver:

        ```json\n
        <contenido corregido>
        \n
        ```

        Ten cuidado de solo hacer un nivel de keys en el json y que solo haya un par key-valor que sea "new_content": string
    """

    user_query = f"""
    \"json\": {response}
    \"error\": {error}
    """
    messages = [{
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": user_query,
            }]

    oai_client = OpenAIClient()
    oai_client.chat(messages)

    llm_response = delete_json_quotes(llm_response)
    return llm_response


def delete_json_quotes(llm_response):
    if llm_response.startswith('```'):
        llm_response = llm_response.split('\n')[1:-1]
        llm_response = '\n'.join(llm_response)
    return llm_response