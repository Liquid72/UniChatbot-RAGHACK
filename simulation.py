import os
from util.helper import function_manager, completion
from dotenv import load_dotenv
from openai import pydantic_function_tool
from util.schemas import *
load_dotenv()
os.system("cls")

tools = [pydantic_function_tool(GetUserInfo), pydantic_function_tool(FindCourseByName),
         pydantic_function_tool(EnrollClass), pydantic_function_tool(UnEnrollClass), pydantic_function_tool(ClassSchedule)]

messages = [
    {"role": "system", "content": 'You are Contoso University AI Chatbot'},
]

while True:
    input_message = input("User: ")
    messages.append({"role": "user", "content": input_message})
    inference = completion(messages, tools)
    if inference.choices[0].message.tool_calls:
        if len(inference.choices[0].message.tool_calls) > 1:
            messages.append(inference.choices[0].message)
            for history in inference.choices[0].message.tool_calls:
                messages.append(function_manager(history, inference))
        else:
            tools_call = inference.choices[0].message.tool_calls[0]
            # print(f"Inference Message\n\n{inference.choices[0].message}")
            messages.append(inference.choices[0].message)
            messages.append(function_manager(tools_call, inference))
        # print(messages)
        inference = completion(messages, tools)
    else:
        messages.append(inference.choices[0].message)
    print(f"History\n\n {messages}")
    print(f"AI: {inference.choices[0].message.content}")
