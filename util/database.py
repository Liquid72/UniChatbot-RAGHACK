import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()
'''
SELECT CT.ClassID, CourT.CourseName, CT.DayOfWeek, CT.ClassStartTime, CT.ClassEndTime,COUNT(*), CT.ClassQuota - COUNT(*) AS CurrentQuota
FROM EnrollmentTable ET FULL OUTER JOIN
    ClassTable CT ON ET.ClassID = CT.ClassID
    INNER JOIN CourseTable CourT ON CT.CourseID = CourT.CourseID

GROUP BY CT.ClassID, CourT.CourseName, CT.ClassQuota, CT.DayOfWeek, CT.ClassStartTime, CT.ClassEndTime;
'''


class Database:
    def __init__(self) -> None:
        self.conn = pyodbc.connect(os.getenv("CONNECTION_STRING"))
        self.cursor = self.conn.cursor()

    def verifyKey(self, key: str) -> bool:
        """
        Verifies if the given key exists in the StudentTable.

        Parameters:
        - key (str): The key to be verified.

        Returns:
        - bool: True if the key exists in the StudentTable, False otherwise.
        """
        self.cursor.execute(
            'select * from StudentTable where StudentKey = ?', (key,))
        records = self.cursor.fetchone()
        if records is None:
            return False
        return True

    def fetchClassByName(self, course_name_input: str, key: str) -> tuple:
        if not self.verifyKey(key):
            return {'status': 'Error', 'message': 'Invalid Key'}

        self.cursor.execute(
            "SELECT CT.ClassID, CourT.CourseName, CT.DayOfWeek, CT.ClassStartTime, CT.ClassEndTime, CT.ClassQuota - COUNT(ET.EnrollmentID) AS CurrentQuota\
                FROM EnrollmentTable ET FULL OUTER JOIN\
                ClassTable CT ON ET.ClassID = CT.ClassID\
                INNER JOIN CourseTable CourT ON CT.CourseID = CourT.CourseID\
                WHERE CourT.CourseName = ?\
                GROUP BY CT.ClassID, CourT.CourseName, CT.ClassQuota, CT.DayOfWeek, CT.ClassStartTime, CT.ClassEndTime", (course_name_input))
        records = self.cursor.fetchall()

        return {'status': 'Success',
                'Data': records}

    def fetchStudentByKey(self, key: str) -> tuple:
        self.cursor.execute(
            'select * from StudentTable where StudentKey = ?', (key,))
        records = self.cursor.fetchone()
        if records is None:
            return {'status': 'Error',
                    'message': 'Invalid Key'}

        else:
            return {'status': 'Success',
                    'data': records}

    def insertClassByClassID(self, key: str, classID: int):
        # Log into which user using private decrypt key
        self.cursor.execute(
            'select * from StudentTable where StudentKey = ?', (key,))
        records = self.cursor.fetchone()
        if records is None:
            return {'status': 'Error',
                    'message': 'Invalid Key'}
        current_studentID = records[0]

        # verify that class is not full and make sure that it doesn't clash with other courses that has been enrolled
        self.cursor.execute(
            'select ClassQuota, DayOfWeek, ClassStartTime, ClassEndTime from ClassTable where ClassID = ?', (classID,))
        records = self.cursor.fetchone()
        original_quota, newDayOfWeek, newCST, newCET = records[0], records[1], records[2], records[3]

        self.cursor.execute(
            'select COUNT(*) from EnrollmentTable where ClassID = ?', (classID,))
        current_quota = self.cursor.fetchone()[0]
        if original_quota == current_quota:
            return {'status': 'Error',
                    'message': 'Class is full'}

        # check if there is clashes with other courses that the student is already enrolled in
        query = 'select EnrollmentID, StudentID, DayOfWeek, ClassStartTime, ClassEndTime\
                from EnrollmentTable\
                inner join ClassTable CT on EnrollmentTable.ClassID = CT.ClassID\
                and StudentID = ?'
        self.cursor.execute(query, (current_studentID,))
        enrolled_classes = self.cursor.fetchall()
        for e_class in enrolled_classes:
            if e_class[2] == newDayOfWeek:
                if (e_class[3] <= newCST and newCST <= e_class[4]) or (e_class[3] <= newCET and newCET <= e_class[4]):
                    return {'status': 'Error',
                            'message': 'Clashes with other courses'}

        # check that the students should not take the same course twice
        query = 'select distinct CT.CourseID\
                    from CourseTable\
                    inner join ClassTable CT on CourseTable.CourseID = CT.CourseID\
                    inner join EnrollmentTable ET on CT.ClassID = ET.ClassID\
                    AND StudentID = ?'
        self.cursor.execute(query, (current_studentID,))
        enrolled_courses = self.cursor.fetchall()
        self.cursor.execute(
            'select CourseID from ClassTable where ClassID = ?', (classID,))
        new_course = self.cursor.fetchone()[0]
        if new_course in enrolled_courses:
            return {'status': 'Error',
                    'message': 'Student already enrolled in this course'}
        self.cursor.execute(
            'INSERT INTO EnrollmentTable (StudentID, ClassID) values (?, ?)', (current_studentID, classID))
        self.conn.commit()
        return {'status': 'Success',
                'message': 'This Class successfully enrolled'}

    def dropClassByClassID(self, key: str, classID: int):
        # Log into which user using private decrypt key
        self.cursor.execute(
            'select * from StudentTable where StudentKey = ?', (key,))
        records = self.cursor.fetchone()
        if records is None:
            return {'status': 'Error',
                    'message': 'Invalid Key'}
        current_studentID = records[0]

        # verify that the student is enrolled in the class
        self.cursor.execute(
            'select * from EnrollmentTable where StudentID = ? and ClassID = ?', (current_studentID, classID))
        records = self.cursor.fetchone()
        if records is None:
            return {'status': 'Error',
                    'message': 'Student is not enrolled in this class'}
        else:
            # drop the student from this class
            eid = records[0]
            self.cursor.execute(
                'delete from EnrollmentTable where EnrollmentID = ?', (eid, ))
            self.conn.commit()
            return {'status': 'Success',
                    'message': 'This Class successfully dropped'}

    def fetchEnrolledClassByStudentKey(self, key: str):
        self.cursor.execute(
            'select * from StudentTable where StudentKey = ?', (key,))
        records = self.cursor.fetchone()
        if records is None:
            return {'status': 'Error',
                    'message': 'Invalid Key'}
        current_studentID = records[0]

        self.cursor.execute(
            'SELECT CT.ClassID, CourT.CourseName, CT.DayOfWeek, CT.ClassStartTime, CT.ClassEndTime FROM EnrollmentTable ET \
                INNER JOIN ClassTable CT ON ET.ClassID = CT.ClassID\
                INNER JOIN StudentTable ST on ET.StudentID = ST.StudentID\
                INNER JOIN CourseTable CourT ON CourT.CourseID = CT.CourseID\
                WHERE ST.StudentID = ?;', (current_studentID,))
        records = self.cursor.fetchall()
        if records is None:
            return {'status': 'Error',
                    'message': 'Student is not enrolled in any class'}
        else:
            return {'status': 'Success',
                    'data': records}
