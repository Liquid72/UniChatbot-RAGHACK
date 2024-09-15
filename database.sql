-- Drop all tables
DROP TABLE IF EXISTS EnrollmentTable;
DROP TABLE IF EXISTS ClassTable;
DROP TABLE IF EXISTS StudentTable;
DROP TABLE IF EXISTS CourseTable;
DROP TABLE IF EXISTS MajorTable;
DROP TABLE IF EXISTS MajorCourseTable;

--
use universitydb;

CREATE TABLE CourseTable
(
    CourseID   INT NOT NULL IDENTITY PRIMARY KEY,
    CourseName VARCHAR(80)
);

CREATE TABLE MajorTable
(
    MajorID   INT NOT NULL IDENTITY PRIMARY KEY,
    MajorName VARCHAR(80)
);

CREATE TABLE MajorCourseTable
(
    MajorID  INT,
    CourseID INT,
    FOREIGN KEY (MajorID) REFERENCES MajorTable (MajorID),
    FOREIGN KEY (CourseID) REFERENCES CourseTable (CourseID)
);


CREATE TABLE StudentTable
(
    StudentID   INT PRIMARY KEY IDENTITY NOT NULL,
    StudentName VARCHAR(80),
    StudentKey  VARCHAR(30),
    StudentMajorID INT,
    FOREIGN KEY (StudentMajorID) REFERENCES MajorTable (MajorID)
);

CREATE TABLE ClassTable
(
    ClassID        INT PRIMARY KEY,
    CourseID       INT,
    DayOfWeek      VARCHAR(10),
    ClassStartTime TIME,
    ClassEndTime   TIME,
    ClassQuota     INT,
    FOREIGN KEY (CourseID) REFERENCES CourseTable (CourseID)
);

CREATE TABLE EnrollmentTable
(
    EnrollmentID INT IDENTITY PRIMARY KEY,
    StudentID    INT,
    ClassID      INT,
    FOREIGN KEY (StudentID) REFERENCES StudentTable (StudentID),
    FOREIGN KEY (ClassID) REFERENCES ClassTable (ClassID)
);

INSERT INTO CourseTable (CourseName)
VALUES ('Calculus 1'),
       ('Calculus 2'),
       ('Calculus 3'),
       ('Linear Algebra'),
       ('Differential Equations'),
       ('Discrete Mathematics'),
       ('Probability and Statistics'),
       ('Networking & Security'),
       ('Data Structures'),
       ('Algorithms'),
       ('Operating Systems'),
       ('Computer Architecture'),
       ('Software Engineering'),
       ('Database Systems'),
       ('Computer Networks');

INSERT INTO MajorTable(MajorName)
VALUES ('Computer Engineering'),
       ('Computer Science'),
       ('Artificial Intelligence'),
       ('Data Science');

INSERT INTO MajorCourseTable (MajorID, CourseID)
VALUES (1, 1), (1, 2), (1, 3), (1, 8),
        (1, 9), (1, 10), (1, 11), (1, 12), (1, 15),
        (2, 1), (2, 2), (2, 3), (2, 6),
        (2, 9), (2, 10), (2, 11), (2, 12), (2, 13), (2, 14),
        (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 7),
        (3, 10), (3, 11), (3, 13), (3, 14),
        (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 7),
        (4, 9), (4, 10), (4, 13), (4, 14), (4, 15);

