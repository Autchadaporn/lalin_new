from flask import Flask, render_template, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired 

@app.route('/')
def index():
    return render_template('test1.html')

if __name__== "__main__" :
    app.run(debug=True)