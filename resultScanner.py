from flask import Flask, render_template, request
import sqlite3 as sql
import os
import pickle

resultScanner = Flask(__name__)


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

@resultScanner.route('/logout')
def logout():
    os.system("rm text.txt")
    os.system("rm MarkList.db")
    os.system("rm courses.pickle")
    os.system("rm '"+file_name+"'")
    return render_template("index.htm")

@resultScanner.route('/failures')
def failures():
    database = sql.connect('MarkList.db')
    database.row_factory = sql.Row
    courses_pickle = open("courses.pickle",'rb')
    global cols
    cols = pickle.load(courses_pickle)
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

@resultScanner.route('/list')
def list():
    return render_template("list.html",rows = rows,cols = cols)

@resultScanner.route('/database')
def database():
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
    subject = subject.encode('ascii','ignore')
    print("subject is",subject)
    database = sql.connect('MarkList.db')
    database.row_factory = sql.Row
    cursor = database.cursor()
    cols = ['NAME',subject]
    print(cols)
    sql_query = ["select NAME,"]
    sql_query.append(subject)
    sql_query.append(" from marks")
    sql_query.append(" order by ")
    sql_query.append(subject)
    sql_query.append(" asc")
    query = ""
    for x in sql_query:
        query+=x
    cursor.execute(query)
    
    rows = cursor.fetchall()
    database.close()
    return render_template("specific.html",rows = rows,cols = cols)

if __name__ == '__main__':
    resultScanner.run(debug=True)