INSERT INTO StudentTable (StudentName, StudentKey, StudentMajorID)
VALUES ('Mia Tanner', '1zorv', 1),
       ('Alex Moran', '9b26h', 2),
       ('Liam Frost', 'lcotl', 1),
       ('Liam Waters', 'bdvfs', 3),
       ('Alex Parker', 'c5qfy', 4),
       ('Liam Chen', 'alahd', 4),
       ('Liam Clark', 'bo4fh', 2),
       ('Liam Wright', '1gnry', 3),
       ('Liam Bennett', 's5i92', 1),
       ('Liam Grayson', 'dv8cp', 3),
       ('Liam Jennings', 'ed6zf', 4),
       ('Liam Miller', 'hrdf4', 2),
       ('Liam Sawyer', '5se1o', 3),
       ('Aiden Smith', 'g8ytd', 1),
       ('Eliot Warren', 'jipmz', 4),
       ('Liam Smith', 'qrhg0', 4),
       ('Liam Stone', 'y23lr', 2),
       ('Alex Carter', '551l0', 1),
       ('Liam Morris', 'zoflr', 3),
       ('Liam Turner', 'mqy77', 4),
       ('Ava Smith', 'gnnfz', 3),
       ('Amy Smith', 'sv3xw', 1),
       ('Liam Murphy', '1n2ww', 2),
       ('Liam Walker', '7140b', 4),
       ('Liam Green', 'eidpq', 1),
       ('Liam Parker', 'ktnvs', 3),
       ('Liam Hendrix', 'gx8xz', 3),
       ('Eli Brooks', 'n4tni', 2),
       ('Anna Clark', 'fhekf', 4),
       ('Liam Baker', 'i9guy', 1),
       ('Lucas Morris', 'b83e1', 4),
       ('Liam Evans', '2xow0', 3),
       ('Alex Rivera', 'md3az', 1),
       ('Liam Hughes', 'otre5', 1),
       ('Alex Stone', 'arux6', 3),
       ('Liam Brooks', 'uvii2', 2),
       ('Alex Smith', 'howrj', 3),
       ('Ava Woods', 'maboi', 2),
       ('Leo Foster', 'fwzex', 1),
       ('Alex Johnson', 'mb1eo', 1),
       ('Liam Fox', '57zfe', 2),
       ('Lucas Green', 'v146x', 4),
       ('Liam Carter', 'd9uqb', 4),
       ('Alice Green', '5fub1', 2),
       ('Liam Reid', 'g7f6l', 1),
       ('Liam Reed', 'tpgj0', 3),
       ('Liam Foster', 'j67vf', 3),
       ('Anna Blake', '2ejvr', 2),
       ('Emily Brown', 'tq73s', 4),
       ('Emma Brooks', 'hbbyt', 1);

INSERT INTO ClassTable (ClassID, CourseID, DayOfWeek, ClassStartTime, ClassEndTime, ClassQuota) VALUES
(1, 1, 'Friday', '09:00:00', '10:00:00', 10),
(2, 1, 'Monday', '12:00:00', '13:00:00', 5),
(3, 1, 'Thursday', '09:00:00', '10:00:00', 5),
(4, 2, 'Monday', '09:00:00', '10:00:00', 5),
(5, 3, 'Friday', '12:00:00', '13:00:00', 5),
(6, 3, 'Tuesday', '13:00:00', '14:00:00', 10),
(7, 3, 'Friday', '12:00:00', '13:00:00', 5),
(8, 4, 'Monday', '10:00:00', '11:00:00', 15),
(9, 4, 'Wednesday', '09:00:00', '10:00:00', 10),
(10, 4, 'Monday', '11:00:00', '12:00:00', 10),
(11, 5, 'Wednesday', '14:00:00', '15:00:00', 15),
(12, 5, 'Thursday', '09:00:00', '10:00:00', 15),
(13, 6, 'Wednesday', '11:00:00', '12:00:00', 10),
(14, 6, 'Monday', '13:00:00', '14:00:00', 10),
(15, 7, 'Monday', '10:00:00', '11:00:00', 10),
(16, 7, 'Thursday', '14:00:00', '15:00:00', 10),
(17, 8, 'Tuesday', '13:00:00', '14:00:00', 10),
(18, 8, 'Friday', '10:00:00', '11:00:00', 10),
(19, 8, 'Tuesday', '14:00:00', '15:00:00', 15),
(20, 9, 'Wednesday', '11:00:00', '12:00:00', 10),
(21, 9, 'Monday', '11:00:00', '12:00:00', 10),
(22, 10, 'Monday', '15:00:00', '16:00:00', 15),
(23, 10, 'Friday', '11:00:00', '12:00:00', 5),
(24, 11, 'Monday', '12:00:00', '13:00:00', 10),
(25, 11, 'Monday', '09:00:00', '10:00:00', 5),
(26, 11, 'Friday', '11:00:00', '12:00:00', 5),
(27, 12, 'Wednesday', '15:00:00', '16:00:00', 5),
(28, 12, 'Monday', '15:00:00', '16:00:00', 5),
(29, 12, 'Thursday', '11:00:00', '12:00:00', 15),
(30, 13, 'Tuesday', '10:00:00', '11:00:00', 5),
(31, 14, 'Tuesday', '13:00:00', '14:00:00', 5),
(32, 14, 'Wednesday', '15:00:00', '16:00:00', 10),
(33, 14, 'Tuesday', '14:00:00', '15:00:00', 10),
(34, 15, 'Tuesday', '09:00:00', '10:00:00', 5),
(35, 15, 'Friday', '11:00:00', '12:00:00', 5);

---select * from ClassTable join CourseTable on ClassTable.CourseID = CourseTable.CourseID where CourseName = 'Calculus 1';

---select * from CourseTable;
---select * from StudentTable;
---select * from StudentTable where StudentKey = '1zorv';

