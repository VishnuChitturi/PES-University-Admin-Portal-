DROP DATABASE IF EXISTS UniversityDB2;
CREATE DATABASE UniversityDB2;
USE UniversityDB2;
SET FOREIGN_KEY_CHECKS=0;


-- Department Table

CREATE TABLE department (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_code VARCHAR(10) NOT NULL UNIQUE,
    dept_name VARCHAR(100) NOT NULL
);

--  Professor Table
CREATE TABLE professor (
    prof_id INT AUTO_INCREMENT PRIMARY KEY,
    prof_name VARCHAR(100) NOT NULL,
    designation VARCHAR(50),
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

--  Student Table
CREATE TABLE student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    srn VARCHAR(20) UNIQUE NOT NULL,
    student_name VARCHAR(100) NOT NULL,
    gender ENUM('Male','Female','Other'),
    dob DATE CHECK (dob BETWEEN '1999-01-01' AND '2010-12-31'),
    dept_id INT,
    year_of_study INT CHECK (year_of_study BETWEEN 1 AND 4),
    cgpa DECIMAL(3,2) CHECK (cgpa BETWEEN 0.00 AND 10.00),
    CHECK (srn REGEXP '^PES1UG[0-9]{2}(CS|AI|EC|EE|ME)[0-9]{3}$'),
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

--  Course Table
CREATE TABLE course (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) NOT NULL UNIQUE,
    course_name VARCHAR(150) NOT NULL,
    credits INT,
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

--  Enrollment Table
CREATE TABLE enrollment (
    enroll_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    semester VARCHAR(10),
    grade VARCHAR(2),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

--  Scholarship Table
CREATE TABLE scholarship (
    scholarship_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    scholarship_name VARCHAR(100),
    scholarship_award ENUM('MRD','CNR','DAC'),
    amount DECIMAL(10,2),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

--  Hostel Table
CREATE TABLE hostel (
    hostel_id INT AUTO_INCREMENT PRIMARY KEY,
    hostel_name VARCHAR(100),
    hostel_alloted ENUM('IT','NB','NBX','MM','IH','MESS'),
    total_rooms INT
);

CREATE TABLE hostel_allocation (
    allocation_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    hostel_id INT,
    room_no VARCHAR(10),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (hostel_id) REFERENCES hostel(hostel_id)
);

--  Fee Payment Table
CREATE TABLE fee_payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    amount_paid DECIMAL(10,2),
    payment_date DATE,
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

--  Library Tables
CREATE TABLE library_book (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150),
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

--  Placement Tables
CREATE TABLE placement_company (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100),
    domain VARCHAR(100)
);

CREATE TABLE placement_offer (
    offer_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    company_id INT,
    package_lpa DECIMAL(5,2),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (company_id) REFERENCES placement_company(company_id)
);

--  Clubs Tables
CREATE TABLE club (
    club_id INT AUTO_INCREMENT PRIMARY KEY,
    club_name VARCHAR(100),
    faculty_incharge INT,
    FOREIGN KEY (faculty_incharge) REFERENCES professor(prof_id)
);

CREATE TABLE club_member (
    club_member_id INT AUTO_INCREMENT PRIMARY KEY,
    club_id INT,
    student_id INT,
    role VARCHAR(50),
    FOREIGN KEY (club_id) REFERENCES club(club_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

SET FOREIGN_KEY_CHECKS=1;
