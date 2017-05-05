import sqlite3 as lite
import csv
import sys

# this file must be run once to create the database
con = lite.connect("UCBerkeley.db")

collegeFile = "College.csv"

majorFile = "Major.csv"

counselorFile = "Counselor.csv"

studentFile = "Student.csv"

appointmentFile = "Appointment.csv"

with con:
	cur = con.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS College (collegeID INT, collegeName VARCHAR(255));")
	cur.execute("CREATE TABLE IF NOT EXISTS Major (majorName VARCHAR(255), collegeName VARCHAR, collegeID INT, GPAReq VARCHAR(5));")
	cur.execute("CREATE TABLE IF NOT EXISTS Counselor (counselorID INT, counselorName VARCHAR(255), username VARCHAR, password VARCHAR, majorName VARCHAR(255), roomNum VARCHAR(255));")
	cur.execute("CREATE TABLE IF NOT EXISTS Student (studentID INT, studentName VARCHAR(255), gender VARCHAR(1), majorName VARCHAR(255), studentGPA REAL, ethnicity VARCHAR(255), declared VARCHAR(255), username VARCHAR(255), password VARCHAR(255));")
	cur.execute("CREATE TABLE IF NOT EXISTS Appointment(appID INTEGER PRIMARY KEY AUTOINCREMENT, counselorID INT, studentID INT, hour VARCHAR(10), appDate VARCHAR(255));")

	# Reading in tables
	college = open(collegeFile,'r') 
	college_read = csv.reader(college) 
	college_toDB = [(i[1], i[0]) for i in college_read]

	major = open(majorFile,'r') 
	major_read = csv.reader(major) 
	major_toDB = [(i[1], i[2], i[0], i[3]) for i in major_read]

	counselor = open(counselorFile,'r')
	counselor_read = csv.reader(counselor)
	counselor_toDB = [(i[0], i[1], i[2], i[3], i[4], i[5]) for i in counselor_read]

	student = open(studentFile,'r') 
	student_read = csv.reader(student) 
	student_toDB = [(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]) for i in student_read]

	appointment = open(appointmentFile,'r')
	appointment_read = csv.reader(appointment)
	appointment_toDB = [(i[0], i[1], i[2], i[3], i[4]) for i in appointment_read]
# insert into corresponding tables
	cur.executemany("INSERT INTO College (collegeID, collegeName) VALUES (?,?);", college_toDB)
	cur.executemany("INSERT INTO Major (majorName, collegeName, collegeID, GPAReq) VALUES (?,?,?,?);", major_toDB)
	cur.executemany("INSERT INTO Counselor (counselorID, counselorName, username, password, majorName, roomNum) VALUES (?,?,?,?,?,?);", counselor_toDB)
	cur.executemany("INSERT INTO Student (studentID, studentName, gender, majorName, studentGPA, ethnicity, declared, username, password) VALUES (?,?,?,?,?,?,?,?,?);", student_toDB) 
	cur.executemany("INSERT INTO Appointment (appID, counselorID, studentID, hour, appDate) VALUES (?,?,?,?,?);", appointment_toDB) 


con.commit()
con.close()

