import mysql.connector

class DB:
    def __init__(self):
        self.conn = mysql.connector.connect(user='machimori',password='yatsushironct',host='127.0.0.1',database='machimori',port=3306)

    def select(self,sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close
        return data

    def insert_data(self,sql,data):
        cur = self.conn.cursor()
        cur.execute(sql,data)
        cur.close
        self.conn.commit()

    def end_DB(self):
        self.conn.close


if __name__ == "__main__":
    db = DB()
    data = db.select('select * from occur;')
    for i in data:
        print(i)
    db.end_DB()
    
