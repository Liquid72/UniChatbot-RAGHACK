""""
Todo: 
1. Fetch data dari SQL
2. Input data ke SQL
"""

import os
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-07-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

completion = client.chat.completions.create(
        model=os.getenv("DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": 'You are an AI'},
            {"role": "user", "content": f"Halo"},
        ],
        max_tokens=16384,
    )

print(completion.choices[0].message.content)