from flask import Flask, render_template, redirect, request, url_for, session,flash, jsonify,json
from flask_mysqldb import MySQL, MySQLdb
from sqlalchemy import text
from function import * #เรียกใช้ function จากไฟล์ function.py 
import bcrypt


# Start connect DB
app = Flask(__name__)

app.config['MYSQL_USER']='b1c419bc05a2f4'
app.config['MYSQL_PASSWORD']='4923446e'
app.config['MYSQL_HOST']='us-cdbr-east-02.cleardb.com'
app.config['MYSQL_DB']='heroku_afb54efb4938d74'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    #-------ดูว่านิสิตรหัส...เรียนถึงเทอมไหน ดูใน database -------
    cur = mysql.connection.cursor()
    cur.execute("SELECT MAX(year) FROM student_grade WHERE student_id = '60020671' ")
    maxYear=cur.fetchall() # ค่าที่ printได้ >> ({'MAX(year)': '2'},)
    maxYear=(maxYear[0]['MAX(year)']) # ดึงค่าออกมาจาก tuple ค่าที่ printได้ >> 2  
    maxYear = str(maxYear)
    print('ปีล่าสุดที่เรียน',maxYear)
    cur = mysql.connection.cursor()
    cur.execute("SELECT MAX(DISTINCT(term)) FROM student_grade WHERE student_id = '60020671' AND year = '"+maxYear+"' ")
    termMaxYear = cur.fetchall()
    # print("ยังไม่ได้ดึงค่าออกมา",termMaxYear)
    termMaxYear=(termMaxYear[0]['MAX(DISTINCT(term))']) # ดึงค่าออกมาจาก tuple ค่าที่ printได้ >> 2  
    termMaxYear = str(termMaxYear)
    print("เทอมล่าสุดที่เรียน",termMaxYear)

    #--------------------- กรณีเรีนถึงเทอม 1 ---------------------------------
    if termMaxYear == '1':
        termMaxYear = int(termMaxYear)
        # print(type(termMaxYear))
        maxYear = str(maxYear)
        termMaxYear = termMaxYear + 1
        termMaxYear = str(termMaxYear)
        print("ปีต่อไปที่ต้องเรียน",maxYear,"เทอม",termMaxYear)
        #----- เลือกวิชาตามแผนการเรียนมาจาก database ----------
        cur = mysql.connection.cursor()
        cur.execute("SELECT subject.subject_id,subject.subject_nameTh, subject.subject_nameEng, subject.unit ,study_plan.year ,study_plan.term FROM subject JOIN study_plan ON subject.subject_id = study_plan.subject_id WHERE study_plan.year ='"+maxYear+"' AND study_plan.term='"+termMaxYear+"' AND study_plan.plan_id='60' ")
        subjectCal = cur.fetchall()
        print(subjectCal)

    #--------------------- กรณีเรีนถึงเทอม 1 ---------------------------------    
    elif termMaxYear == '2':
        maxYear = int(maxYear)
        maxYear = maxYear + 1
        maxYear = str(maxYear)
        termMaxYear = "1"
        print("ปีต่อไปที่ต้องเรียน",maxYear,"เทอม",termMaxYear)
        #----- เลือกวิชาตามแผนการเรียนมาจาก database ----------
        cur = mysql.connection.cursor()
        cur.execute("SELECT subject.subject_id,subject.subject_nameTh, subject.subject_nameEng, subject.unit ,study_plan.year ,study_plan.term FROM subject JOIN study_plan ON subject.subject_id = study_plan.subject_id WHERE study_plan.year ='"+maxYear+"' AND study_plan.term='"+termMaxYear+"' AND study_plan.plan_id='60' ")
        subjectCal = cur.fetchall()
        print(subjectCal)



    return render_template('test2.html')

if __name__== "__main__" :
    app.run(debug=True)