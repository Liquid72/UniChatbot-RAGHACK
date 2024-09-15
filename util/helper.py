from util.database import Database
from openai import AzureOpenAI, pydantic_function_tool
import json
import os
Database = Database()


def completion(messages: list, tools=None):
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-07-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

    inference = client.chat.completions.create(
        model=os.getenv("DEPLOYMENT_NAME"),
        messages=messages,
        tools=tools,
        max_tokens=16384,
    )

    return inference


def function_manager(tools_call, completion):
    function_name = tools_call.function.name

    if function_name == "GetUserInfo":
        arguments = json.loads(tools_call.function.arguments)
        key = arguments['key']
        student = Database.fetchStudentByKey(key)

        function_call_message = {
            "role": "tool",
            "content": f"{student}",
            "tool_call_id": tools_call.id
        }

    elif function_name == "FindCourseByName":
        arguments = json.loads(tools_call.function.arguments)
        course_name_input = arguments['course_name_input']
        key = arguments['key']
        course = Database.fetchClassByName(course_name_input, key)

        function_call_message = {
            "role": "tool",
            "content": f"{course}",
            "tool_call_id": tools_call.id
        }

    elif function_name == "EnrollClass":
        arguments = json.loads(tools_call.function.arguments)
        key = arguments['key']
        classID = arguments['classID']
        enrollment = Database.insertClassByClassID(key, classID)

        function_call_message = {
            "role": "tool",
            "content": f"{enrollment}",
            "tool_call_id": tools_call.id
        }

    elif function_name == "UnEnrollClass":
        arguments = json.loads(tools_call.function.arguments)
        print(arguments)
        key = arguments['key']
        classID = arguments['classID']
        drop = Database.dropClassByClassID(key, classID)

        function_call_message = {
            "role": "tool",
            "content": f"{drop}",
            "tool_call_id": tools_call.id
        }

    elif function_name == "GetMyClassSchedule":
        arguments = json.loads(tools_call.function.arguments)
        key = arguments['key']
        schedule = Database.fetchEnrolledClassByStudentKey(key)

        function_call_message = {
            "role": "tool",
            "content": f"{schedule}",
            "tool_call_id": tools_call.id
        }

    elif function_name == "GetTodayClass":
        arguments = json.loads(tools_call.function.arguments)
        key = arguments['key']
        schedule = Database.fetchEnrolledClassByStudentKey(key)

        function_call_message = {
            "role": "tool",
            "content": f"{schedule}",
            "tool_call_id": tools_call.id
        }

    elif function_name == "GetCourseByMajor":
        arguments = json.loads(tools_call.function.arguments)
        print(arguments)
        key = arguments['key']
        print("TEST", key)
        classes = Database.GetCourseListByStudentID(key)
        print(classes)

        function_call_message = {
            "role": "tool",
            "content": f"{classes}",
            "tool_call_id": tools_call.id
        }

    elif function_name == "FindCourseScheduleByCourseID":
        arguments = json.loads(tools_call.function.arguments)
        course_id = arguments['course_id']
        key = arguments['key']
        course = Database.FindCourseScheduleByCourseID(course_id, key)

        function_call_message = {
            "role": "tool",
            "content": f"{course}",
            "tool_call_id": tools_call.id
        }

    return function_call_message
