from flask import Flask, render_template, request
import sqlite3 as sql
import os

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


@resultScanner.route('/database')
def database():
    os.system("python run.py")
    con = sql.connect('MarkList.db')

    con.row_factory = sql.Row
    cur = con.cursor()
    try: 
        cur.execute("select * from marks where CS100 is NOT ''")
        rows = cur.fetchall()
        con.close()
        os.system("rm text.txt")
        os.system("rm MarkList.db")
        os.system("rm "+file_name)
        return render_template("list.html",rows = rows)
    except: 
        os.system("rm "+file_name)
        return render_template("failed.htm")


if __name__ == '__main__':
    resultScanner.run(debug=True)