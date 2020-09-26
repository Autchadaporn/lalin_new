from flask import Flask, render_template, redirect, request, url_for, session,flash, jsonify,json
from flask_mysqldb import MySQL, MySQLdb
from sqlalchemy import text
import bcrypt


# Start connect DB
app = Flask(__name__)

app.config['MYSQL_USER']='b1c419bc05a2f4'
app.config['MYSQL_PASSWORD']='4923446e'
app.config['MYSQL_HOST']='us-cdbr-east-02.cleardb.com'
app.config['MYSQL_DB']='heroku_afb54efb4938d74'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql = MySQL(app)

# @app.route('/')
# def index():
#     #-------ดูว่านิสิตรหัส...เรียนถึงเทอมไหน ดูใน database -------
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT MAX(year) FROM student_grade WHERE student_id = '60020671' ")
#     maxYear=cur.fetchall() # ค่าที่ printได้ >> ({'MAX(year)': '2'},)
#     maxYear=(maxYear[0]['MAX(year)']) # ดึงค่าออกมาจาก tuple ค่าที่ printได้ >> 2  
#     maxYear = str(maxYear)
#     print('ปีล่าสุดที่เรียน',maxYear)
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT MAX(DISTINCT(term)) FROM student_grade WHERE student_id = '60020671' AND year = '"+maxYear+"' ")
#     termMaxYear = cur.fetchall()
#     # print("ยังไม่ได้ดึงค่าออกมา",termMaxYear)
#     termMaxYear=(termMaxYear[0]['MAX(DISTINCT(term))']) # ดึงค่าออกมาจาก tuple ค่าที่ printได้ >> 2  
#     termMaxYear = str(termMaxYear)
#     print("เทอมล่าสุดที่เรียน",termMaxYear)

#     #--------------------- กรณีเรีนถึงเทอม 1 ---------------------------------
#     if termMaxYear == '1':
#         termMaxYear = int(termMaxYear)
#         # print(type(termMaxYear))
#         maxYear = str(maxYear)
#         termMaxYear = termMaxYear + 1
#         termMaxYear = str(termMaxYear)
#         print("ปีต่อไปที่ต้องเรียน",maxYear,"เทอม",termMaxYear)
#         #----- เลือกวิชาตามแผนการเรียนมาจาก database ----------
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT subject.subject_id,subject.subject_nameTh, subject.subject_nameEng, subject.unit ,study_plan.year ,study_plan.term FROM subject JOIN study_plan ON subject.subject_id = study_plan.subject_id WHERE study_plan.year ='"+maxYear+"' AND study_plan.term='"+termMaxYear+"' AND study_plan.plan_id='60' ")
#         subjectCal = cur.fetchall()
#         print(subjectCal)

#         #------------------- บันทึกผลการเรียนเทอมที่คำนวณ ส่งอาจารย์ -------------------------
#         # 1) กดบันทึกลง database 
            


#     #--------------------- กรณีเรียนถึงเทอม 1 ---------------------------------    
#     elif termMaxYear == '2':
#         maxYear = int(maxYear)
#         maxYear = maxYear + 1
#         maxYear = str(maxYear)
#         termMaxYear = "1"
#         print("ปีต่อไปที่ต้องเรียน",maxYear,"เทอม",termMaxYear)
#         #----- เลือกวิชาตามแผนการเรียนมาจาก database ----------
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT subject.subject_id,subject.subject_nameTh, subject.subject_nameEng, subject.unit ,study_plan.year ,study_plan.term FROM subject JOIN study_plan ON subject.subject_id = study_plan.subject_id WHERE study_plan.year ='"+maxYear+"' AND study_plan.term='"+termMaxYear+"' AND study_plan.plan_id='60' ")
#         subjectCal = cur.fetchall()
#         print(subjectCal)
#     return render_template('test2.html')

