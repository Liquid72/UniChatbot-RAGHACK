-- Drop all tables
DROP TABLE IF EXISTS EnrollmentTable;
DROP TABLE IF EXISTS ClassTable;
DROP TABLE IF EXISTS StudentTable;
DROP TABLE IF EXISTS CourseTable;

--
use universitydb;

CREATE TABLE CourseTable
(
    CourseID   INT NOT NULL IDENTITY PRIMARY KEY,
    CourseName VARCHAR(80)
);


CREATE TABLE StudentTable
(
    StudentID   INT PRIMARY KEY IDENTITY NOT NULL,
    StudentName VARCHAR(80),
    StudentKey  VARCHAR(30),
    StudentMajor VARCHAR(50)
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
    EnrollmentID INT IDENTITY(1,1) PRIMARY KEY,
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

select *
from CourseTable;

INSERT INTO StudentTable (StudentName, StudentKey)
VALUES ('Mia Tanner', '1zorv', 'Computer Engineering'),
       ('Alex Moran', '9b26h', 'Computer Science'),
       ('Liam Frost', 'lcotl', 'Computer Engineering'),
       ('Liam Waters', 'bdvfs', 'Artificial Intelligence'),
       ('Alex Parker', 'c5qfy', 'Data Science'),
       ('Liam Chen', 'alahd', 'Data Science'),
       ('Liam Clark', 'bo4fh', 'Computer Science'),
       ('Liam Wright', '1gnry', 'Artificial Intelligence'),
       ('Liam Bennett', 's5i92', 'Computer Engineering'),
       ('Liam Grayson', 'dv8cp', 'Artificial Intelligence'),
       ('Liam Jennings', 'ed6zf', 'Data Science'),
       ('Liam Miller', 'hrdf4', 'Computer Science'),
       ('Liam Sawyer', '5se1o', 'Artificial Intelligence'),
       ('Aiden Smith', 'g8ytd', 'Computer Engineering'),
       ('Eliot Warren', 'jipmz', 'Data Science'),
       ('Liam Smith', 'qrhg0', 'Data Science'),
       ('Liam Stone', 'y23lr', 'Computer Science'),
       ('Alex Carter', '551l0', 'Computer Engineering'),
       ('Liam Morris', 'zoflr', 'Artificial Intelligence'),
       ('Liam Turner', 'mqy77', 'Data Science'),
       ('Ava Smith', 'gnnfz', 'Artificial Intelligence'),
       ('Amy Smith', 'sv3xw', 'Computer Engineering'),
       ('Liam Murphy', '1n2ww', 'Computer Science'),
       ('Liam Walker', '7140b', 'Data Science'),
       ('Liam Green', 'eidpq', 'Computer Engineering'),
       ('Liam Parker', 'ktnvs', 'Artificial Intelligence'),
       ('Liam Hendrix', 'gx8xz', 'Artificial Intelligence'),
       ('Eli Brooks', 'n4tni', 'Computer Science'),
       ('Anna Clark', 'fhekf', 'Data Science'),
       ('Liam Baker', 'i9guy', 'Computer Engineering'),
       ('Lucas Morris', 'b83e1', 'Data Science'),
       ('Liam Evans', '2xow0', 'Artificial Intelligence'),
       ('Alex Rivera', 'md3az', 'Computer Engineering'),
       ('Liam Hughes', 'otre5', 'Computer Engineering'),
       ('Alex Stone', 'arux6', 'Artificial Intelligence'),
       ('Liam Brooks', 'uvii2', 'Computer Science'),
       ('Alex Smith', 'howrj', 'Artificial Intelligence'),
       ('Ava Woods', 'maboi', 'Computer Science'),
       ('Leo Foster', 'fwzex', 'Computer Engineering'),
       ('Alex Johnson', 'mb1eo', 'Computer Engineering'),
       ('Liam Fox', '57zfe', 'Computer Science'),
       ('Lucas Green', 'v146x', 'Data Science'),
       ('Liam Carter', 'd9uqb', 'Data Science'),
       ('Alice Green', '5fub1', 'Computer Science'),
       ('Liam Reid', 'g7f6l', 'Computer Engineering'),
       ('Liam Reed', 'tpgj0', 'Artificial Intelligence'),
       ('Liam Foster', 'j67vf', 'Artificial Intelligence'),
       ('Anna Blake', '2ejvr', 'Computer Science'),
       ('Emily Brown', 'tq73s', 'Data Science'),
       ('Emma Brooks', 'hbbyt', 'Computer Engineering');

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

select * from ClassTable join CourseTable on ClassTable.CourseID = CourseTable.CourseID where CourseName = 'Calculus 1';

select * from CourseTable;
select * from StudentTable;
select * from StudentTable where StudentKey = '1zorv';

