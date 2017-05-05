from flask import Flask, render_template, request, redirect
import sqlite3 as lite
import sys
import time
app = Flask(__name__)

@app.route("/")
def goToLogin():
	con = lite.connect("UCBerkeley.db")
	cur = con.cursor()
	return render_template("index.html", **locals())
	

@app.route("/login" , methods=["GET", "POST"])
def loginScreen():

	if request.method == "GET":
		return render_template("login.html", **locals())
	else:
		username = request.form['username']
		password = request.form['password']
		status = request.form['status']
		con = lite.connect("UCBerkeley.db")

		with con:
			cur = con.cursor()
			if status == 'Student':
				print("what is happening GAHHHHHH")
				student_query = "SELECT username, studentID from Student WHERE Student.username = '{username}' AND Student.password = '{password}'".format(username = username, password = password)
				cur.execute(student_query)
				student = cur.fetchone()
				print "PLEASE"
				print student
				if (len(student) > 0):
					student_username = student[0]
					student_id = student[1]
					return redirect("/student/" + str(student_id))
				else:
					return redirect("/login")
			else:
				print (username, password, status)
				cur.execute("SELECT username, counselorID From Counselor WHERE username = '{username}' AND password = '{password}'".format(username = username, password = password))
				logged_counselor = cur.fetchone()
				print(logged_counselor)
				if len(logged_counselor) > 0:
					#logged_counselor = cur.fetchone()
					counselor_username = logged_counselor[0]
					counselor_id = logged_counselor[1]

					return redirect("/counselor/" + str(counselor_id) )
				else:
					return redirect("/login")


@app.route("/student/<int:id>", methods=["GET", "POST"])
def studentPage(id):
	print(request.method)
	if request.method == "GET":
		print("\n\n")
		print(id)
		con = lite.connect("UCBerkeley.db")
		with con:
			cur = con.cursor()
			cur.execute("SELECT Counselor.counselorID from Student, Counselor WHERE Student.majorName = Counselor.majorName AND Student.studentID = " + str(id) + ";")
			counselor_id = cur.fetchone()[0]
			cur.execute("SELECT distinct hour, appDate, counselorName, roomNum, Counselor.counselorID FROM Appointment INNER JOIN Counselor on Appointment.counselorID = Counselor.counselorID WHERE studentID =" + str(id) + " ORDER BY hour ASC;")
			app_name = cur.fetchall()
			print "BABABABA"
			print(counselor_id)


			print(app_name)
			cur.execute("SELECT hour FROM Appointment WHERE appDate = '05/6/2017' and Appointment.counselorID = " + str(counselor_id) + ";"); 
			all_times = [(u'8:00 AM',), (u'8:30 AM',), (u'9:00 AM',), (u'9:30 AM',), (u'10:00 AM',), (u'10:30 AM',), (u'11:00 AM',), (u'11:30 AM',),
			(u'12:00 PM',), (u'12:30 PM',), (u'1:00 PM',), (u'1:30 PM',), (u'2:00 PM',), (u'2:30 PM',), (u'3:00 PM',), (u'3:30 PM',)]
			appointments = cur.fetchall()
			available_times = [i for i in all_times if i not in appointments]
			print available_times
			print("HAHAHAHAHAHA")
			print appointments
			student_id = "/student/" + str(id)

			cur.execute("SELECT * from Appointment;")
			appointments_now = cur.fetchall()
			print("DID IT UPDATE OUR TABLE??????")

			return render_template("student.html", **locals())
	else:
		counselorID = request.form['counselorID']
		print("++++++++++++++++",counselorID, "++++++++++++++")
		hour = request.form['hour']
		potential_hours = ['8:00 AM', '8:30 AM', '9:00 AM', '9:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', '12:00 PM', '12:30 PM', '1:00 PM',
		'1:30 PM', '2:00 PM', '2:30 PM', '3:00 PM', '3:30 PM', '4:00 PM', '4:30 PM']
		if(hour not in potential_hours):
			print("am i in here")
			return redirect("/student/" + str(id))
		print counselorID
		appDate = '05/6/2017'
		con = lite.connect("UCBerkeley.db")
		cur = con.cursor()
		cur.execute("insert into Appointment (counselorID, studentID, hour , appDate) values ('{}', '{}','{}', '{}')".format(counselorID, id, hour, appDate))
		cur.execute("SELECT * from Appointment;")
		all_appointments = cur.fetchall()
		con.commit()
		return redirect("/student/" + str(id) )	
		'''
	if request.method == "GET":
		con = lite.connect("UCBerkeley.db")
		with con:
			cur = con.cursor()
			cur.execute("SELECT * FROM Appointment WHERE Appointment.studentID = " + str(id))
			app_rows = cur.fetchall()
			return render_template("student.html", **locals())
	else:
		date = request.form['date']
		time = request.form['time']
		con = lite.connect("UCBerkeley.db")
		with con:
			cur = con.cursor()
			cur.execute("SELECT majorName FROM Student WHERE Student.id = " + str(id))
			studentMajor = cur.fetchall()#[0]?
			cur.execute("SELECT id FROM Counselor WHERE Counselor.majorName = " + str(studentMajor))
			counselorID = cur.fetchall()#[0]?
			cur.execute("insert into Appointment (counselorID, studentID, time , appDate) values ('{}', '{}','{}', '{}')".format(counselorID, id, time, date))
			cur.execute("SELECT * FROM Appointment WHERE Appointment.studentID = " + str(id))
			app_rows = cur.fetchall()
			return render_template("student.html", **locals())
	'''

@app.route("/counselor/<int:id>")
def counselorPage(id):
	con = lite.connect("UCBerkeley.db")
	with con:
		cur = con.cursor()
		cur.execute("SELECT studentName, hour, appDate, Student.studentID FROM Appointment INNER JOIN Student ON Appointment.studentID = Student.studentID WHERE Appointment.counselorID = " + str(id) + " ORDER BY hour ASC;")
		apps = cur.fetchall()

		return render_template("counselor.html", **locals())
		

@app.route("/studentInfo/<int:studentID>")
def studentInfo(studentID):
	con = lite.connect("UCBerkeley.db")
	with con:
		cur = con.cursor()
		cur.execute("SELECT studentName, Student.majorName, gender, ethnicity, studentGPA, gpaReq, College.collegeName, declared from Student INNER JOIN Major ON Student.majorName = Major.majorName INNER JOIN College ON Major.collegeID = College.collegeID WHERE Student.studentID = " + str(studentID) + " ;")
		student= cur.fetchone()
		name = student[0]
		major = student[1]
		gender = student[2]
		etchnicity = student[3]
		gpa = student[4]
		required_gpa = "Required GPA: " + student[5] if student[7] == "False" else ""
		college_name = student[6]
		declared = "Declared" if student[7] == "True" else "Intended"
	

		return render_template("studentInfo.html", **locals())

if __name__ == "__main__":
	app.run()