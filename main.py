# 실행예시
# 가 - A, D, G
# 나 - B, E, H
# 다 - C, F,  I, J


# A - 1. Print all universities
# A - 2. Print all students
# B - 3. Insert a new university
# B - 4. Remove a university
# C - 5. Insert a new student
# C - 6. Remove a student
# D - 7. Make a application
# E - 8. Print all students who applied for a university
# F - 9. Print all universities a students applied for
# G - 10. Print expected successful applicants of a university
# H - 11. Print universities expected to accept a student
# I - 12. Exit
# J - 13. Reset database



# (1/30) Term Project
# Due Date: 2019/02/15(Fri) 11:59PM
# 제출: lecture@europa.snu.ac.kr
# 파일명: PRJ_조이름.zip (예: PRJ_12조.zip)
# 메일 제목: [DB Project] 조이름 – 조원 이름1, 조원 이름2, 조원 이름3 (예: [DB Project] 12조 – 홍길동, 김철수, 김영희)
# 제출 내용 (압축하여 zip으로 제출)
# 1. Runnable python script 파일 (파일명: main.py)
# 2. DB 관련 정보
# 2-1. DB 테이블 스키마 (CREATE 문)
# 2-2. DB 접속 정보 (main.py에 잘 적어서 제출해 주세요.)
# 반드시 truncate한 후 제출해주세요!
# 3. 리포트 (pdf 포맷으로 제출해주세요!)
# 파일명: PRJ_조이름.pdf (예: PRJ_12조.pdf)



# A - 1. Print all universities
# A - 2. Print all students
# B - 3. Insert a new university
# B - 4. Remove a university
# C - 5. Insert a new student
# C - 6. Remove a student
# D - 7. Make a application
# E - 8. Print all students who applied for a university
# F - 9. Print all universities a students applied for
# G - 10. Print expected successful applicants of a university
# H - 11. Print universities expected to accept a student
# I - 12. Exit
# J - 13. Reset database


import pymysql
import pymysql.cursors    

ddlscripts = '''
use project;|
drop table if exists Apply cascade;|
drop table if exists Schools cascade;|
drop table if exists Students cascade;|
DROP PROCEDURE IF EXISTS check_school;|
DROP PROCEDURE IF EXISTS check_student;|

CREATE TABLE `Schools` (
  `school_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `school_name` varchar(200) NOT NULL,
  `capacity` int(11) NOT NULL,
  `school_district` char(2) NOT NULL,
  `min_score` int(10) unsigned NOT NULL,
  `adjust_ratio` float unsigned NOT NULL,
  PRIMARY KEY (`school_id`)
) ENGINE=InnoDB AUTO_INCREMENT=166 DEFAULT CHARSET=utf8;|

CREATE TABLE `Students` (
  `student_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `student_name` varchar(200) NOT NULL,
  `test_score` int(10) unsigned NOT NULL,
  `school_grades` int(10) unsigned NOT NULL,
  PRIMARY KEY (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6095 DEFAULT CHARSET=utf8;|

CREATE TABLE `Apply` (
  `student_id` int(10) unsigned NOT NULL,
  `school_id` int(10) unsigned NOT NULL,
  `school_district` char(2) DEFAULT NULL,
  PRIMARY KEY (`student_id`,`school_id`),
  UNIQUE KEY `uk_student_id_school_district` (`student_id`,`school_district`),  
  CONSTRAINT `fk_apply_school` FOREIGN KEY (`school_id`) REFERENCES `Schools` (`school_id`),
  CONSTRAINT `fk_apply_student` FOREIGN KEY (`student_id`) REFERENCES `Students` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;|


ALTER TABLE Schools AUTO_INCREMENT=1;|

ALTER TABLE Students AUTO_INCREMENT=1;|


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
end|

CREATE TRIGGER `check_school_before_insert` BEFORE INSERT ON `Schools`
FOR EACH ROW
    BEGIN
        CALL check_school(new.school_name,new.capacity,new.school_district,new.min_score,new.adjust_ratio);
END|


CREATE TRIGGER `check_school_before_update` BEFORE UPDATE ON `Schools`
FOR EACH ROW
    BEGIN
        CALL check_school(new.school_name,new.capacity,new.school_district,new.min_score,new.adjust_ratio);
END|


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
end|

CREATE TRIGGER `check_student_before_insert` BEFORE INSERT ON `Students`
FOR EACH ROW
    BEGIN
        CALL check_student(new.student_name,new.test_score,new.school_grades);
END|

CREATE TRIGGER `check_student_before_update` BEFORE UPDATE ON `Students`
FOR EACH ROW
    BEGIN
        CALL check_student(new.student_name,new.test_score,new.school_grades);
END
'''




