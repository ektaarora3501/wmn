from flask import Flask
from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,ValidationError,validators,PasswordField,SubmitField
from wtforms.validators import DataRequired,EqualTo,Length,Email
#from main.models import data_user


class Regis_form(FlaskForm):
    fullname=StringField('Full name',validators=[DataRequired(),Length(min=4,max=50)])
    username=StringField('Username',validators=[DataRequired(),Length(min=4,max=20)])
    password=PasswordField('Passward',validators=[DataRequired(),Length(min=5,max=9)])
    cnf_pass=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    email=StringField("Email",validators=[DataRequired(),Email()])
    phone_no=StringField("Phone no.",validators=[DataRequired(),Length(min=10,max=10)])
    whatsapp=StringField("Whatsapp N0",validators=[DataRequired(),Length(min=10,max=10)])
    submit=SubmitField('Sign Up')




class login_form(FlaskForm):
        username=StringField('Username',validators=[DataRequired(),Length(min=4,max=20)])
        password=PasswordField('Password',validators=[DataRequired(),Length(min=5,max=9)])
        submit=SubmitField('Sign In')

class veri_form(FlaskForm):
        otp=StringField('otp',validators=[DataRequired(),Length(min=4,max=4)])
        submit=SubmitField('Verify')


class add(FlaskForm):
        username=StringField('Username',validators=[DataRequired(),Length(min=4,max=20)])
        medicine=StringField('Medicine name',validators=[DataRequired(),Length(min=4,max=50)])
        time=StringField('Time of taking (in hr:min format.)',validators=[DataRequired(),Length(min=4,max=8)])
        exp_date=StringField('Expiry of medicine in MM/YYYY',validators=[DataRequired(),Length(min=4,max=8)])
        submit=SubmitField('Add medicine')


class up_form(FlaskForm):
        password=PasswordField('Password',validators=[DataRequired(),Length(min=5,max=9)])
        phone_no=StringField("Phone no.",validators=[DataRequired(),Length(min=10,max=10)])
        whatsapp=StringField("Whatsapp N0",validators=[DataRequired(),Length(min=10,max=10)])

        submit=SubmitField('update')
