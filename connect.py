from flask import Flask, render_template, redirect, request, url_for, session,flash, jsonify,json
from flask_mysqldb import MySQL, MySQLdb
from sqlalchemy import text
from function import * #เรียกใช้ function จากไฟล์ function.py 
import bcrypt

# from flask_wtf import FlaskForm
# from wtforms import StringField, FieldList, FormField, SubmitField
# from wtforms.validators import DataRequired 

# Start connect DB
app = Flask(__name__)

# app.config['MYSQL_USER']='root'
# app.config['MYSQL_PASSWORD']=''
# app.config['MYSQL_HOST']='127.0.0.1'
# app.config['MYSQL_DB']='lalin_new'
# app.config['MYSQL_CURSORCLASS']='DictCursor'

app.config['MYSQL_USER']='b1c419bc05a2f4'
app.config['MYSQL_PASSWORD']='4923446e'
app.config['MYSQL_HOST']='us-cdbr-east-02.cleardb.com'
app.config['MYSQL_DB']='heroku_afb54efb4938d74'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subject')
def student():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM subject")
    data=cur.fetchall()
    return render_template('subject.html',data=data)



@app.route('/get_token', methods=['GET','POST'])
def get_token():
    # print("เข้า")
    # clicked=None
    if request.method == "GET":
        print("เข้ามาแล้ว")
        data = request.args.get('result')
    return chect_id(data)
    #     # clicked = request.get_json(['data'])
    #     print("เข้าjsonมาแล้ว")
#  return render_template('test.html')
    # print(clicked)
    # return render_template('Verify.html')
def chect_id(data):
    # print(data)
    return gradeall(data)






@app.route('/test')
def test():
    return render_template('test.html')



@app.route('/gradeall')
def gradeall():
    # if data == None:
    #     print("ไม่มี")
    # data = "Ud0c7fe8f06589b9b9d075a88188318cf"
    if request.method == "GET":
        print("เข้ามาแล้ว")
        data = request.args.get('result')

    if data == None:
        return render_template('grade.html')
    elif data != None:
        print("ตรงนี้",data)
        cur = mysql.connection.cursor()
        cur.execute("SELECT  members.member_id FROM members  WHERE token_id = '"+data+"' ") # ex. ดูว่ารหัสนิสิต 60023179 เรียนอะไรไปแล้วบ้าง
        studentId=cur.fetchall()
        studentId=(studentId[0]['member_id'])
        print(studentId)
        cur = mysql.connection.cursor()
        cur.execute("SELECT student_grade.student_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng ,student_grade.grade , student_grade.unit , student_grade.year, student_grade.term  FROM student_grade JOIN subject ON subject.subject_id = student_grade.subject_id WHERE student_id = '"+studentId+"' ") # ex. ดูว่ารหัสนิสิต 60023179 เรียนอะไรไปแล้วบ้าง
        data1=cur.fetchall()
        
        #------------------------------ start คำนวนเกรด gpax---------------------------------#
        cur.execute("SELECT unit FROM student_grade WHERE student_id = '"+studentId+"' ")
        unit = cur.fetchall()
        sumUnit = 0 
        for indexUnit in range(0,len(unit)):
            unitCal = (unit[indexUnit]['unit'])
            # print (float(unitcal))
            sumUnit = sumUnit + float(unitCal) 
        # print(sumnUit)

        cur.execute("SELECT grade FROM student_grade WHERE student_id = '"+studentId+"' ")
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
        print(data1)
    #------------------------------ stop คำนวนเกรด gpax---------------------------------#
        return render_template('grade.html',data1=data1,GPAX=itemGPAX)
        # return render_template('index.html')








