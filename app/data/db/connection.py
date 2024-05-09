import pymysql

def connect():
    return pymysql.connect(
            host='nextgame.ctu2qk4u26tp.us-east-1.rds.amazonaws.com',
            user='admin', password='A_946372466_s',db='NextGame',
            charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor
        )
