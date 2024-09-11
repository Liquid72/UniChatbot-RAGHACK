import os
from util.helper import function_manager, completion
from dotenv import load_dotenv
from openai import pydantic_function_tool
from util.schemas import *
load_dotenv()
os.system("cls")

tools = [pydantic_function_tool(GetUserInfo), pydantic_function_tool(FindCourseByName),
         pydantic_function_tool(EnrollClass)]

messages = [
    {"role": "system", "content": 'You are an AI'},
    {"role": "user", "content": f"Key saya adalah lcotal, Carikan saya kelas Calculus 1"},
]

inference = completion(messages, tools)
tools_call = inference.choices[0].message.tool_calls[0]

messages.append(inference.choices[0].message)
messages.append(function_manager(tools_call, inference))

# print(messages)
# for m in messages:
    # print(m)

inference = completion(messages, tools)
print(inference.choices[0].message.content)


