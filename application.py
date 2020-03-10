from flask import Flask, render_template, request
import csv
#import pandas as pd
import os
import base64
import sqlite3
from sqlite3 import Error
from werkzeug.utils import secure_filename

application = app = Flask(__name__)

#conn = sqllite3.connect(':memory:')
conn = sqlite3.connect('student.db', check_same_thread=False)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/uploadcsv', methods=['POST'])
def uploadcsv():
    file = request.files['fileupload']
    print(file.filename)
    # print(type(file.read()))
    # print(file.read())
    print('XXXX..........XXXXXXX')
    file.save(secure_filename(file.filename))
    # print(file.read().decode('utf-8').splitlines())
    # data = file.read().decode('utf-8').splitlines()
    # for l in data:
    #     print(l)

    with open(secure_filename(file.filename)) as csvfile:
        fileread = csv.reader(csvfile, delimiter=',')
        #print(fileread)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS
            student (name TEXT, grade INT, room INT,
            telnum INT, picture TEXT, keywords TEXT) """)

        for row in fileread:
            name = row[0]
            grade = row[1]
            room = row[2]
            telnum = row[3]
            picture = row[4]
            keywords = row[5]
            # es = picture
            # dict = {picture:es}

            if not picture == "":
                with open(picture, "rb") as pic:
                    encoded_string = base64.b64encode(pic.read())
                    # print(encoded_string)
                    ds = encoded_string.decode('utf_8')
                    #dict = {pic:ds}

            cursor.execute("INSERT INTO student (name, grade, room, telnum, picture, keywords) VALUES (?,?,?,?,?,?)", (name, grade, room, telnum, ds, keywords))

        conn.commit()

    return render_template('home.html')

@app.route('/list')
def liststudents():

    #conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM student')
    rows = cursor.fetchall()

    return render_template('liststudents.html', studlist=rows)

@app.route('/searchuser', methods=['POST'])
def search_user_by_name():
    uname = request.form['usersearch']
    if not uname == "":
        print('haha '+uname)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM student where name like ?', ('%'+uname+'%',))
        rows = cursor.fetchall()

    return render_template('searchname.html', title='User search', record=rows)

@app.route('/searchgrade', methods=['POST'])
def search_user_by_grade():
    grade = request.form['usergrade']
    if not grade == "":
        print('haha '+grade)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM student where grade < ?', (grade,))
        rows = cursor.fetchall()

    return render_template('searchgradepage.html', title='User grade', record=rows)

@app.route('/changepic', methods=['POST'])
def change_picture():
    name = request.form['username']
    pic = request.files['picupload']
    if not name == "":
        encoded_string = base64.b64encode(pic.read())
        ds = encoded_string.decode('utf_8')
        cursor = conn.cursor()
        cursor.execute('UPDATE student SET picture = ? where name = ?', (ds,name))
        rows = cursor.fetchall()

    return render_template('changepicture.html', title='User grade', record=rows)


@app.route('/removeuser', methods=['POST'])
def removeuser():
    uname = request.form['userremove']
    if not uname == "":
        print('del '+uname)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM student where name like ?', ('%'+uname+'%',))
        rows = cursor.fetchall()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM student where name like ?', ('%'+uname+'%',))

    return render_template('removeuser.html', title='User Delete', record=rows)

@app.route('/changekeywords', methods=['POST'])
def change_keywords():
    uname = request.form['username']
    keyw = request.form['userkeyw']
    if not uname == "":
        print(uname+ ', ' + keyw)
        cursor = conn.cursor()
        cursor.execute('UPDATE student set keywords = ? where name = ?', (keyw,uname))
        rows = cursor.fetchall()
        conn.commit()

    return render_template('changekeywords.html', title='Keywords Update', record=rows)

@app.route('/changegrade', methods=['POST'])
def change_grade():
    uname = request.form['username']
    grade = request.form['usergrade']
    if not uname == "":
        print(uname+ ', ' + grade)
        cursor = conn.cursor()
        cursor.execute('UPDATE student set grade = ? where name = ?', (grade,uname))
        rows = cursor.fetchall()
        conn.commit()

    return render_template('changegrade.html', title='Grade Update', record=rows)

@app.route('/searchpage')
def search_page():
    return render_template('searchname.html')

@app.route('/gradefilterpage')
def search_grade_page():
    return render_template('searchgradepage.html', title='Grade Filter')

@app.route('/changepicpage')
def change_pic_page():
    return render_template('changepicture.html', title='Update Pic')

@app.route('/removepage')
def removeuserpage():
    return render_template('removeuser.html', title='Delete')

@app.route('/changekeywordpage')
def change_keyw_page():
    return render_template('changekeywords.html', title='Keyword Change')

@app.route('/changegradepage')
def change_grade_page():
    return render_template('changegrade.html', title='Grade Change')

if __name__ == '__main__':
    app.run(debug=True)
