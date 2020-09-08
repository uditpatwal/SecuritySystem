import sqlite3

class Database:

    def __init__(self):
        self.con = sqlite3.connection()
        c = con.cursor()

        create_table_statement = """CREATE TABLE duration_face_detected (VARCHAR name, VARCHAR time, INT duration);"""
        c.execute(create_table_statement)
        con.commit()
        c.close()


    def addPersonWithTime(self, name, time, duration):
        c = self.con.cursor()
        insert_statement = """INSERT INTO duration_face_detected(name, time, duration) 
                            values(?,?,?);""" 
        data_tuple = (name, time, duration)

        c.execute(insert_statement, data_tuple)
        
        con.commit()
        c.close()







