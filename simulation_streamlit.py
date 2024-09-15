from util.helper import function_manager, completion
from dotenv import load_dotenv
from openai import pydantic_function_tool
from util.schemas import *
import streamlit as st
import os

load_dotenv()
# os.system("cls")
st.title('Contoso University AI Chatbot')

tools = [pydantic_function_tool(GetUserInfo), pydantic_function_tool(FindCourseByName),
         pydantic_function_tool(EnrollClass), pydantic_function_tool(UnEnrollClass),
         pydantic_function_tool(GetMyClassSchedule), pydantic_function_tool(GetTodayClass),
         pydantic_function_tool(GetCourseByMajor), pydantic_function_tool(FindCourseScheduleByCourseID),
         ]

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": """You are Contoso University AI Chatbot, If you got ambiguous answer, please ask again,
        If you want to know about the course, please ask the user to find the course by name,
        If you want to enroll the student to the course, please ask the user to enroll the class by classID if the user not specify class id, please ask the user to find the course by name first,
        If user said login, then the word coming after login is the student key that you must use to login, then you output the user information (the student ID, name, and major name),
        If user want to get the available classes schedule based on the courses that the major, then you output the classes schedules of the courses that correspond to their major,"""}
    ]

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
        # print(inference.choices[0].message.tool_calls)
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

        inference = completion(st.session_state.messages, tools)
        st.session_state.messages.append(
            {"role": "assistant", "content": inference.choices[0].message.content})
    else:
        st.session_state.messages.append(
            {"role": "assistant", "content": inference.choices[0].message.content})
    st.chat_message("AI").write(inference.choices[0].message.content)
