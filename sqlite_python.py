import sqlite3

#Connecting to sqlite
conn = sqlite3.connect('db.sqlite3')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Doping EMPLOYEE table if already exists
cursor.execute("DROP TABLE analysis_mailingticker")
print("Table dropped... ")

#Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()