#string format
scholls_head ='''
----------------------------------------------------------------------
id\tname\t\tcapacity\tgroup\tcutline\tweight\tappled
----------------------------------------------------------------------'''

students_head ='''
----------------------------------------------------------------------
id\tname\t\tcsat_score\tscholl_score
----------------------------------------------------------------------'''

tail='''
----------------------------------------------------------------------'''

menu_list ='''
======================================================================
1. print all universities
2. print all students
3. insert a new university
4. remove a university
5. insert a new student
6. remove a student
7. make an application
8. print all students who applied for a university
9. print all universities a student applied for
10. print expected successful applicants of a university
11. print universities expected to accept a student
12. exit
13. reset database
======================================================================'''


# connection information 분리, 테스트를 위한 정보와, 실제 project 정보 dictionary 형태로 분리
connection_info_list ={
    'test':{
        'host':'localhost',
        'user':'root',
        'password':'1q2w3e4r5t!',
        'db': 'project'
    },
    'project':{
        'host' : 'ds1.snu.ac.kr',
        'user' : 'ds3_4',
        'password' : '1q2w3e4r5t',
        'db': 'ds3_4_project'

    }
}
con_info = None


#db connection method
def querytodatabase(sql,querytype=0, *args):
    '''
    sql : sqlstatement, 
    querytype : 0 => select clause, 1 => ddl clause,
    args : optional arguments for sql statement
    '''
    
    connection = pymysql.connect(
        host = con_info['host'],
        user = con_info['user'],
        password = con_info['password'],
        db = con_info['db'],
        charset = 'utf8',
        cursorclass = pymysql.cursors.DictCursor
    )
    result = None
    try:  
        with connection.cursor() as cursor:            
            cursor.execute(sql,args)
            #query 목적
            if querytype == 0:
                result = cursor.fetchall()  

            #ddl 실행시(insert/remove 등)
            else:
                connection.commit()
                result = cursor.rowcount
    except Exception as e:
        raise Exception
    
    finally:
        connection.close()
    return result



def inputwithpredicate(comment,dtype,predfunc=None,custom_errmsg=''):
    typechecker = {
        0 : {'type' : [int,float],'errmsg' : 'Please enter integer/float value'},        
        1 : {'type' : [str], 'errmsg' : 'Please enter string value'}
    }
    p = True
    #입력란에 대해 정상적으로 입력받기전까지 입력창 유지
    while p:
        try:
            #숫자/정수형 입력란이면 eval 함수로 정확한 type 으로 type casting
            res = eval(input(comment)) if dtype == 0 else input(comment)            
            if type(res) in typechecker[dtype]['type'] :   

                #db constraint 와 별도로 사용자가 입력시 실시간으로 피드백 주기 위한 입력 제약조건 함수실행
                if predfunc==None:         
                    return res            
                else:
                    if predfunc(res):
                        return res
                    else:
                        print(custom_errmsg)
            #입력받은 타입이 오류가 있을 시 타입관련 에러메시지
            else:
                print(typechecker[dtype]['errmsg'])    
        except:
            print(typechecker[dtype]['errmsg'])


         

