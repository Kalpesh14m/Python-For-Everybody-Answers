"""

To get credit for this assignment, perform the instructions below and enter the code you get here:


(Hint: starts with 414)
Instructions
This application will read roster data in JSON format, parse the file, and then produce an SQLite database that contains a User, Course, and Member table and populate the tables from the data file.

You can base your solution on this code: http://www.py4e.com/code3/roster/roster.py - this code is incomplete as you need to modify the program to store the role column in the Member table to complete the assignment.

Each student gets their own file for the assignment. Download this file and save it as roster_data.json. Move the downloaded file into the same folder as your roster.py program.

Once you have made the necessary changes to the program and it has been run successfully reading the above JSON data, run the following SQL command:

SELECT hex(User.name || Course.title || Member.role ) AS X FROM
    User JOIN Member JOIN Course
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X
Find the first row in the resulting record set and enter the long string that looks like 53656C696E613333.
The first row in the resulting record set: ('414A736933333430',)
"""


import json
import sqlite3

#PART 1: Creating the database
dbname = "roster.sqlite"
conn = sqlite3.connect(dbname)
cur = conn.cursor()

cur.executescript('''
	DROP TABLE IF EXISTS User;
	DROP TABLE IF EXISTS Course;
	DROP TABLE IF EXISTS Member;
	CREATE TABLE User (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		name TEXT UNIQUE 
	);
	CREATE TABLE Course (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		title TEXT UNIQUE
	);
	CREATE TABLE Member (
		user_id INTEGER,
		course_id INTEGER,
		role INTEGER,
		PRIMARY KEY(user_id, course_id)
	)
''')
#Note: if we don't add UNIQUE after "User.name" and "Course.title", 
#the IGNORE statement won't work and therefore we'll have duplicates


#PART 2: DESERIALIZING THE data
#The JSON data we're going to process is stored in an array form, with each
#item being also an array of three elements: one corresponding to the username 
#one corresponding to the course name, and one indicating if the user is instructor
#None of them has any field title. 

filename = "roster_data.json"
jsondata = open(filename)
data = json.load(jsondata)

#PART 3: INSERTING DATA
for entry in data:
	user = entry[0]
	course = entry[1]
	instructor = entry[2]

	#Inserting user
	user_statement = """INSERT OR IGNORE INTO User(name) VALUES( ? )"""
	SQLparams = (user, )
	cur.execute(user_statement, SQLparams)

	#Inserting course
	course_statement = """INSERT OR IGNORE INTO Course(title) VALUES( ? )"""
	SQLparams = (course, )
	cur.execute(course_statement, SQLparams)

	#Getting user and course id
	courseID_statement = """SELECT id FROM Course WHERE title = ?"""
	SQLparams = (course, )
	cur.execute(courseID_statement, SQLparams)
	courseID = cur.fetchone()[0]

	userID_statement = """SELECT id FROM User WHERE name = ?"""
	SQLparams = (user, )
	cur.execute(userID_statement, SQLparams)
	userID = cur.fetchone()[0]

	#Inserting the entry
	member_statement = """INSERT INTO Member(user_id, course_id, role)
		VALUES(?, ?, ?)"""
	SQLparams = (userID, courseID, instructor)
	cur.execute(member_statement, SQLparams)

#Saving the changes
conn.commit()

#PART 4: Testing and obtaining the results
test_statement = """
SELECT hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X
"""
cur.execute(test_statement)
result = cur.fetchone()
print("The first row in the resulting record set: " + str(result))

#Closing the connection
cur.close()
conn.close()