#-------------------------------------------คำนวณเกรด---------------------------------
@app.route('/gradecal',methods=['POST','GET'])
def gradecal():
    # print("ตรงนี้",data)
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT  members.member_id FROM members  WHERE token_id = '"+data+"' ") # ex. ดูว่ารหัสนิสิต 60023179 เรียนอะไรไปแล้วบ้าง
    # studentId=cur.fetchall()
    # studentId=(studentId[0]['member_id'])
    # print(studentId)

    #--------- ถ้ามีค่าส่งมา เป็น post -------#
    grade =[]
    unit=[]
    if request.method == 'POST':
        grade = request.form.getlist('grade[]')
        unit = request.form.getlist('unit[]')
        # print("grade",grade)
        # print("unit",unit)
        # print(type(unit))
        print("***********************************************************************")
        print('หน่วยกิต:',unit)
        print('เกรด:',grade)
        print("***********************************************************************")
         #---------------------เช็ค W------------------------------------
        for i in range(len(grade)): #วนลูปเช็คว่ามี W ไหม
            # print(Grade[i])
            if (grade[i] == 'W') or (grade[i] == 'P') or (grade[i] == 'I') or (grade[i] == 'S') or (grade[i] == 'U'):
                grade[i] = 0
                for x in range(len(unit)): #วนหาหน่วยกิตที่ติด W
                    if x == i:
                        unit[x] = 0 #เปลี่ยนหน่วตกิตวิชาที่ติด W ให้มีค่าเป็น 0
                        
            else :
                print(grade[i]) #เกรดที่นำมาคิด
            
        print("***********************************************************************")
        print('หน่วยกิต:',unit)
        print('เกรด:',grade)
        print("***********************************************************************")

        #------------------------------ start คำนวนเกรด gpax---------------------------------#
        sumUnit= 0
        for indexUnit in range(0,len(unit)):
            # print("หน่วยกิต ",unit[indexUnit])
            sumUnit = sumUnit + (float(unit[indexUnit]))
        print("sumUnit : ผลรวมหน่วยกิต",sumUnit)

        sum = 0
        for indexGrade in range(0,len(grade)):
            gradeCal = (tranformgrade(grade[indexGrade])) #เรียกใช้ฟังก์ชั่น tranformgrade แปลงเกรด ex. A=4.00 ,B=3.00 
            # print(gradeCal)
            # print(type(gradeCal))
            for indexUnit in range(0,len(unit)):
                unitCal = (unit[indexUnit])
                # print(type(unitCal))
                if indexGrade==indexUnit:
                    sumGradeUnit = float(gradeCal) * (float(unitCal))
                    sum = sum + sumGradeUnit
        GPA = sum/sumUnit
        GPA = '%.4f'%(GPA)
        x = str(GPA)
        itemGPA = ""
        for i in range(0,4):
            itemGPA = itemGPA+ x[i]
        print("itemGPA : เกรดเฉลี่ย",itemGPA)
        cur = mysql.connection.cursor()
        cur.execute("SELECT student_grade.student_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng ,student_grade.grade , student_grade.unit , student_grade.year, student_grade.term  FROM student_grade JOIN subject ON subject.subject_id = student_grade.subject_id WHERE student_id = '60020671'") # ex. ดูว่ารหัสนิสิต 60023179 เรียนอะไรไปแล้วบ้าง
        subject=cur.fetchall()
        # print(subject)
        
        #------------------------------ start คำนวนเกรด gpax---------------------------------#
        cur.execute("SELECT unit FROM student_grade WHERE student_id = '60020671' ")
        unit = cur.fetchall()
        sumUnit1 = 0 
        for indexUnit in range(0,len(unit)):
            unitCal = (unit[indexUnit]['unit'])
            # print (float(unitcal))
            sumUnit1 = sumUnit1 + float(unitCal) 
        print("แสดงผลsumUnit1 ก่อน:",sumUnit1)

        cur.execute("SELECT grade FROM student_grade WHERE student_id = '60020671' ")
        grade = cur.fetchall()
        #print(grade)
        sum1 = 0
        for indexGrade in range(0,len(grade)):
            gradeCal = (tranformgrade(grade[indexGrade]['grade'])) #เรียกใช้ฟังก์ชั่น tranformgrade แปลงเกรด ex. A=4.00 ,B=3.00 
            #print(float(gradeCal))
            for indexUnit in range(0,len(unit)):
                unitCal = (unit[indexUnit]['unit'])
                if indexGrade==indexUnit:
                    sumGradeUnit = float(gradeCal) * float(unitCal)
                    sum1 = sum1 + sumGradeUnit
        print("แสดงค่า sum1 ก่อน",sum1)
        GPAX = sum1/sumUnit1
        #---- start แสดงทศนิยม2ตำแหน่ง---------#
        x = str(GPAX)
        # print(type(x))
        
        itemGPAX = ""
        for i in range(0,4):
            itemGPAX = itemGPAX + x[i]
        print(itemGPAX)
        #------ stop แสดงทศนิยม2ตำแหน่ง--------#

        
        # รับค่ามาแสดงเป็น json 
        if request.method == 'POST':
            student_id = request.form.getlist("student_id[]")
            subject_id = request.form.getlist("subject_id[]")
            subject_nameTh = request.form.getlist("subject_nameTh[]") #รับค่าเป็น list จากform index.html
            subject_nameEng = request.form.getlist("subject_nameEng[]")
            grade = request.form.getlist("grade[]")
            unit = request.form.getlist("unit[]")
            year = request.form.getlist("year[]")
            term = request.form.getlist("term[]")
        # ---------------------- start  ส่งค่าแล้วprintออกมาเป็นjson -------------------------
        headers = ('student_id','subject_id','subject_nameTh', 'subject_nameEng', 'grade','unit','year','term')
        values = (
            request.form.getlist("student_id[]"),
            request.form.getlist("subject_id[]"),
            request.form.getlist("subject_nameTh[]"), #รับค่าเป็น list จากform index.html
            request.form.getlist("subject_nameEng[]"),
            request.form.getlist("grade[]"),
            request.form.getlist("unit[]"),
            request.form.getlist("year[]"),
            request.form.getlist("term[]"),        
        )
        items = [{} for i in range(len(values[0]))]
        for x,i in enumerate(values):  #enumerate เป็นคำสั่งสำหรับแจกแจงค่า index และข้อมูลใน index ในรูปแบบทูเพิล (Tuple) ดังนี้ (Index,Value) โดยต้องใช้กับข้อมูลชนิด list
            # print(x,i)
            for _x,_i in enumerate(i): 
                items[_x][headers[x]] = _i
        result = jsonify(items)
        #print("---------------------------------------------------")
        # print(result)
        # print(items)
        
        # rows = json.dumps(items)
        rows=items
        # print(rows)
        #print("---------------------------------------------------")
        # -------------------- stop  ส่งค่าแล้วprintออกมาเป็นjson-----------------------

         #------------รับค่าามาจาก gradecal.html--------------
        if request.method == 'POST':
            grade = request.form.getlist('grade[]')
            unit = request.form.getlist('unit[]')
            # print("grade",grade)
            # print("unit",unit)
            # print(type(unit))
            print("***********************************************************************")
            print('หน่วยกิต:',unit)
            print('เกรด:',grade)
            print("***********************************************************************")

            #---------------------เช็ค W------------------------------------
            for i in range(len(grade)): #วนลูปเช็คว่ามี W ไหม
                # print(Grade[i])
                if (grade[i] == 'W') or (grade[i] == 'P') or (grade[i] == 'I') or (grade[i] == 'S') or (grade[i] == 'U') :
                    grade[i] = 0
                    for x in range(len(unit)): #วนหาหน่วยกิตที่ติด W
                        if x == i:
                            unit[x] = 0 #เปลี่ยนหน่วตกิตวิชาที่ติด W ให้มีค่าเป็น 0
                            
                else :
                    print(grade[i]) #เกรดที่นำมาคิด
                
        print("***********************************************************************")
        print('หน่วยกิต:',unit)
        print('เกรด:',grade)
        print("***********************************************************************")

        #------------------------------ start คำนวนเกรด gpax---------------------------------#
        sumUnit= 0
        for indexUnit in range(0,len(unit)):
            # print("หน่วยกิต ",unit[indexUnit])
            sumUnit = sumUnit + (float(unit[indexUnit]))
        print("sumUnit : ผลรวมหน่วยกิต",sumUnit)

        sum = 0
        for indexGrade in range(0,len(grade)):
            gradeCal = (tranformgrade(grade[indexGrade])) #เรียกใช้ฟังก์ชั่น tranformgrade แปลงเกรด ex. A=4.00 ,B=3.00 
            # print(gradeCal)
            # print(type(gradeCal))
            for indexUnit in range(0,len(unit)):
                unitCal = (unit[indexUnit])
                # print(type(unitCal))
                if indexGrade==indexUnit:
                    sumGradeUnit = float(gradeCal) * (float(unitCal))
                    sum = sum + sumGradeUnit
        # print(sum)
        X=sum1+sum
        Y=sumUnit1+sumUnit
        # GPA = sum/sumUnit
        GPA = X/Y
        #---- start แสดงทศนิยม2ตำแหน่ง---------#
        GPA = '%.4f'%(GPA) #ทำให้เป็นทศนิยม4ตำแหน่ง
        x = str(GPA)
        # print(type(x))
        
        itemGPAXAll = ""
        for i in range(0,4):
            itemGPAXAll = itemGPAXAll+ x[i]
        print("itemGPAXAll : เกรดเฉลี่ย",itemGPAXAll) #เกรดที่ได้จากการคำนวณรต่อเทอม
        # ------ stop แสดงทศนิยม2ตำแหน่ง--------#
        return render_template('gradecalShow.html',itemGPA=itemGPA,rows=rows,subject=subject,GPAX=itemGPAX,itemGPAXAll=itemGPAXAll)

    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT student_grade.student_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng ,student_grade.grade , student_grade.unit , student_grade.year, student_grade.term  FROM student_grade JOIN subject ON subject.subject_id = student_grade.subject_id WHERE student_id = '60020671' ") # ex. ดูว่ารหัสนิสิต 60023179 เรียนอะไรไปแล้วบ้าง
        subject=cur.fetchall()
        # print(subject)
        
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
        #---- start แสดงทศนิยม2ตำแหน่ง ---------#
        x = str(GPAX)
        # print(type(x))
        
        itemGPAX = ""
        for i in range(0,4):
            itemGPAX = itemGPAX + x[i]
        print(itemGPAX)
        #------ stop แสดงทศนิยม2ตำแหน่ง --------#
        #------------------------------ stop คำนวนเกรด gpax---------------------------------#
        
        #--------- แผนการเรียนที่จะนำมาคำนวณเกรด-----------#
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
            return render_template('gradecal.html',subject=subject,GPAX=itemGPAX,subjectCal=subjectCal)

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
            return render_template('gradecal.html',subject=subject,GPAX=itemGPAX,subjectCal=subjectCal)
    