# A - 1. Print all universities
#querytodatabase('SELECT * FROM ds3_4_project.Students where student_name like %s and test_score > %s',0,('A%',30))
#querytodatabase(query문,0,(튜플로 조건))
def printalluniversities():
    print(scholls_head)
    sql = '''select school_id, school_name, capacity,school_district,min_score,adjust_ratio,count(Apply.student_id) as appled
                        from Schools Natural left outer join Apply
                        group by school_id''' 
    result = querytodatabase(sql,0)  
    for row in result:
        print(str(row['school_id']) + '\t'+row['school_name'] + '\t'+str(row['capacity']) + '\t\t'+row['school_district'] + '\t'+str(row['min_score']) + '\t'+str(row['adjust_ratio']) + '\t'+ str(row['appled']) )
    print(tail)

# A - 2. Print all students
def printallstudents():
    print(students_head)   
    sql = 'select * from Students'
    result = querytodatabase(sql,0)      
    for row in result:
        print(str(row['student_id']) + '\t'+row['student_name'] + '\t\t'+str(row['test_score']) + '\t\t'+str(row['school_grades'])) 
    print(tail)

# B - 3. Insert a new university    
def insertanewuniversity():    
    try:
        #get values from user()
        #db table 에 trigger & stored procedure 로 제약조건 설정하였으나,실제 입력받을 때 실시간으로 피드배 받아 정상적으로 입력받게 유도
        temp=[]
        temp.append(inputwithpredicate('University name: ',1))
        temp.append(inputwithpredicate('University capacity: ',0,lambda x : x>0,'Please enter a value over 0'))
        temp.append(inputwithpredicate('University group: ',1,lambda x : x.upper() in ('A','B','C'),'Please enter a value between A and C'))
        temp.append(inputwithpredicate('Cutline score: ',0,lambda x:x>0,'Please enter a value over 0'))
        temp.append(inputwithpredicate('Weight of high school records: ',0,lambda x : x>0,'Please enter a value over 0'))
        #execute query with data from user
        was_inserted = querytodatabase('insert into Schools(school_name,capacity,school_district,min_score,adjust_ratio) values(%s,%s,%s,%s,%s)',1,*temp)
        if was_inserted:            
            print('A university is successfully inserted.')
        else:
            print('No data inserted')
        
    except pymysql.err.InternalError:
        print('your value is wrong. retry')        

# B - 4. Remove a university
def removeauniversity():    
    try:
        temp=''
        temp=inputwithpredicate('school_id: ',0)
        was_deleted = querytodatabase('delete from Schools where school_id = %s',1,temp)
        if was_deleted:          
            print('A university is successfully deleted.')    
        else:
            print('There is no university matching with id you entered')
        
    except pymysql.err.InternalError:
        print('your value is wrong. retry')

# C - 5. Insert a new student   
def insertanewstudent():
    try:
        #사용자로부터 정보 받기
        #db table 에 trigger & stored procedure 로 제약조건 설정하였으나,실제 입력받을 때 실시간으로 피드배 받아 정상적으로 입력받게 유도
        temp=[]
        temp.append(inputwithpredicate('Student name: ',1))
        temp.append(inputwithpredicate('Test Score: ',0))
        temp.append(inputwithpredicate('School Grade: ',0))        

        #입력받은 정보 db에 입력
        was_inserted = querytodatabase('insert into Students(student_name,test_score,school_grades) values (%s,%s,%s);',1,*temp)
        if was_inserted :
            print('A Student is successfully inserted.')
        else :
            print('No data inserted')        
    except pymysql.err.InternalError:
        print('your value is wrong. retry')          
    

# C - 6. Remove a student
def removeastudent():
    try:
        student_id = inputwithpredicate('Student ID : ',0)
        was_deleted = querytodatabase('delete from Students where student_id = %s',1,*[student_id]) 
        if was_deleted:          
            print('A Student is successfully deleted.') 
        else:
            print('There is no student matching with id you entered')
    except pymysql.err.InternalError:
        print('your value is wrong. retry')          


