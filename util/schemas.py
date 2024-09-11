from pydantic import BaseModel

class GetUserInfo(BaseModel):
    key: str

class FindCourseByName(BaseModel):
    course_name_input: str
    key: str

class EnrollClass(BaseModel):
    key: str
    classID: int

class DropClass(BaseModel):
    key: str
    classID: int

class ClassSchedule(BaseModel):
    key: str