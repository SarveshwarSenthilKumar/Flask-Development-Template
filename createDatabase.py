import sqlite3
import os

database = open('users.db', 'w')
database.truncate(0)  
database.close()
connection = sqlite3.connect("users.db")
crsr = connection.cursor()
crsr.execute("CREATE TABLE users (id INTEGER, username NOT NULL, password NOT NULL, emailaddress, name, money, dateJoined, friends, setpoint, watching, PRIMARY KEY(id))")
connection.commit()
crsr.close()
connection.close()

