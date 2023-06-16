import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")


async def gpt_chat_completion(messages):
    print("KEYYY:", os.getenv("OPENAI_KEY"))
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.3,
    )
    return response.choices[0].messages["content"]
