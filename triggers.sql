use UniversityDB;
CREATE TABLE student_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    srn VARCHAR(20),
    action VARCHAR(50),
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
DELIMITER //

CREATE TRIGGER after_student_insert
AFTER INSERT ON student
FOR EACH ROW
BEGIN
    INSERT INTO student_log (srn, action)
    VALUES (NEW.srn, 'New student added');
END //

DELIMITER ;
DELIMITER //

CREATE TRIGGER after_student_update
AFTER UPDATE ON student
FOR EACH ROW
BEGIN
    INSERT INTO student_log (srn, action)
    VALUES (NEW.srn, 'Student details updated');
END //

DELIMITER ;




