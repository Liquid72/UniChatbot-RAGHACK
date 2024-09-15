import pyodbc
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

'''
SELECT * FROM EnrollmentTable ET
         INNER JOIN StudentTable ST ON ST.StudentID = ET.StudentID
        INNER JOIN ClassTable CLT ON CLT.ClassID = ET.ClassID
         INNER JOIN CourseTable CT ON CT.CourseID = CLT.CourseID
WHERE ST.StudentName = 'Liam Frost'
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
            "SELECT CT.ClassID AS 'Class ID', CourT.CourseName, CT.DayOfWeek, CT.ClassStartTime, CT.ClassEndTime, CT.ClassQuota - COUNT(ET.EnrollmentID) AS 'Current Class Quota'\
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
            'select ST.StudentID, ST.StudentName, MT.MajorName from StudentTable ST\
              INNER JOIN MajorTable MT ON MT.MajorID = ST.StudentMajorID\
              where StudentKey = ?', (key,))
        records = self.cursor.fetchone()
        print(records)
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
        current_majorID = records[3]

        # Check student is eligible to take this course
        print(f"Key: {key} - {type(key)} - {current_studentID} - {type(current_studentID)} - {classID} - {type(classID)}")
        if self.checkEligibilityEnrollCourseByMajorID(key, current_majorID, classID)['status'] == 'Error':
            return {'status': 'Error',
                    'message': 'This student is not allowed to take this course'}

        # check that the students should not take the same course twice
        query = 'select CT.CourseID\
                    FROM EnrollmentTable ET\
                    INNER JOIN ClassTable CLT ON ET.ClassID = CLT.ClassID\
                    INNER JOIN CourseTable CT ON CT.CourseID = CLT.CourseID\
                    WHERE ET.StudentID = ?'
        self.cursor.execute(query, (current_studentID,))
        enrolled_courses = self.cursor.fetchall()
        self.cursor.execute(
            'select CourseID from ClassTable where ClassID = ?', (classID,))
        new_course = self.cursor.fetchone()[0]
        for i in enrolled_courses:
            if i[0] == new_course:
                return {'status': 'Error',
                    'message': 'Student already enrolled in this course'}
    
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

    def checkEligibilityEnrollCourseByMajorID(self, key: str, majorID: int, courseID: int):
        print(f"Data Passed | Key: {key} - {type(key)} - {majorID} - {type(majorID)} - {courseID} - {type(courseID)}")
        self.cursor.execute(
            'select * from StudentTable where StudentKey = ?', (key,))
        records = self.cursor.fetchone()
        if records is None:
            return {'status': 'Error',
                    'message': 'Invalid Key'}
        current_studentID = records[0]
        self.cursor.execute(
            'select * from MajorCourseTable where MajorID = ? and CourseID = ?', (majorID, courseID))
        records = self.cursor.fetchall()
        if records is None:
            return {'status': 'Error',
                    'message': 'This student is not allowed to take this course'}
        else:
            return {'status': 'Success',
                    'data': records}

    def GetCourseListByStudentID(self, key: str):
        self.cursor.execute(
            'select * from StudentTable where StudentKey = ?', (key,))
        records = self.cursor.fetchone()
        if records is None:
            return {'status': 'Error',
                    'message': 'Invalid Key'}
        current_studentID = records[0]

        "Fetch Major ID By StudentID"
        self.cursor.execute(
            'select StudentMajorID from StudentTable where StudentID = ?', (current_studentID,))
        current_majorID = self.cursor.fetchone()[0]

        self.cursor.execute(
            'select CT.CourseID, CT.CourseName from MajorCourseTable MCT\
                INNER JOIN CourseTable CT on MCT.CourseID = CT.CourseID\
                WHERE MCT.MajorID = ?', (current_majorID,))
        records = self.cursor.fetchall()

        print(records)
        if records is None:
            print('No course found for this major')
            return {'status': 'Error',
                    'message': 'No course found for this major'}
        else:
            output = []
            for i in records:
                output.append({'CourseID': i[0], 'CourseName': i[1]})
            print('Success')
            return {'status': 'Success',
                    'data': output}
        
    def checkTodayScedule(self, key: str):
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
                WHERE ST.StudentID = ? AND CT.DayOfWeek = ?', (current_studentID, datetime.today().weekday()))
        records = self.cursor.fetchall()
        if records is None:
            return {'status': 'Error',
                    'message': 'Student is not enrolled in any class or no class today'}
        else:
            return {'status': 'Success',
                    'data': records}
        
    def FindCourseScheduleByCourseID(self, course_id: int, key: str):
        self.cursor.execute(
            'select * from StudentTable where StudentKey = ?', (key,))
        records = self.cursor.fetchone()
        if records is None:
            return {'status': 'Error',
                    'message': 'Invalid Key'}
        current_studentID = records[0]

        query = 'select * from ClassTable where CourseID = ?;'
        self.cursor.execute(query, (course_id,))
        records = self.cursor.fetchall()
        if records is None:
            return {'status': 'Error',
                    'message': 'No class found for this course'}
        else:
            return {'status': 'Success',
                    'data': records}