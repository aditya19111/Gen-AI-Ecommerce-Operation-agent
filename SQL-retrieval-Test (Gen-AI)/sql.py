import sqlite3

# crerating connection
connection = sqlite3.connect("student.db")

#creating cursor to create amd make changes to the dataset
cursor = connection.cursor()

#create table
table_info = """
CREATE TABLE STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT);
"""

cursor.execute(table_info)

##inserting new records

cursor.execute('''INSERT INTO STUDENT values('Aditya', 'computer science', 'A', 90)''')
cursor.execute('''INSERT INTO STUDENT values('Sai', 'computer science', 'A', 65)''')
cursor.execute('''INSERT INTO STUDENT values('Chris', 'computer science', 'A', 80)''')
cursor.execute('''INSERT INTO STUDENT values('Adelene', 'Data science', 'B', 90)''')

#DISPLAY ALL THE RECORDS

print("The inserted records are ")

data = cursor.execute('''SELECT * FROM STUDENT''')

for row in data:
    print(row)

#commit changes and close the connection
connection.commit()
connection.close()