#---------------------------------------------
# CONVERTING PDF TO TEXT
#---------------------------------------------
print
try:
	import PyPDF2
	pdf_file = open('result_RET.pdf','rb')
	read_pdf = PyPDF2.PdfFileReader(pdf_file)
	number_of_pages = read_pdf.getNumPages()
	for i in range(number_of_pages):
	    page = read_pdf.getPage(i)
	    page_content = page.extractText()
	    file = open("text.txt","a")
	    file.write(page_content)
	    file.close()
	print("Converting PDF to text................. SUCCESS")
except: print("Converting PDF to text................. FAILED")

#---------------------------------------------
# EXTRACTING TEXT
#---------------------------------------------

global courses
courses = []
global dictionary # Dictionary for storing student ID and course grades dictionary.[Dictionary in Dictionary Concept]
dictionary = {}
print
try:
	import re       								# Module for Regular Expression(REGEX).
	import pickle
	source = open("text.txt",'r')
	regex = r"RET[0-9]+IT[0-9]+"					# REGEX for extracting required students.
	source_text = source.read()
	students_list = re.findall(regex, source_text)	# Storing all the required students from the source text.


	start = source_text.index(students_list[0])	# start index before required students.
	end = source_text.index("MECHANICAL ENGINEERING[Full Time]") #stop index after required students.

	require_text = source_text[ start : end ] # Slicing the required text from source.
	require_text = require_text.replace(",","").replace(" ","").replace(")",") ") # Clearing unwanted characters.

	regex = r"[A-Z][A-Z][1-9][0-9][0-9]"			# REGEX for the courses
	courses = set(re.findall(regex, require_text))	# Finding and storing all courses written by students.

	cols = ["NAME"]
	for x in courses:
		cols.append(x)

	courses_pickle  = open("courses.pickle",'wb')
	pickle.dump(cols,courses_pickle)
	courses_pickle.close()

	for course in courses:
		require_text = require_text.replace(course,(" "+course)) # Seperating student ID and cosecutive course. 

	filtered_text = []								
	for i in require_text.split(" "):
		if(i != ''): filtered_text.append(i)		# Filtering out '' from the list from required_text.

	filtered_text.append("end")
					
	student = ''
	for i in filtered_text:
		if(i[0] == 'R'):							# 'R'ET17IT001
			if(student == ''):						# If it is the first student from the filtered_text.
				student = i 						# student = RET17IT001
				student_grades = {}					# student_grades will contain {course:grade} pair.
			else:
				dictionary.update({student:student_grades}) # Adding the student_grades dictionary to dictionary.
				student_grades = {}						# Resetting students_grades dictionary.
				student = i 							# Next student from the filtered_text.
		elif (i == 'end'):
			dictionary.update({student:student_grades})
			student_grades = {}
		else:
			student_grades.update({i[:5]:i[6:(len(i)-1)]}) 
		
	'''
		Above line does the following:
		if CS120(A+) is 'i' then 
			i[:5] = CS120
			i[6:(len(i)-1)] = A+
		student_grades will be updated with {'CS120':'A+'}
	'''
	print("Extracting information from text....... SUCCESS")
except: print("Extracting information from text....... FAILED")

#-------------------------------------------------------
# UPLOADING TO DATABASE
#-------------------------------------------------------

import sqlite3
print
def create_connection(file):				# Function to create a connection with Database.
	try:
		conn = sqlite3.connect(file)
		return conn
	except: return None

def create_table(conn, sql_create_table):	# Function to create a table.
	c = conn.cursor()
	c.execute(sql_create_table)

def insert_data(conn, inputs):				# Function to insert data.
	sql = ["INSERT INTO marks"]
	sql.append(" VALUES(?,?")
	for x in range(len(courses)):
		sql.append(',?')
	sql.append(')')
	
	sql_query = ""
	for i in sql: sql_query+=i

	c = conn.cursor()
	c.execute(sql_query,inputs)
	conn.commit()

conn = create_connection("MarkList.db")		# Create a database called 'MarkList.db' and create a connection.

sql_create_table = "CREATE TABLE IF NOT EXISTS marks (id integer PRIMARY KEY,NAME text NOT NULL,"	# Create table if it doesn't exist in the database.
sql_command = [sql_create_table]
for course in courses: sql_command.append((course+" text,"))	# Adding all the required courses as columns in the database.
sql_command[len(sql_command)-1]=sql_command[len(sql_command)-1][:-1] # Filtering out ',' character from last.
sql_command.append(");")

sql_create_table = ""
for i in sql_command: sql_create_table+=i 	# Join words in 'sql_command' list to a string.
try:
	if conn is not None: create_table(conn, sql_create_table)	# Create the required table if not exists.
except: 
	print("Uploading information to database...... FAILED")
	print
	exit(0)

for item in dictionary:
	inputs = [None, item]	# SQL each student details insertion list.
	for x in range(len(courses)):
		inputs.append("")
	count = 1 								# Counter to correctly insert grade corresponding to the course. 
	for i in courses:
		try:
			count+=1
			if(dictionary[item][i]):		# If a student have a mentioned course in the field then,
				inputs[count] = dictionary[item][i]		# 'inputs' list will replace corresponding None with grade. 
		except:
			continue						# If there is no course for that student then continue.
	insert_data(conn, inputs)				# Insert the data into the DB.
print("Uploading information to database...... SUCCESS")
print