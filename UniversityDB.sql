-- ===============================
-- DATABASE: UniversityDB_Final_Pro
-- ===============================
DROP DATABASE IF EXISTS UniversityDB;
CREATE DATABASE UniversityDB;
USE UniversityDB;
SET FOREIGN_KEY_CHECKS = 0;

-- ===============================
-- DEPARTMENT
-- ===============================
CREATE TABLE department (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_code VARCHAR(10) UNIQUE NOT NULL,
    dept_name VARCHAR(100) NOT NULL,
    dept_head VARCHAR(100)
);

INSERT INTO department (dept_code, dept_name, dept_head) VALUES
('CSE', 'Computer Science and Engineering', 'Dr. Anitha Rao'),
('ECE', 'Electronics and Communication Engineering', 'Dr. Ramesh Gowda'),
('EEE', 'Electrical and Electronics Engineering', 'Dr. Meena Iyer'),
('ME', 'Mechanical Engineering', 'Dr. Sanjay Rao'),
('CIV', 'Civil Engineering', 'Dr. Ravi Kumar'),
('IT', 'Information Technology', 'Dr. Sneha Nair');

-- ===============================
-- FACULTY
-- ===============================
CREATE TABLE faculty (
    faculty_id INT AUTO_INCREMENT PRIMARY KEY,
    faculty_name VARCHAR(100),
    designation VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(15),
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

INSERT INTO faculty (faculty_name, designation, email, phone, dept_id) VALUES
('Dr. Rajesh Kumar', 'Professor', 'rajesh.cse@univ.edu', '9876543210', 1),
('Dr. Priya Sharma', 'Professor', 'priya.ece@univ.edu', '9876543211', 2),
('Dr. Karthik Menon', 'Professor', 'karthik.eee@univ.edu', '9876543212', 3),
('Dr. Manoj Patil', 'Professor', 'manoj.me@univ.edu', '9876543213', 4),
('Dr. Kavya Reddy', 'Professor', 'kavya.civ@univ.edu', '9876543214', 5),
('Dr. Harish Bhat', 'Professor', 'harish.it@univ.edu', '9876543215', 6);

-- ===============================
-- SUBJECT (5 per semester per dept)
-- ===============================
CREATE TABLE subject (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_code VARCHAR(10),
    subject_name VARCHAR(100),
    semester INT,
    credits INT,
    dept_id INT,
    faculty_id INT,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
);

-- CSE Subjects (3rd Sem)
INSERT INTO subject (subject_code, subject_name, semester, credits, dept_id, faculty_id) VALUES
('CS301', 'Data Structures', 3, 4, 1, 1),
('CS302', 'OOP using Java', 3, 3, 1, 1),
('CS303', 'Computer Organization', 3, 3, 1, 1),
('CS304', 'Discrete Mathematics', 3, 4, 1, 1),
('CS305', 'Operating Systems', 3, 4, 1, 1);

-- ECE Subjects (3rd Sem)
INSERT INTO subject (subject_code, subject_name, semester, credits, dept_id, faculty_id) VALUES
('EC301', 'Signals & Systems', 3, 4, 2, 2),
('EC302', 'Analog Circuits', 3, 3, 2, 2),
('EC303', 'Digital Logic Design', 3, 3, 2, 2),
('EC304', 'Electromagnetics', 3, 4, 2, 2),
('EC305', 'Microprocessors', 3, 4, 2, 2);

-- EEE Subjects (5th Sem)
INSERT INTO subject (subject_code, subject_name, semester, credits, dept_id, faculty_id) VALUES
('EE501', 'Power Systems', 5, 4, 3, 3),
('EE502', 'Electrical Machines', 5, 3, 3, 3),
('EE503', 'Control Systems', 5, 3, 3, 3),
('EE504', 'Power Electronics', 5, 4, 3, 3),
('EE505', 'Renewable Energy', 5, 3, 3, 3);

-- ME Subjects (2nd Sem)
INSERT INTO subject (subject_code, subject_name, semester, credits, dept_id, faculty_id) VALUES
('ME201', 'Engineering Mechanics', 2, 4, 4, 4),
('ME202', 'Thermodynamics', 2, 3, 4, 4),
('ME203', 'Manufacturing Tech', 2, 3, 4, 4),
('ME204', 'Fluid Mechanics', 2, 4, 4, 4),
('ME205', 'Material Science', 2, 3, 4, 4);

-- CIV Subjects (4th Sem)
INSERT INTO subject (subject_code, subject_name, semester, credits, dept_id, faculty_id) VALUES
('CV401', 'Structural Mechanics', 4, 4, 5, 5),
('CV402', 'Surveying', 4, 3, 5, 5),
('CV403', 'Building Materials', 4, 3, 5, 5),
('CV404', 'Hydraulics', 4, 4, 5, 5),
('CV405', 'Transportation Engg', 4, 3, 5, 5);

-- IT Subjects (6th Sem)
INSERT INTO subject (subject_code, subject_name, semester, credits, dept_id, faculty_id) VALUES
('IT601', 'Web Technologies', 6, 4, 6, 6),
('IT602', 'Cloud Computing', 6, 3, 6, 6),
('IT603', 'AI and ML', 6, 4, 6, 6),
('IT604', 'Cyber Security', 6, 3, 6, 6),
('IT605', 'Data Analytics', 6, 4, 6, 6);

-- ===============================
-- HOSTEL
-- ===============================
CREATE TABLE hostel (
    hostel_id INT AUTO_INCREMENT PRIMARY KEY,
    hostel_name VARCHAR(50),
    total_rooms INT
);

INSERT INTO hostel (hostel_name, total_rooms) VALUES
('IT', 100), ('NB', 120), ('NBX', 80), ('MM', 90), ('IH', 100), ('MESS', 150);

-- ===============================
-- STUDENT
-- ===============================
CREATE TABLE student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    srn VARCHAR(20) UNIQUE,
    student_name VARCHAR(100),
    gender VARCHAR(10),
    dob DATE,
    dept_id INT,
    semester INT,
    year_of_study INT,
    hostel_id INT,
    scholarship_award VARCHAR(50),
    cgpa DECIMAL(4,2),
    lpa DECIMAL(5,2),
    placement_company VARCHAR(100),
    red_marks INT,
    permanent_address TEXT,
    present_address TEXT,
    father_name VARCHAR(100),
    mother_name VARCHAR(100),
    parent_contact VARCHAR(15),
    FOREIGN KEY (dept_id) REFERENCES department(dept_id),
    FOREIGN KEY (hostel_id) REFERENCES hostel(hostel_id)
);