@app.route('/gradeall')
def gradeall():
    # if data == None:
    #     print("ไม่มี")
    # data = "Ud0c7fe8f06589b9b9d075a88188318cf"
    # if request.method == "GET":
    #     print("เข้ามาแล้ว")
    #     data = request.args.get('result')

    # if data == None:
    #     return render_template('grade.html')
    # elif data != None:
        # print("ตรงนี้",data)
        # cur = mysql.connection.cursor()
        # cur.execute("SELECT  members.member_id FROM members  WHERE token_id = '"+data+"' ") # ex. ดูว่ารหัสนิสิต 60023179 เรียนอะไรไปแล้วบ้าง
        # studentId=cur.fetchall()
        # studentId=(studentId[0]['member_id'])
        # print(studentId)
    
    
        studentId = '60023179' #<< ลองใส่เกรดดูค่า ทำ css 

       #---------------------แสดงรหัสวิชา เกรดที่เรียนไแล้วทั้งหมด ---------------# 
        # cur = mysql.connection.cursor()
        # cur.execute("SELECT student_grade.student_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng ,student_grade.grade , student_grade.unit , student_grade.year, student_grade.term  FROM student_grade JOIN subject ON subject.subject_id = student_grade.subject_id WHERE student_id = '"+studentId+"' ") # ex. ดูว่ารหัสนิสิต 60023179 เรียนอะไรไปแล้วบ้าง
        # data1=cur.fetchall()
        # print(data1)

        #---------------------นับปีที่เรียน เทอมที่เรียน--------------------------#
        cur = mysql.connection.cursor()
        cur.execute("select DISTINCT(student_grade.year) from student_grade where student_grade.student_id = '"+studentId+"' ")
        year = cur.fetchall()
        print(year)

        cur = mysql.connection.cursor()
        cur.execute("select DISTINCT(student_grade.term) from student_grade where student_grade.student_id = '"+studentId+"' ")
        term = cur.fetchall()
        print(term)

        for i in range(len(year)):
            # print(year[i]['year'])
            for x in range(len(term)):
                print(year[i]['year'],term[x]['term'])

    #     #------------------------------ start คำนวนเกรด gpax---------------------------------#
    #     cur.execute("SELECT unit FROM student_grade WHERE student_id = '"+studentId+"' ")
    #     unit = cur.fetchall()
    #     sumUnit = 0 
    #     for indexUnit in range(0,len(unit)):
    #         unitCal = (unit[indexUnit]['unit'])
    #         # print (float(unitcal))
    #         sumUnit = sumUnit + float(unitCal) 
    #     # print(sumnUit)

    #     cur.execute("SELECT grade FROM student_grade WHERE student_id = '"+studentId+"' ")
    #     grade = cur.fetchall()
    #     #print(grade)
    #     sum = 0
    #     for indexGrade in range(0,len(grade)):
    #         gradeCal = (tranformgrade(grade[indexGrade]['grade'])) #เรียกใช้ฟังก์ชั่น tranformgrade แปลงเกรด ex. A=4.00 ,B=3.00 
    #         #print(float(gradeCal))
    #         for indexUnit in range(0,len(unit)):
    #             unitCal = (unit[indexUnit]['unit'])
    #             if indexGrade==indexUnit:
    #                 sumGradeUnit = float(gradeCal) * float(unitCal)
    #                 sum = sum + sumGradeUnit
    #     # print(sum)
    #     GPAX = sum/sumUnit
    #     #---- start แสดงทศนิยม2ตำแหน่ง---------#
    #     x = str(GPAX)
    #     # print(type(x))
        
    #     itemGPAX = ""
    #     for i in range(0,4):
    #         itemGPAX = itemGPAX + x[i]
    #     print(itemGPAX)
    # #------ stop แสดงทศนิยม2ตำแหน่ง--------#
    #     print(data1)
    #------------------------------ stop คำนวนเกรด gpax---------------------------------#
        return render_template('test3.html')
        # return render_template('test2.html',data1=data1,GPAX=itemGPAX)
        # return render_template('index.html')




if __name__== "__main__" :
    app.run(debug=True)