# D - 7. Make a application
def makeaapplication():      
    try:
        temp=[]
        temp.append(inputwithpredicate('Student ID : ',0))
        temp.append(inputwithpredicate('School ID : ',0))
        was_inserted = querytodatabase('insert into Apply select %s,school_id,school_district from Schools where school_id=%s  ',1,*temp)
        if was_inserted:
            print('Successfully made an application')
        else:
            print('No data inserted because of either of no student_id or no school_id')
    except pymysql.err.IntegrityError:
        print('You already aplly same school_district.')
    except Exception as e:
        print(str(e))

#E - 8. Print all students who applied for a university
def printallstudentsappliedforauniversity():    
    temp=''
    temp=input('school_id: ')
    result = querytodatabase('select student_id, student_name, test_score,school_grades from Schools natural join Apply natural join Students where school_id =%s',0,temp)
    if result:
        print(students_head)   
        for row in result:
            print(str(row['student_id']) + '\t'+row['student_name'] + '\t\t'+str(row['test_score']) + '\t\t'+str(row['school_grades'])) 
        print(tail)                
    else:
        print('your value is wrong.')

#F - 9. Print all universities a students applied for
def printalluniversitiesastudentsappliedfor():    
    temp=[]
    temp.append(input('student_id: '))
    result = querytodatabase('select school_id, school_name, capacity,  school_district, min_score, adjust_ratio,count(Apply.student_id) as appled from Students  natural join Apply natural join Schools where student_id = %s group by school_id ',0,*temp)
    if result:
        print(scholls_head)
        for row in result:
            print(str(row['school_id']) + '\t'+row['school_name'] + '\t'+str(row['capacity']) + '\t\t'+row['school_district'] + '\t'+str(row['min_score']) + '\t'+str(row['adjust_ratio']) + '\t'+ str(row['appled']) )
        print(tail)
    else:
        print('your value is wrong.')


def getpassstudentlist(temp):       
    x = '(select school_id, school_name, student_id, student_name, test_score, capacity,  min_score,school_grades, (test_score+school_grades*adjust_ratio) as total_score from Students  natural join Apply natural join Schools where school_id = %s) as x'
    y = 'select school_id, school_name, student_id, student_name, capacity,test_score, min_score, total_score,school_grades  from '+x+' where total_score>=min_score order by total_score desc,school_grades desc'
    t = 'select count(student_id) as t from (' + y + ') as y group by total_score,school_grades order by total_score desc,school_grades desc ' 
    z = 'select count(student_id) as count_s from (' + y + ') as y group by school_id' 
    result = querytodatabase(y,0,*temp)
    count= querytodatabase(z,0,*temp)
    t1= querytodatabase(t,0,*temp)
    if result:
        test=[]
        for x in t1:
            test.append(x['t'])

        if result[0]['capacity']>=count[0]['count_s']:
            temp=[]
            for i in result:
                temp.append((i['student_id'],i['student_name'],i['school_grades'],i['test_score']))
            return temp
        else:  
            sum=0
            temp=[]
            for i in test:
                for j in range(i):                    
                    if sum<=result[0]['capacity']*1.1:  
                        temp.append((result[j]['student_id'],result[j]['student_name'],result[j]['school_grades'],result[j]['test_score']))
                        sum += test[j]
                    else:
                        break
            return temp

            


#G - 10. Print expected successful applicants of a university
def printexpectedsuccessfulapplicantsofauniversity(): 
    temp=[]
    temp.append(input('school_id: '))   
    result=getpassstudentlist(temp)

    print(students_head)   
    for row in sorted(list(set(result))):
        print(str(row[0]) + '\t'+row[1] + '\t\t'+str(row[2]) + '\t\t'+str(row[3])) 
    print(tail) 