# #--------------------ส่งค่าจาก gradecal.html มาคำนวณ-----------------------------------
# @app.route('/calculategrade',methods=['POST','GET'])
# def calculategrade():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT student_grade.student_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng ,student_grade.grade , student_grade.unit , student_grade.year, student_grade.term  FROM student_grade JOIN subject ON subject.subject_id = student_grade.subject_id WHERE student_id = '60020671'") # ex. ดูว่ารหัสนิสิต 60023179 เรียนอะไรไปแล้วบ้าง
#     subject=cur.fetchall()
#     # print(subject)
    
#     #------------------------------ start คำนวนเกรด gpax---------------------------------#
#     cur.execute("SELECT unit FROM student_grade WHERE student_id = '60020671' ")
#     unit = cur.fetchall()
#     sumUnit1 = 0 
#     for indexUnit in range(0,len(unit)):
#         unitCal = (unit[indexUnit]['unit'])
#         # print (float(unitcal))
#         sumUnit1 = sumUnit1 + float(unitCal) 
#     print("แสดงผลsumUnit1 ก่อน:",sumUnit1)

#     cur.execute("SELECT grade FROM student_grade WHERE student_id = '60020671' ")
#     grade = cur.fetchall()
#     #print(grade)
#     sum1 = 0
#     for indexGrade in range(0,len(grade)):
#         gradeCal = (tranformgrade(grade[indexGrade]['grade'])) #เรียกใช้ฟังก์ชั่น tranformgrade แปลงเกรด ex. A=4.00 ,B=3.00 
#         #print(float(gradeCal))
#         for indexUnit in range(0,len(unit)):
#             unitCal = (unit[indexUnit]['unit'])
#             if indexGrade==indexUnit:
#                 sumGradeUnit = float(gradeCal) * float(unitCal)
#                 sum1 = sum1 + sumGradeUnit
#     print("แสดงค่า sum1 ก่อน",sum1)
#     GPAX = sum1/sumUnit1
#     #---- start แสดงทศนิยม2ตำแหน่ง---------#
#     x = str(GPAX)
#     # print(type(x))
    
