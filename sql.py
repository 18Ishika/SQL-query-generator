import sqlite3
#connect to sqlite3 
#streamlit is used for building interactive frontend
connection=sqlite3.connect("student.db")
#creating a cursor object for db
cur=connection.cursor()
table_info="""
Create table STUDENT(
Name VARCHAR(30), Class VARCHAR(25),
Section VARCHAR(25),Marks INT
);
"""
cur.execute(table_info)
cur.execute('''Insert into STUDENT values('Ishika','Data Science','A',93);''')
cur.execute('''Insert into STUDENT values('Vishakha Routra','Data Science','B',93);''')
cur.execute('''Insert into STUDENT values('Nischay','Devops','B',83);''')
cur.execute('''Insert into STUDENT values('Abhishek','Augmented Reality','C',73);''')
cur.execute('''Insert into STUDENT values('Kaushal','Cyber Security','B',53);''')
cur.execute('''Insert into STUDENT values('Bhoomi Patenkar','Robotics','C',69);''')
cur.execute('''Insert into STUDENT values('Payal','Devops','A',23);''')
cur.execute('''Insert into STUDENT values('Yash','AI','C',88);''')
cur.execute('''Insert into STUDENT values('Om','Data Science','A',89);''')
cur.execute('''Insert into STUDENT values('Anushka Gupta','Augmented Reality','B',77);''')
cur.execute('''Insert into STUDENT values('Ayush','DSA','C',53);''')
cur.execute('''Insert into STUDENT values('Ishan Thakur','Data Science','B',66);''')
cur.execute('''Insert into STUDENT values('Gauri','Devops','C',85);''')
cur.execute('''Insert into STUDENT values('Jai','Augmented Reality','A',33);''')
cur.execute('''Insert into STUDENT values('Sridevi','Cyber Security','C',63);''')
cur.execute('''Insert into STUDENT values('Nidhi','Cyber Security','B',89);''')
cur.execute('''Insert into STUDENT values('Unnatti Sharma','Devops','C',38);''')
cur.execute('''Insert into STUDENT values('Yashi','Devops','B',48);''')
cur.execute('''Insert into STUDENT values('Marie','DSA','B',66);''')
cur.execute('''Insert into STUDENT values('Abhay Verma','Augmented Reality','A',87);''')


#printing all the records in the db
print("all the records in the database are")
data=cur.execute('''select * from STUDENT;''')
for i in data:
    print(i)
connection.commit()
connection.close()