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




mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/calendar")
def  calendar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT topic.topic_name, calendar.term ,calendar.date_start, calendar.date_stop,calendar.year FROM topic INNER JOIN calendar ON topic.topic_id = calendar.topic_id ORDER BY calendar.term")
    data = cur.fetchall()
    return render_template('calendar-mobile.html',data=data)
    

if __name__== "__main__" :
    app.run(debug=True)