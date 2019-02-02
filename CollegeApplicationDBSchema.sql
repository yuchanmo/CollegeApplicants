use ds3_4_project;
drop table if exists Schools cascade;
drop table if exists Students cascade;
drop table if exists Apply cascade;
create table Schools
(
school_id int unsigned primary key auto_increment,
school_name nvarchar(200) not null,
capacity int unsigned not null,
school_district char(2) not null,
min_score int unsigned not null,
adjust_ratio float unsigned not null,
constraint capacity_ck check (capacity > 1),
constraint school_district_ck check (school_district in ('A','B','C')),
constraint min_score_ck check (min_score >=0)
);

create table Students
(
	student_id int unsigned  primary key auto_increment,
    student_name nvarchar(200) not null,
    test_score int unsigned not null,
    school_grades int unsigned not null,
    constraint test_score_ck check (test_score between 0 and 400),
    constraint school_grades_ck check (school_grades_ck between 0 and 100)    
);

create table Apply
(
	student_id int unsigned not null,
    school_id int unsigned not null,        
    constraint pk_apply primary key(student_id,school_id),
	constraint fk_apply_student foreign key(student_id) references Students(student_id),
    constraint fk_apply_school foreign key(school_id) references Schools(school_id)
);


--참고 : http://www.mysqltutorial.org/mysql-check-constraint/

-- school 제약조건
-- 1. 학교 
-- 학교 ID: 정수 (Primary key) 
-- 이름: 문자열 (최대 200 자)  
-- 정원: 정수 (1 이상의 값) 
-- 군: 문자열 (대문자 ‘A’, ‘B’, ‘C’ 중 1 개의 값을 가져야 함) 
-- 최소 점수: 정수 (0 이상의 값) 
-- 내신 성적 반영 비율: 실수 (0 이상의 값) 
DELIMITER $$
create procedure check_school
(in pname nvarchar(200),
 in pcapacity int,
 in pdistrict char(2),
 in pminscore int,
 in padjustratio float
)
begin
    if pcapacity < 1 then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Please enter value over 0 for Capacity';
    end if;

    if pdistrict not in ('A','B','C') then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Please enter only A or B or C for school district';
    end if;
end$$

DELIMITER ;

-- before insert
DELIMITER $$
CREATE TRIGGER `check_school_before_insert` BEFORE INSERT ON `Schools`
FOR EACH ROW
BEGIN
    CALL check_school(new.school_name,new.capacity,new.school_district,new.min_score,new.adjust_ratio);
END$$   
DELIMITER ; 


-- before update
DELIMITER $$
CREATE TRIGGER `check_school_before_update` BEFORE UPDATE ON `Schools`
FOR EACH ROW
BEGIN
    CALL check_school(new.school_name,new.capacity,new.school_district,new.min_score,new.adjust_ratio);
END$$   
DELIMITER ;

-- 학생 
-- 학생 ID: 정수 (Primary key) 
-- 이름: 문자열 (최대 200 자) 
-- 수능 성적: 정수 (0 이상 400 이하의 값) 
-- 내신 성적: 정수 (0 이상 100 이하의 값) 
use ds3_4_project;

DELIMITER $$
create procedure check_student
(
    in pname nvarchar(200),
    in ptestscore int,
    in pschoolgrade int 
)
begin
    if ptestscore < 0 or ptestscore > 400 then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Please enter value between 0 and 400 for TestScore';
    end if;

    if pschoolgrade < 0 or pschoolgrade > 100 then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Please enter value between 0 and 100 for SchoolGrade';
    end if;
end$$
DELIMITER ;

-- before insert
DELIMITER $$
CREATE TRIGGER `check_student_before_insert` BEFORE INSERT ON `Students`
FOR EACH ROW
BEGIN
    CALL check_student(new.student_name,new.test_score,new.school_grades);
END$$   
DELIMITER ; 


-- before update
DELIMITER $$
CREATE TRIGGER `check_student_before_update` BEFORE UPDATE ON `Students`
FOR EACH ROW
BEGIN
    CALL check_student(new.student_name,new.test_score,new.school_grades);
END$$   
DELIMITER ;