import pyodbc, os
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self) -> None:
        self.conn = pyodbc.connect(os.getenv("CONNECTION_STRING"))
        self.cursor = self.conn.cursor()

    def fetchClassByName(self, course_name_input: str, key: str) -> tuple:
        # Verify key
        self.cursor.execute(
            'select * from StudentTable where StudentKey = ?', (key,))
        records = self.cursor.fetchone()
        if records is None:
            return {'status': 'Error',
                    'message': 'Invalid Key'}

        self.cursor.execute(
            "select * from ClassTable join CourseTable on ClassTable.CourseID = CourseTable.CourseID WHERE CourseTable.CourseName = ?;", (course_name_input))
        records = self.cursor.fetchall()

        output = {'status': 'Success',
                  'Data': records}
        return records

    def fetchStudentByKey(self, key: str) -> tuple:
        self.cursor.execute(
            'select * from StudentTable where StudentKey = ?', (key,))
        records = self.cursor.fetchone()
        output = {'status': 'Success',
                  'Data': records}

        return records

    