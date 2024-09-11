from util.helper import function_manager, completion
from dotenv import load_dotenv
from openai import pydantic_function_tool
from util.schemas import *
import streamlit as st
import os

load_dotenv()
os.system("cls")
st.title('Contoso University AI Chatbot')

tools = [pydantic_function_tool(GetUserInfo), pydantic_function_tool(FindCourseByName),
         pydantic_function_tool(EnrollClass), pydantic_function_tool(UnEnrollClass), 
         pydantic_function_tool(GetMyClassSchedule)]

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": 'You are Contoso University AI Chatbot, If you got ambiguous answer, please ask again.'}]

for msg in st.session_state.messages[1:]:
    try:
        if msg["role"] == "tool":
            pass
        elif msg["role"] == "assistant" or msg["role"] == "user":
            st.chat_message(msg["role"]).write(msg["content"])
    except TypeError:
        pass
if prompt := st.chat_input():
    if not os.getenv("AZURE_OPENAI_API_KEY"):
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    # try: 
    st.chat_message("User").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    inference = completion(st.session_state.messages, tools)
    if inference.choices[0].message.tool_calls:
        if len(inference.choices[0].message.tool_calls) > 1:
            # messages.append(inference.choices[0].message)
            st.session_state.messages.append(inference.choices[0].message)
            for history in inference.choices[0].message.tool_calls:
                # messages.append(function_manager(history, inference))
                st.session_state.messages.append(
                    function_manager(history, inference))
        else:
            tools_call = inference.choices[0].message.tool_calls[0]
            st.session_state.messages.append(
                inference.choices[0].message)
            st.session_state.messages.append(
                function_manager(tools_call, inference))

        # print(st.session_state.messages)
        inference = completion(st.session_state.messages, tools)
        print(inference)
        st.session_state.messages.append({"role": "assistant", "content": inference.choices[0].message.content})
    else:
        # messages.append(inference.choices[0].message)
        st.session_state.messages.append({"role": "assistant", "content": inference.choices[0].message.content})
    st.chat_message("AI").write(inference.choices[0].message.content)
    # except Exception as e:
    #     print(e)
    #     st.session_state.messages.append({"role": "assistant", "content": "We're sorry, but something went wrong. Please try again."})
    #     st.chat_message("AI").write("We're sorry, but something went wrong. Please try again.")

