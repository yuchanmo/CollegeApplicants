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

def main():
    while True:
        menu_num = eval(input('메뉴 번호를 입력하세요'))        
        if menu_num in menu_selection.keys():
            menu_selection[menu_num]()
        elif menu_num == 12:
            break
        else:
            print('잘못된 번호 입력하였습니다')


            
        

def querytodatabase(sql,querytype, *args):
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
            if querytype == 'query':
                result = cursor.fetchall()                
            #ddl 실행시(insert/remove 등)
            else:
                connection.commit()
    finally:
        connection.close()
    return result

# A - 1. Print all universities
def printalluniversities():
    pass
# A - 2. Print all students
def printallstudents():
    pass
# B - 3. Insert a new university    
def insertanewuniversity():
    pass
# B - 4. Remove a university
def removeauniversity():
    pass

# C - 5. Insert a new student   
def insertanewstudent():
    pass
# C - 6. Remove a student
def removeastudent():
    pass

# D - 7. Make a application
def makeaapplication():
    pass

#E - 8. Print all students who applied for a university
def printallstudentsappliedforauniversity():
    pass

#F - 9. Print all universities a students applied for
def printalluniversitiesastudentsappliedfor():
    pass

#G - 10. Print expected successful applicants of a university
def printexpectedsuccessfulapplicantsofauniversity():
    pass

#H - 11. Print universities expected to accept a student
def printuniversitiesexpectedtoacceptastudent():
    pass

#J - 13. Reset database
def resetdatabase():
    pass