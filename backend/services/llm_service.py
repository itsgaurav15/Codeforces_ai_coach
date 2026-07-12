import os

from groq import Groq

from dotenv import load_dotenv

from backend.config import GROQ_MODEL

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_coach(prompt):

    response = client.chat.completions.create(

        model=GROQ_MODEL,

        messages=[
            {
                "role": "system",
                "content":
                "You are an expert competitive programming coach."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.4,

        max_tokens=800

    )

    return response.choices[0].message.content