#H - 11. Print universities expected to accept a student
def printuniversitiesexpectedtoacceptastudent():
    x = 'select school_id from Students  natural join Apply natural join Schools where student_id = %s'
    y = 'select student_id,student_name,school_grades,test_score from Students  where student_id = %s'
    z = 'select school_id, school_name, capacity,  school_district, min_score, adjust_ratio,count(Apply.student_id) as appled from Schools  natural join Apply where school_id = %s group by school_id '
    temp=[]
    temp.append(input('student_id: ')) 
    result = querytodatabase(x,0,*temp)
    result2 = querytodatabase(y,0,*temp)
    
    student = (result2[0]['student_id'],result2[0]['student_name'],result2[0]['school_grades'],result2[0]['test_score'])
    # print(student)

    schools=[]
    schools_list=[]
    for i in result:
        schools.append(i['school_id'])
    # print (schools)
    for j in schools:
        schools_list.append(getpassstudentlist([j]))
    # print(schools_list)
    for k in range(len(schools_list)):
        if student in schools_list[k]:
            print(querytodatabase(z,0,schools[k]))

#J - 13. Reset database
def resetdatabase():   
    try:
        print('Start to reset database.')
        querylist = ddlscripts.replace('\n','').split('|')
        for q in querylist:
            print(q)
            querytodatabase(q,1)
        print('''
Done to reset database. Executed commands below. 
1. Drop tables : Apply -> Schools & Students
2. Drop Procedure of Students & Schools for input constraint
3. Create tables : Students & Schools -> Apply
4. Reset Autoincrement columns : Students & Schools
3. Create Procedure and Trigger of Students & Schools for input constraint
Please enter new data.''')    
    except Exception:
        print('Error occured while trying to reset database.')

#14 Test목적 dataset
def dumptestdateset():
    import sys
    import os
    try:
        filepathlist = {
            'Students': ['students_list.csv','insert into Students(student_id,student_name,test_score,school_grades) values (%s,%s,%s,%s)'],
            'Schools' : ['university_list.csv','insert into Schools(school_name,capacity,school_district,min_score,adjust_ratio) values (%s,%s,%s,%s,%s)']
        }

        for tablename in filepathlist:
            filepath = filepathlist[tablename][0]
            sql = filepathlist[tablename][1]
            filefullpath = os.path.join(os.getcwd() ,filepath)
            with open(filefullpath,'r') as f:
                header = f.readline()
                rows = f.readlines()
                for r in rows:
                    params = list(map(lambda x : x.strip(), r.replace('\n','').split(',')))
                    querytodatabase(sql,1,*params)   
            print('Done to dump %s table.'%(tablename))

        import random
        random.seed(0)
        schooldistrictrange = [(1,45),(62,126),(132,180)]
        for studentid in range(1,201):                                    
            templist = list(map(lambda rng : (studentid, random.randint(rng[0],rng[1])),schooldistrictrange))
            for temp in templist:
                querytodatabase('insert into Apply select %s,school_id,school_district from Schools where school_id=%s  ',1,*temp)
        print('Done to dump %s table.'%('Apply'))

    except:
        print('occur error as insert dataset')



menu_num = 0
menu_selection={
    1:printalluniversities,
    2:printallstudents,
    3:insertanewuniversity,
    4:removeauniversity,
    5:insertanewstudent,
    6:removeastudent,
    7:makeaapplication,
    8:printallstudentsappliedforauniversity,
    9:printalluniversitiesastudentsappliedfor,
    10:printexpectedsuccessfulapplicantsofauniversity,
    11:printuniversitiesexpectedtoacceptastudent,    
    13:resetdatabase,
    14:dumptestdateset
}



def main():
    while True:
        print(menu_list)
        menu_num = eval(input('Select your action : '))        
        if menu_num in menu_selection.keys():
            menu_selection[menu_num]()
        elif menu_num == 12:
            print('Bye!')
            break
        else:
            print('잘못된 번호 입력하였습니다')

if __name__ == '__main__':
    con_info = connection_info_list['test']
    main()        