#     itemGPAX = ""
#     for i in range(0,4):
#         itemGPAX = itemGPAX + x[i]
#     print(itemGPAX)
#     #------ stop แสดงทศนิยม2ตำแหน่ง--------#

    
#     # รับค่ามาแสดงเป็น json 
#     if request.method == 'POST':
#         student_id = request.form.getlist("student_id[]")
#         subject_id = request.form.getlist("subject_id[]")
#         subject_nameTh = request.form.getlist("subject_nameTh[]") #รับค่าเป็น list จากform index.html
#         subject_nameEng = request.form.getlist("subject_nameEng[]")
#         grade = request.form.getlist("grade[]")
#         unit = request.form.getlist("unit[]")
#         year = request.form.getlist("year[]")
#         term = request.form.getlist("term[]")
#      # ---------------------- start  ส่งค่าแล้วprintออกมาเป็นjson -------------------------
#     headers = ('student_id','subject_id','subject_nameTh', 'subject_nameEng', 'grade','unit','year','term')
#     values = (
#         request.form.getlist("student_id[]"),
#         request.form.getlist("subject_id[]"),
#         request.form.getlist("subject_nameTh[]"), #รับค่าเป็น list จากform index.html
#         request.form.getlist("subject_nameEng[]"),
#         request.form.getlist("grade[]"),
#         request.form.getlist("unit[]"),
#         request.form.getlist("year[]"),
#         request.form.getlist("term[]"),        
#     )
#     items = [{} for i in range(len(values[0]))]
#     for x,i in enumerate(values):  #enumerate เป็นคำสั่งสำหรับแจกแจงค่า index และข้อมูลใน index ในรูปแบบทูเพิล (Tuple) ดังนี้ (Index,Value) โดยต้องใช้กับข้อมูลชนิด list
#         # print(x,i)
#         for _x,_i in enumerate(i): 
#             items[_x][headers[x]] = _i
#     result = jsonify(items)
#     #print("---------------------------------------------------")
#     # print(result)
#     # print(items)
    