-- 10 Students
INSERT INTO student (srn, student_name, gender, dob, dept_id, semester, year_of_study, hostel_id, scholarship_award, cgpa, lpa, placement_company, red_marks, permanent_address, present_address, father_name, mother_name, parent_contact) VALUES
('PES1UG21CS001', 'Aarav Reddy', 'Male', '2003-04-12', 1, 3, 2, 1, 'MRD', 8.3, 0.0, NULL, 0, 'Hyderabad', 'Hostel IT', 'Suresh Reddy', 'Lakshmi Reddy', '9876541111'),
('PES1UG21CS002', 'Diya Menon', 'Female', '2003-06-15', 1, 3, 2, 2, 'None', 7.9, 0.0, NULL, 0, 'Bangalore', 'Hostel NB', 'Ravi Menon', 'Anitha Menon', '9876541112'),
('PES1UG21EC003', 'Rohan Patil', 'Male', '2002-09-09', 2, 3, 3, 3, 'CNR', 8.1, 0.0, NULL, 1, 'Pune', 'NBX', 'Sanjay Patil', 'Meena Patil', '9876541113'),
('PES1UG21EC004', 'Ananya Sharma', 'Female', '2003-02-18', 2, 3, 2, NULL, 'None', 8.9, 0.0, NULL, 0, 'Delhi', 'PG', 'Mahesh Sharma', 'Kavitha Sharma', '9876541114'),
('PES1UG21EE005', 'Karthik Nair', 'Male', '2002-12-01', 3, 5, 3, 5, 'DAC', 8.5, 7.5, 'TCS', 0, 'Kochi', 'IH', 'Sreenivasan Nair', 'Revathi Nair', '9876541115'),
('PES1UG21ME006', 'Sanya Rao', 'Female', '2002-07-10', 4, 2, 1, 4, 'None', 7.4, 0.0, NULL, 0, 'Mysuru', 'MM', 'Raghav Rao', 'Priya Rao', '9876541116'),
('PES1UG21CV007', 'Aditya Singh', 'Male', '2001-11-21', 5, 4, 3, NULL, 'MRD', 8.7, 0.0, NULL, 2, 'Jaipur', 'Flat', 'Vivek Singh', 'Sunita Singh', '9876541117'),
('PES1UG21IT008', 'Megha Iyer', 'Female', '2003-03-14', 6, 6, 4, 2, 'CNR', 9.2, 12.0, 'Google', 0, 'Chennai', 'NB', 'Narayan Iyer', 'Radhika Iyer', '9876541118'),
('PES1UG21IT009', 'Rahul Das', 'Male', '2003-08-05', 6, 6, 4, NULL, 'None', 8.8, 10.5, 'Amazon', 0, 'Kolkata', 'PG', 'Subhash Das', 'Mina Das', '9876541119'),
('PES1UG21CS010', 'Tanya Bose', 'Female', '2003-01-22', 1, 3, 2, 2, 'MRD', 8.6, 0.0, NULL, 1, 'Kolkata', 'NB', 'Arun Bose', 'Nisha Bose', '9876541120');

-- ===============================
-- PLACEMENT COMPANY
-- ===============================
CREATE TABLE placement_company (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100),
    domain VARCHAR(100)
);

INSERT INTO placement_company (company_name, domain) VALUES
('TCS', 'Software Services'),
('Infosys', 'Software Services'),
('Google', 'Technology'),
('Amazon', 'E-commerce'),
('Wipro', 'IT Services');

-- ===============================
-- PLACEMENT OFFER
-- ===============================
CREATE TABLE placement_offer (
    offer_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    company_id INT,
    package_lpa DECIMAL(5,2),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (company_id) REFERENCES placement_company(company_id)
);

INSERT INTO placement_offer (student_id, company_id, package_lpa) VALUES
(5, 1, 7.5),
(8, 3, 12.0),
(9, 4, 10.5);

-- ===============================
-- FEE PAYMENT
-- ===============================
CREATE TABLE fee_payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    amount_paid DECIMAL(10,2),
    payment_date DATE,
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

-- ===============================
-- LIBRARY
-- ===============================
CREATE TABLE library_book (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE library_borrow (
    borrow_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    book_id INT,
    borrow_date DATE,
    return_date DATE,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (book_id) REFERENCES library_book(book_id)
);

SET FOREIGN_KEY_CHECKS = 1;

-- ===============================
-- ✅ FINAL CHECK
-- ===============================
SELECT COUNT(*) AS total_students FROM student;
