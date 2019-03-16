from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
import os
import pickle
import pdfkit
import zipfile

resultScanner = Flask(__name__)

file_name = ''

@resultScanner.route('/')
def home():
    return render_template("index.htm")

@resultScanner.route('/upload', methods=["POST"])

def upload_file():
    file = request.files['data_file']
    if not file:
        return render_template("failed.htm")

    file.save(file.filename)
    global file_name
    file_name = file.filename
    return render_template("success.htm")


PDFfile = file_name

@resultScanner.route('/logout')
def logout():
    os.system("rm text.txt")
    os.system("rm MarkList.db")
    os.system("rm courses.pickle")
    os.system("rm '"+PDFfile+"'")
    os.system("rm -r zip")
    os.system("rm static/archive.zip")
    return render_template("index.htm")

@resultScanner.route('/failures')
def failures():
    database = sql.connect('MarkList.db')
    database.row_factory = sql.Row
    courses_pickle = open("courses.pickle",'rb')
    global cols
    cols = pickle.load(courses_pickle)
    global courses
    courses = cols
    courses_pickle.close()
    courses = courses[1:]
    cursor = database.cursor()
    sql_query = ["select * from marks where"]
    for x in courses:
        sql_query.append(" ")
        sql_query.append(x)
        sql_query.append("='F'")
        sql_query.append(" or")

    del sql_query[-1]
    sql_query.append(" order by NAME asc")
    query = ""
    for x in sql_query:
        query+=x
    cursor.execute(query)
    global rows
    rows = cursor.fetchall()
    database.close()
    return render_template("failures.html",rows = rows,cols = cols)

@resultScanner.route('/database')
def database():
    if(os.path.isfile("MarkList.db") == False):   
        os.system("python run.py")
    database = sql.connect('MarkList.db')

    database.row_factory = sql.Row
    cursor = database.cursor()
    try: 
        cursor.execute("select * from marks order by NAME asc")
        global rows
        rows = cursor.fetchall()
        courses = open("courses.pickle",'rb')
        global cols
        cols = pickle.load(courses)
        courses.close()
        database.close()
        return render_template("list.html",rows = rows,cols = cols)
    except:
        os.system("rm MarkList.db")
        os.system("rm '"+file_name+"'") 
        return render_template("failed.htm")

@resultScanner.route('/specific', methods=["GET"])
def specific():
    subject = request.args.get('subject')
    type = request.args.get('type')
    subject = subject.encode('ascii','ignore')
    database = sql.connect('MarkList.db')
    database.row_factory = sql.Row
    cursor = database.cursor()
    cols = ['NAME',subject]
    sql_query = ["select NAME,"]
    sql_query.append(subject)
    sql_query.append(" from marks")
    if(type == 'fail'):
        sql_query.append(" where ")
        sql_query.append(subject)
        sql_query.append("='F'")
    elif(type == 'outstanding'):
        sql_query.append(" where ")
        sql_query.append(subject)
        sql_query.append("='O'")
    elif(type == 'result'):
        sql_query.append(" where ")
        sql_query.append(subject)
        sql_query.append("!=''")
    sql_query.append(" order by ")
    if(type == 'fail' or type == 'outstanding'): sql_query.append("name")
    else: sql_query.append(subject)
    sql_query.append(" asc")
    query = ""
    for x in sql_query:
        query+=x
    cursor.execute(query)
    
    rows = cursor.fetchall()
    database.close()
    return render_template("specific.html",rows = rows,cols = cols)
    

@resultScanner.route('/download')
def download():
    pdfkit.from_url('http://localhost:5000/failures', 'all_failures.pdf')

    if not os.path.exists("./zip/subjectwise_failure"):
        os.makedirs("./zip/subjectwise_failure")
    if not os.path.exists("./zip/subjectwise_results"):
        os.makedirs("./zip/subjectwise_results")
    if not os.path.exists("./zip/subjectwise_outstanding"):
        os.makedirs("./zip/subjectwise_outstanding")

    os.system("mv all_failures.pdf ./zip/") 

    for i in courses:
        link= "http://localhost:5000/specific?subject="
        link += i
        link += "&type=fail"
        filename = i+".pdf"
        pdfkit.from_url(link, filename)
        command = "mv "+filename+" ./zip/subjectwise_failure/"
        os.system(command) 

    for i in courses:
        link= "http://localhost:5000/specific?subject="
        link += i
        link += "&type=result"
        filename = i+".pdf"
        pdfkit.from_url(link, filename)
        command = "mv "+filename+" ./zip/subjectwise_results/"
        os.system(command) 

    for i in courses:
        link= "http://localhost:5000/specific?subject="
        link += i
        link += "&type=outstanding"
        filename = i+".pdf"
        pdfkit.from_url(link, filename)
        command = "mv "+filename+" ./zip/subjectwise_outstanding/"
        os.system(command) 

    sub_fail = zipfile.ZipFile('archive.zip', 'w')
 
    for folder, subfolders, files in os.walk('./zip/'):
        for file in files:
            if file.endswith('.pdf'):
                sub_fail.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), 'zip/'), compress_type = zipfile.ZIP_DEFLATED)
    os.system("mv archive.zip static/")
    return redirect(url_for('static', filename='archive.zip'))

if __name__ == '__main__':
    resultScanner.run(debug=True)