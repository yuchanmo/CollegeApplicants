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

scholls_head ='''
----------------------------------------------------------------------
id      name        capacity        group   cutline     weight  appled
----------------------------------------------------------------------'''

students_head ='''
----------------------------------------------------------------------
id      name        csat_score      scholl_score
----------------------------------------------------------------------'''

tail='''
----------------------------------------------------------------------'''


def querytodatabase(sql,querytype=0, *args):
    import pymysql.cursors
    connection = pymysql.connect(
        host = 'ds1.snu.ac.kr',
        user = 'ds3_4',
        password = '1q2w3e4r5t!',
        db = 'ds3_4_project',
        charset = 'utf8',
        cursorclass = pymysql.cursors.DictCursor
    )
    result = None
    try:  
        with connection.cursor() as cursor:            
            cursor.execute(sql,args)
            #print 구문
            if querytype == 0:
                result = cursor.fetchall()  

            #ddl 실행시(insert/remove 등)
            else:
                res = connection.commit()
    finally:
        connection.close()
    return result

# A - 1. Print all universities
def printalluniversities():
    print(scholls_head)
    print(querytodatabase('select * from Students limit 10 where student_name like %s',0,'A%'))
    print(tail)

# A - 2. Print all students
def printallstudents():
    print(students_head)
    print(querytodatabase('select * from Students limit 10 where student_name like %s',0,'A%'))
    print(tail)

# B - 3. Insert a new university    
def insertanewuniversity():
    print('3')
    import pymysql
    p = True
    while p:
        try:
            temp=[]
            temp.append(input('University name: '))
            temp.append(input('University capacity: '))
            temp.append(input('University group: '))
            temp.append(input('Cutline score: '))
            temp.append(input('Weight of high school records: '))
            querytodatabase('insert into Schools(school_name,capacity,school_district,min_score,adjust_ratio) values(%s,%s,%s,%s,%s)',1,*temp)
            print('A university is successfully inserted.')
            p = False
        except pymysql.err.InternalError:
            print('your value is wrong. retry')
        

    print('2')
# B - 4. Remove a university
def removeauniversity():
    print('4')
    import pymysql
    p = True
    while p:
        try:
            temp=''
            temp=input('school_id: ')
            querytodatabase('delete from Schools where school_id = %s',1,temp)
            print('A university is successfully deleted.')
            p = False
        except pymysql.err.InternalError:
            print('your value is wrong. retry')

# C - 5. Insert a new student   
def insertanewstudent():    
    print('5')
# C - 6. Remove a student
def removeastudent():
    print('6')

# D - 7. Make a application
def makeaapplication():
    print('7')
    import pymysql
    temp=[]
    temp.append(input('student_id: '))
    temp.append(input('school_id: '))
    try:
        querytodatabase('insert into Apply select %s,school_id,school_district from Schools where school_id=%s  ',1,*temp)
        print('Successfully made an application')
    except pymysql.err.IntegrityError:
        print('You already aplly same school_district.')

#E - 8. Print all students who applied for a university
def printallstudentsappliedforauniversity():
    print('8')
    import pymysql
    temp=''
    temp=input('school_id: ')
    result = querytodatabase('select student_id, student_name, test_score,school_grades from Schools natural join Apply natural join Students where school_id =%s',0,temp)
    if result:
        print(result)
    else:
        print('your value is wrong.')

    

#F - 9. Print all universities a students applied for
def printalluniversitiesastudentsappliedfor():
    print('9')
    
    temp=[]
    temp.append(input('student_id: '))
    result = querytodatabase('select school_id, school_name, capacity,  school_district, min_score, adjust_ratio from Students  natural join Apply natural join Schools where student_id = %s',0,*temp)
    if result:
        print(result)
    else:
        print('your value is wrong.')

#G - 10. Print expected successful applicants of a university
def printexpectedsuccessfulapplicantsofauniversity():
    print('10')
    import pandas as pd
    
    temp=[]
    temp.append(input('school_id: '))
    result = querytodatabase('select school_id, school_name, student_id, student_name, capacity, round(capacity*1.1,0) as add_capa, min_score, (test_score+school_grades*adjust_ratio) as total_score from Students  natural join Apply natural join Schools where school_id = %s',0,*temp)
    if result:
            print(result)
    else:
        print('Your value is wrong.')

#H - 11. Print universities expected to accept a student
def printuniversitiesexpectedtoacceptastudent():
    pass

#J - 13. Reset database
def resetdatabase():
    pass

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
    13:resetdatabase
}

menu_list ='''
============================================================
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
============================================================'''


def main():
    while True:
        print(menu_list)
        menu_num = eval(input('Select your action : '))        
        if menu_num in menu_selection.keys():
            menu_selection[menu_num]()
        elif menu_num == 12:
            break
        else:
            print('잘못된 번호 입력하였습니다')

main()        
        
