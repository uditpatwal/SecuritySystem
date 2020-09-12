import sqlite3

class Database:

    def __init__(self):
        con = sqlite3.connect("database.db")
        c = con.cursor()

        create_table_statement = """CREATE TABLE IF NOT EXISTS duration_face_detected (name VARCHAR, time VARCHAR, duration INT);"""
        create_doorUnlock_table = """CREATE TABLE IF NOT EXISTS doorUnlock(name VARCHAR, time VARCHAR, did_doorUnlock BOOLEAN);"""
        c.execute(create_table_statement)
        c.execute(create_doorUnlock_table)
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

    def addPersonToUnlock(self, name, time, didUnlock):
        con = sqlite3.connect("database.db")
        c = con.cursor()
        insert_statement = """INSERT INTO doorUnlock(name, time, did_doorUnlock) 
                                values(?, ?, ?)"""
        data_tuple = (name, time, didUnlock)

        c.execute(insert_statement, data_tuple)

        con.commit()
        c.close()
        con.close()






