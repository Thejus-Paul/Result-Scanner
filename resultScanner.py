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

@resultScanner.route('/failures')
def failures():
    database = sql.connect('MarkList.db')
    database.row_factory = sql.Row
    courses_pickle = open("courses.pickle",'rb')
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
        sql_query.append(" and")

    del sql_query[-1]
    query = ""
    for x in sql_query:
        query+=x
    cursor.execute(query)
    rows = cursor.fetchall()

    database.close()
    return render_template("list.html",rows = rows,cols = cols)


@resultScanner.route('/database')
def database():

    os.system("python run.py")
    database = sql.connect('MarkList.db')

    database.row_factory = sql.Row
    cursor = database.cursor()
    try: 
        cursor.execute("select * from marks order by NAME asc")
        rows = cursor.fetchall()
        courses = open("courses.pickle",'rb')
        cols = pickle.load(courses)
        database.close()
        os.system("rm text.txt")
        #os.system("rm MarkList.db")
        os.system("rm "+file_name)
        return render_template("list.html",rows = rows,cols = cols)
    except: 
        return render_template("failed.htm")
if __name__ == '__main__':
    resultScanner.run(debug=True)