import pymysql.cursors

connection = pymysql.connect(
    host = 'ds1.snu.ac.kr',
    user = 'ds3_4',
    password = '1q2w3e4r5t!',
    db = 'ds3_4',
    charset = 'utf8',
    cursorclass = pymysql.cursors.DictCursor
)

try:  
    with connection.cursor() as cursor:
        sql = '''select name,year_emp
                from professor
                where year_emp < all(select year_emp from professor where name='최성희')'''
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
finally:
    connection.close()

