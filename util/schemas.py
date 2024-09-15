from pydantic import BaseModel

class GetUserInfo(BaseModel):
    key: str

class FindCourseByName(BaseModel):
    course_name_input: str
    key: str

class FindCourseScheduleByCourseID(BaseModel):
    course_id: int
    key: str

class EnrollClass(BaseModel):
    key: str
    classID: int

class UnEnrollClass(BaseModel):
    key: str
    classID: int

class GetMyClassSchedule(BaseModel):
    key: str

class GetTodayClass(BaseModel):
    key: str

class GetCourseByMajor(BaseModel):
    key: str
    # major_id: int