#     # rows = json.dumps(items)
#     rows=items
#     # print(rows)
#     #print("---------------------------------------------------")
#     # -------------------- stop  ส่งค่าแล้วprintออกมาเป็นjson-----------------------

#         #------------รับค่าามาจาก gradecal.html--------------
#     if request.method == 'POST':
#         grade = request.form.getlist('grade[]')
#         unit = request.form.getlist('unit[]')
#         # print("grade",grade)
#         # print("unit",unit)
#         # print(type(unit))
#         print("***********************************************************************")
#         print('หน่วยกิต:',unit)
#         print('เกรด:',grade)
#         print("***********************************************************************")

#         #---------------------เช็ค W------------------------------------
#         for i in range(len(grade)): #วนลูปเช็คว่ามี W ไหม
#             # print(Grade[i])
#             if grade[i] == 'W':
#                 grade[i] = 0
#                 for x in range(len(unit)): #วนหาหน่วยกิตที่ติด W
#                     if x == i:
#                         unit[x] = 0 #เปลี่ยนหน่วตกิตวิชาที่ติด W ให้มีค่าเป็น 0
                        
#             else :
#                 print(grade[i]) #เกรดที่นำมาคิด
            
#     print("***********************************************************************")
#     print('หน่วยกิต:',unit)
#     print('เกรด:',grade)
#     print("***********************************************************************")

