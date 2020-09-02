from flask import Flask, render_template, redirect, request, url_for, session,flash, jsonify,json
from flask_mysqldb import MySQL, MySQLdb
from sqlalchemy import text
from function import * #เรียกใช้ function จากไฟล์ function.py 
import bcrypt

# from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired 

# Start connect DB
app = Flask(__name__)

app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_HOST']='127.0.0.1'
app.config['MYSQL_DB']='lalin_new'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('hello.html')

@app.route('/subject')
def student():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM subject")
    data=cur.fetchall()
    return render_template('subject.html',data=data)

@app.route('/gradeall')
def gradeall():
    cur = mysql.connection.cursor()
    cur.execute("SELECT student_grade.student_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng ,student_grade.grade , student_grade.unit , student_grade.term , student_grade.year FROM student_grade JOIN subject ON subject.subject_id = student_grade.subject_id WHERE student_id = '60020671' ") # ex. ดูว่ารหัสนิสิต 60023179 เรียนอะไรไปแล้วบ้าง
    data1=cur.fetchall()
    
    #------------------------------ start คำนวนเกรด gpax---------------------------------#
    cur.execute("SELECT unit FROM student_grade WHERE student_id = '60020671' ")
    unit = cur.fetchall()
    sumUnit = 0 
    for indexUnit in range(0,len(unit)):
        unitCal = (unit[indexUnit]['unit'])
        # print (float(unitcal))
        sumUnit = sumUnit + float(unitCal) 
    # print(sumnUit)

    cur.execute("SELECT grade FROM student_grade WHERE student_id = '60020671' ")
    grade = cur.fetchall()
    #print(grade)
    sum = 0
    for indexGrade in range(0,len(grade)):
        gradeCal = (tranformgrade(grade[indexGrade]['grade'])) #เรียกใช้ฟังก์ชั่น tranformgrade แปลงเกรด ex. A=4.00 ,B=3.00 
        #print(float(gradeCal))
        for indexUnit in range(0,len(unit)):
            unitCal = (unit[indexUnit]['unit'])
            if indexGrade==indexUnit:
                sumGradeUnit = float(gradeCal) * float(unitCal)
                sum = sum + sumGradeUnit
    # print(sum)
    GPAX = sum/sumUnit
    #---- start แสดงทศนิยม2ตำแหน่ง---------#
    x = str(GPAX)
    # print(type(x))
    itemGPAX = ""
    for i in range(0,4):
        itemGPAX = itemGPAX + x[i]
    print(itemGPAX)
    #------ stop แสดงทศนิยม2ตำแหน่ง--------#

    #------------------------------ stop คำนวนเกรด gpax---------------------------------#
    return render_template('grade.html',data1=data1,GPAX=itemGPAX)

@app.route('/showgrade')
def showgrade():
   
    cur = mysql.connection.cursor()
    cur.execute("SELECT MAX(year) FROM student_grade") # หาปีที่มากสุดใน database
    maxyear = cur.fetchall() # แสดงผล {'MAX(year)': '2'}
    y = (maxyear[0]['MAX(year)']) #ดึง 2 ออกมา ผลลัพธ์ y = 2 เป็น str 
    y = int(y)
    for i in range(1,y+1):
        for p in range(1,3): 
            print(i,p) # i คือปี p คือ เทอม
    
    #---------  start เอาเกรด database แสดงผลหน้า showgrade.html ----------------#
    cur = mysql.connection.cursor()
    cur.execute("SELECT student_grade.student_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng ,student_grade.grade , student_grade.unit , student_grade.term , student_grade.year FROM student_grade JOIN subject ON subject.subject_id = student_grade.subject_id WHERE student_grade.student_id = '60023179' and student_grade.year = '"+i+"' and student_grade.term = '"+p+"' ") # ex. ดูว่ารหัสนิสิต 60023179 เรียนอะไรไปแล้วบ้าง
    data = cur.fetchall()
    print(data)
    #---------  stop เอาเกรด database แสดงผลหน้า showgrade.html ----------------#
    
    #------------------------------ start คำนวนเกรด GPA ---------------------------------#
    cur.execute("SELECT unit FROM student_grade WHERE student_id = '60023179' and year ='"+i+"'  and term = '"+p+"' ")
    unit = cur.fetchall()
    sumUnit = 0 
    for indexUnit in range(0,len(unit)):
        unitCal = (unit[indexUnit]['unit'])
        # print (float(unitcal))
        sumUnit = sumUnit + float(unitCal) 
    # print(sumnUit)

    cur.execute("SELECT grade FROM student_grade WHERE student_id = '60023179' and year ='"+i+"' and term = '"+p+"'  ")
    grade = cur.fetchall()
    #print(grade)
    sum = 0
    for indexGrade in range(0,len(grade)):
        gradeCal = (tranformgrade(grade[indexGrade]['grade'])) #เรียกใช้ฟังก์ชั่น tranformgrade แปลงเกรด ex. A=4.00 ,B=3.00 
        #print(float(gradeCal))
        for indexUnit in range(0,len(unit)):
            unitCal = (unit[indexUnit]['unit'])
            if indexGrade==indexUnit:
                sumGradeUnit = float(gradeCal) * float(unitCal)
                sum = sum + sumGradeUnit
    # print(sum)
    GPA = sum/sumUnit
    #---- start แสดงทศนิยม2ตำแหน่ง---------#
    x = str(GPA)
    # print(type(x))
    itemGPA = ""
    for i in range(0,4):
        itemGPA = itemGPA + x[i]
    print(itemGPA)
    #------ stop แสดงทศนิยม2ตำแหน่ง--------
    #------------------------------ stop คำนวนเกรด GPA ---------------------------------#


    return render_template('showgrade.html',data=data,GPA=itemGPA)
    # return render_template('showgrade.html',data=data)

