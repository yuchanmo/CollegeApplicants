use ds3_4_project;

drop table if exists Schools cascade;
drop table if exists Students cascade;
drop table if exists Apply cascade;
create table Schools
(
school_id int unsigned primary key auto_increment,
school_name nvarchar(200) not null,
capacity int not null,
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