#     #------------------------------ start คำนวนเกรด gpax---------------------------------#
#     sumUnit= 0
#     for indexUnit in range(0,len(unit)):
#         # print("หน่วยกิต ",unit[indexUnit])
#         sumUnit = sumUnit + (float(unit[indexUnit]))
#     print("sumUnit : ผลรวมหน่วยกิต",sumUnit)

#     sum = 0
#     for indexGrade in range(0,len(grade)):
#         gradeCal = (tranformgrade(grade[indexGrade])) #เรียกใช้ฟังก์ชั่น tranformgrade แปลงเกรด ex. A=4.00 ,B=3.00 
#         # print(gradeCal)
#         # print(type(gradeCal))
#         for indexUnit in range(0,len(unit)):
#             unitCal = (unit[indexUnit])
#             # print(type(unitCal))
#             if indexGrade==indexUnit:
#                 sumGradeUnit = float(gradeCal) * (float(unitCal))
#                 sum = sum + sumGradeUnit
#     # print(sum)
#     X=sum1+sum
#     Y=sumUnit1+sumUnit
#     # GPA = sum/sumUnit
#     GPA = X/Y
#     #---- start แสดงทศนิยม2ตำแหน่ง---------#
#     GPA = '%.4f'%(GPA) #ทำให้เป็นทศนิยม4ตำแหน่ง
#     x = str(GPA)
#     # print(type(x))
    
#     itemGPAXAll = ""
#     for i in range(0,4):
#         itemGPAXAll = itemGPAXAll+ x[i]
#     print("itemGPAXAll : เกรดเฉลี่ย",itemGPAXAll) #เกรดที่ได้จากการคำนวณรต่อเทอม
#     # ------ stop แสดงทศนิยม2ตำแหน่ง--------#
        
#     return render_template('gradecalShow.html',rows=rows,subject=subject,GPAX=itemGPAX,itemGPAXAll=itemGPAXAll)
#     # return redirect(url_for('gradecal',itemGPAX=itemGPAX))





@app.route('/gradegpa')
def gradegpa():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT student_grade.student_id , subject.subject_id , subject.subject_nameTh , subject.subject_nameEng ,student_grade.grade , student_grade.unit , student_grade.year, student_grade.term  FROM student_grade JOIN subject ON subject.subject_id = student_grade.subject_id WHERE student_id = '60020671' and year='1' and term='1' ")
    data = cur.fetchall()
        #------------------------------ start คำนวนเกรด gpax---------------------------------#
    cur.execute("SELECT unit FROM student_grade WHERE student_id = '60020671' and year='1' and term='1' ")
    unit = cur.fetchall()
    sumUnit = 0 
    for indexUnit in range(0,len(unit)):
        unitCal = (unit[indexUnit]['unit'])
        # print (float(unitcal))
        sumUnit = sumUnit + float(unitCal) 
    # print(sumnUit)

    cur.execute("SELECT grade FROM student_grade WHERE student_id = '60020671' and year='1' and term='1' ")
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
    
    return render_template('gradegpa.html',data=data,gpa=itemGPAX)









  
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

#--------------------------ค้นหาแผนการศึกษา------------------------------
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


#---------------------ปฏิทินการศึกษา----------------------------------------
@app.route("/calendar")
def  calendar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT topic.topic_name, calendar.term ,calendar.date_start, calendar.date_stop,calendar.year FROM topic INNER JOIN calendar ON topic.topic_id = calendar.topic_id ORDER BY calendar.term")
    data = cur.fetchall()
    return render_template('calendar.html',data=data)
    

if __name__== "__main__" :
    app.run(debug=True)