#-----------------เลือกเกรดมาแสดง--------------------------------------
@app.route('/calculate')
def calculate():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM subject")
    subject = cur.fetchall()
    return render_template('test1.html',subject=subject)
    
 
#-------------------แสดงแผนการเรียนทั้งหมด------------------------
@app.route('/showstudyplan')
def showstudyplan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT study_plan.study_plan_row_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng, study_plan.year , study_plan.term FROM subject JOIN study_plan ON subject.subject_id = study_plan.subject_id WHERE study_plan.plan_id = '60' and study_plan.year ='1' and study_plan.term='1'")
    data1 = cur.fetchall()
    cur.execute("SELECT study_plan.study_plan_row_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng, study_plan.year , study_plan.term FROM subject JOIN study_plan ON subject.subject_id = study_plan.subject_id WHERE study_plan.plan_id = '60' and study_plan.year ='1' and study_plan.term='2'")
    data2 = cur.fetchall()
    cur.execute("SELECT study_plan.study_plan_row_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng, study_plan.year , study_plan.term FROM subject JOIN study_plan ON subject.subject_id = study_plan.subject_id WHERE study_plan.plan_id = '60' and study_plan.year ='2' and study_plan.term='1'")
    data3 = cur.fetchall()
    cur.execute("SELECT study_plan.study_plan_row_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng, study_plan.year , study_plan.term FROM subject JOIN study_plan ON subject.subject_id = study_plan.subject_id WHERE study_plan.plan_id = '60' and study_plan.year ='2' and study_plan.term='2'")
    data4 = cur.fetchall()
    cur.execute("SELECT study_plan.study_plan_row_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng , study_plan.year , study_plan.term FROM subject JOIN study_plan ON subject.subject_id = study_plan.subject_id WHERE study_plan.plan_id = '60' and study_plan.year ='3' and study_plan.term='1'")
    data5 = cur.fetchall()
    cur.execute("SELECT study_plan.study_plan_row_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng , study_plan.year , study_plan.term FROM subject JOIN study_plan ON subject.subject_id = study_plan.subject_id WHERE study_plan.plan_id = '60' and study_plan.year ='3' and study_plan.term='2'")
    data6 = cur.fetchall()
    cur.execute("SELECT study_plan.study_plan_row_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng , study_plan.year , study_plan.term FROM subject JOIN study_plan ON subject.subject_id = study_plan.subject_id WHERE study_plan.plan_id = '60' and study_plan.year ='4' and study_plan.term='1'")
    data7 = cur.fetchall()
    cur.execute("SELECT study_plan.study_plan_row_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng , study_plan.year , study_plan.term FROM subject JOIN study_plan ON subject.subject_id = study_plan.subject_id WHERE study_plan.plan_id = '60' and study_plan.year ='4' and study_plan.term='2'")
    data8 = cur.fetchall()
    return render_template('showstudyplan.html',data1=data1,data2=data2,data3=data3,data4=data4,data5=data5,data6=data6,data7=data7,data8=data8)

#---------------------ค้นหาแผนการศึกษา----------------------------------------
@app.route("/searchplan",methods=['GET','POST'])
def searchplan():
    if request.method == 'POST':
        year = request.form['year']
        term = request.form['term']
        # print(year,term)
        cur = mysql.connection.cursor()
        cur.execute("SELECT study_plan.study_plan_row_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng, study_plan.year , study_plan.term FROM subject JOIN study_plan ON subject.subject_id = study_plan.subject_id WHERE study_plan.plan_id = '60' and study_plan.year ='"+year+"' and study_plan.term='"+term+"' ")
        data = cur.fetchall()
        # print(data)
    return render_template('searchstudyplan.html',data = data,year=year,term=term)

@app.route("/calendar")
def  calendar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT topic.topic_name, calendar.term ,calendar.date_start, calendar.date_stop,calendar.year FROM topic INNER JOIN calendar ON topic.topic_id = calendar.topic_id ")
    data = cur.fetchall()
    return render_template('calendar.html',data=data)
    

if __name__== "__main__" :
    app.run(debug=True)