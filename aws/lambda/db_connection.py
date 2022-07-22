import pymysql
import os
import env

def connect_to_db():

    host = "seoultech-alarm-database.cpbrnv7glqr5.ap-northeast-2.rds.amazonaws.com"
    port = 3306
    user = "eunbin"
    database = 'seoultechNotice'
    password = "8633Hghg!"

    conn = pymysql.connect(host=host, user=user, passwd=password, db=database, port=port, use_unicode=True, charset='utf8')
    cursor = conn.cursor()

    return conn, cursor

print(env.DB_HOST)