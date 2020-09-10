import sqlite3

class Database:

    def __init__(self):
        con = sqlite3.connect("database.db")
        c = con.cursor()

        create_table_statement = """CREATE TABLE duration_face_detected (name VARCHAR, time VARCHAR, duration INT);"""
        # c.execute(create_table_statement)
        con.commit()
        c.close()
        con.close()

    def addPersonTime(self, name, time, duration):
        con = sqlite3.connect("database.db")
        c = con.cursor()
        insert_statement = """INSERT INTO duration_face_detected(name, time, duration) 
                            values(?,?,?);""" 
        data_tuple = (name, time, duration)

        c.execute(insert_statement, data_tuple)
        
        con.commit()
        c.close()
        con.close()







