from flask import Flask,render_template,redirect,url_for,request,flash,get_flashed_messages
from form import Regis_form,login_form,veri_form,add,up_form
from flask_login import LoginManager,UserMixin,login_required,login_user,logout_user
from twilio.rest import Client
import secrets
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError,InvalidRequestError
from random import randint
from datetime import datetime
import time
from datetime  import date
from flask_mail import Mail,Message
from flask_bcrypt import Bcrypt


account_sid="************************"
auth_token="@@@@@@@@@@@@@@@@@@@@@@@"

client = Client(account_sid,auth_token)

from_whatsapp_number='whatsapp:+14155238886'           #+14155238886

to_whatsapp_number='whatsapp:0000000000'



app=Flask(__name__)


app.config['SECRET_KEY']="00b70837bacb0419eec283e85a1d4810"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data_new.db'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']="**********@gmail.com"
app.config['MAIL_PASSWORD']="***************"
app.config['MAIL_USE_TSL']=False
app.config['MAIL_USE_SSL']=True

db=SQLAlchemy(app)
login_manager=LoginManager(app)
mail=Mail(app)
bcrypt=Bcrypt(app)



class source(db.Model):
     id=db.Column(db.Integer,primary_key=True)
     otp=db.Column(db.Integer,unique=True,nullable=False)
     #email = db.Column(db.String(120),unique=True,nullable=False)
     def __repr__(self):
          return f"otp('{self.otp}')"

class regis(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    phone=db.Column(db.String(10),nullable=False,unique=True)
    #whats=db.Column(db.String(10),nullable=False,unique=True)

    def __repr__(self):
       return f"regis('{self.user_name}','{self.email}')"


class logged(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(20),unique=True,nullable=False)

    def __repr__(self):
       return f"logged('{self.user_name}')"


class sendotps(db.Model):
         id=db.Column(db.Integer,primary_key=True)
         otp=db.Column(db.Integer,nullable=False)
         email = db.Column(db.String(120),unique=True,nullable=False)

         def __repr__(self):
              return f"sendotps('{self.otp}','{self.email}')"



class medicines(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(120),nullable=False)
    med=db.Column(db.String(120),nullable=False)
    time=db.Column(db.String(8),nullable=False)
    exp=db.Column(db.String(8),nullable=False)

    def __repr__(self):
        return f"medicines('{self.user_name}','{self.med}','{self.time}','{self.exp}')"




class verified(db.Model):
     id=db.Column(db.Integer,primary_key=True)
     email=db.Column(db.String(120),unique=True,nullable=False)

     def __repr__(self):
          return f"verified('{self.email}')"





@login_manager.user_loader
def load_user(user_id):
    return regis.query.get(int(user_id))


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/register",methods=['GET','POST'])
def register():
    form=Regis_form()
    if form.validate_on_submit():
           print("valid")
           user=request.form.get('username')
           pas=request.form.get('password')
           val=bcrypt.generate_password_hash(pas).decode('utf-8')
           print(val)
           bcrypt.check_password_hash(val,pas)
           email=request.form.get('email')
           phone=request.form.get('phone_no')

           um=regis(user_name=user,password=pas,email=email,phone=phone)
           db.session.add(um)
           try:
               db.session.commit()
               return redirect(url_for('verification',phone=phone))
           except(IntegrityError,InvalidRequestError):
               error="username/email already exists"
               return render_template("register.html",form=form,error=error)

           return redirect(url_for('verification',phone=phone))
    return render_template("register.html",form=form)



@app.route("/login",methods=['GET','POST'])
def login():
    form=login_form()
    if form.validate_on_submit():
        name=request.form.get('username')
        pas=request.form.get('password')
        user=regis.query.filter_by(user_name=name).first()
        if(user==None):
            error="invalid login"
            return render_template("login.html",form=form,error=error)
        else:
            if(pas==user.password):
                 m=logged(user_name=name)
                 db.session.add(m)
                 try:
                     db.session.commit()
                     print(logged.query.all())
                     return redirect(url_for('dashboard',username=name))
                 except(IntegrityError):
                     return redirect(url_for('dashboard',username=name))
            else:
                error ='Invalid login !!!!'
                return render_template("login.html",form=form,error=error)

    return render_template("login.html",form=form)




@app.route("/verification/<phone>",methods=['GET','POST'])
def verification(phone):
        form=veri_form()

        if form.validate_on_submit():
            print("valid")
            us=source.query.filter_by(id=1).first()
            ot=request.form.get('otp')
            print('otp from form=',us.otp)
            #print(type(int(otp)))
            #print(type(us.otp))

            if(int(ot)==us.otp):
                db.session.delete(us)
                db.session.commit()
                print(source.query.all())
                l=regis.query.filter_by(phone=phone).first()
                print(l.user_name)
                return redirect(url_for('dashboard',username=l.user_name))

            else:
                error='invalid otp '
                #link= 'http://127.0.0.1:5000/verification/<phone>'
                m=source.query.filter_by(id=1).first()
                if(m!=None):
                    db.session.delete(m)
                    db.session.commit()
                return render_template('verification.html',form=form,phone=phone,error=error,link=link)

        else:
            us=source.query.filter_by(id=1).first()
            if(us==None):
                m=randint(1000,9999)
                client.messages.create(body='your otp is \n'+ str(m),
                                from_=from_whatsapp_number,
                                 to=to_whatsapp_number)
                print("message sent")

                print("form not validate yet..")
                u=source(otp=m)
                db.session.add(u)
                db.session.commit()
                print(m)
                print("added value")


            return render_template('verification.html',form=form,phone=phone)


@app.route("/added/<username>",methods=["GET","POST"])
def added(username):
    form= add()
    if form.validate_on_submit():
        username=request.form.get('username')
        medi=request.form.get('medicine')
        tim=request.form.get('time')
        ex=request.form.get('exp_date')
        user=medicines(user_name=username,med=medi,time=tim,exp=ex)
        db.session.add(user)
        print('here')
        try:
            db.session.commit()
            print("here")
            return redirect(url_for('dashboard',username=username))
        except(IntegrityError):
            error="already added medicine"
            return render_template('add.html',username=username,form=form,error=error)
    return render_template('add.html',username=username,form=form)





@app.route("/verify/<em>")
def verify(em):
    user=regis.query.filter_by(email=em).first()
    print(user)
    m=randint(1000,9999)
    u=sendotp(otp=m,email=em)
    db.session.add(u)
    try:
        db.session.commit()
        msg = Message('Verify', sender = 'pycoders3501@gmail.com', recipients = [em])
        msg.body='hey there.. this email was sent by medrem  ...enter the otp on the  ' + str(m)
        mail.send(msg)
        print("mail sent")
        flash("enter the otp")
        print(sendotp.query.all())
        return redirect(url_for('emsuccess',em=em))
    except(IntegrityError):
        return "email already verified"







@app.route("/dashboard/<username>")
def dashboard(username):
    #taking sample data for testing
     user=logged.query.filter_by(user_name=username).first()
     print(user)
     if(user==None):
         return(redirect(url_for('login')))
     else:
         today=date.today()
         k=today.strftime("%m/%Y")
         m=datetime.now().strftime("%H:%M")
         print(m,type(m))
         us=regis.query.filter_by(user_name=username).first()
         em=us.email
         print(em)
         values=medicines.query.all()
         for value in values:
             print(value.med)
             print(value.time,type(value.time))
             print(value.exp)
             if m==value.time:
                 return redirect(url_for('call',username=username))
             if  k==value.exp:
                     msg = Message('Attention', sender = 'pycoders3501@gmail.com', recipients = [em])
                     msg.body='hey there.. this email was sent by medrem  to remind you ....\n your medicine'+value.med+'expires on'+value.exp
                     mail.send(msg)
                     print("mail sent")
                     db.session.query(medicines).filter_by(user_name=username).update({'exp':'None'})
                     db.session.commit()



         #flash("one more step to continue... verify your email by clicking on link below..")

         return render_template("dashboard.html",em=em,username=username,medicines=medicines)




@app.route("/call/<username>")
def call(username):
    call =    client.calls.create(
                        method='GET',
                        #status_callback='http://httpstat.us/204/success',
                        #status_callback_event=['initiated', 'answered'],
                        #status_callback_method='POST',
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+918360581227',
                        from_='+918360581227'
                        #status=request.values.get('CallStatus',None)
                    )


    return redirect(url_for('notconnected',username=username))








@app.route("/notconnected/<username>")
def notconnected(username):

    u=regis.query.filter_by(user_name=username).first()
    m=u.phone
    print("messaging on whatsapp")
    client.messages.create(body='hey..' + username +' its your medicine time!!!',
                            from_=from_whatsapp_number,
                             to=to_whatsapp_number)
    print("message sent")
    time.sleep(60)
    return redirect(url_for('dashboard',username=username))



@app.route("/emsuccess/<em>",methods=['GET','POST'])
def emsuccess(em):
    form=veri_form()
    m=sendotp.query.filter_by(email=em).first()
    print(m)

    if form.validate_on_submit():
        otp=request.form.get('otp')
        m=sendotps.query.filter_by(email=em).first()
        print(type(m.otp))
        print(type(otp))

        if(m.otp==int(otp)):
            q=verified(email=em)
            db.session.add(q)
            db.session.commit()
            print("verified")
            return "email verified successfully"
        else:
            error="invalid otp"
            return render_template('emverify.html',error=error,form=form)
    return render_template('emverify.html',form=form)


@app.route("/delete/<med>")
def delete(med):
    user=medicines.query.filter_by(med=med).first()
    m=user.user_name
    print(m)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('dashboard',username=m))






@app.route("/logout/<username>")
def logout(username):
    logout_user()
    m=logged.query.filter_by(user_name=username).first()
    db.session.delete(m)
    db.session.commit()
    print(logged.query.all())
    return redirect(url_for("index"))



@app.route("/update/<username>",methods=['GET','POST'])
def update(username):
    form=up_form()
    if form.validate_on_submit():
        user=regis.query.filter_by(user_name=username).first()
        pas=request.form.get('password')
        if(pas==user.password):
            phone=request.form.get('phone_no')

            db.session.query(regis).filter_by(user_name=username).update({'phone':phone})
            #db.session.query(regis).filter_by(user_name=username).update({'whats':whas})
            try:
                db.session.commit()
            except(IntegrityError):
               return redirect(url_for('dashboard',username=username))

            return redirect(url_for('dashboard',username=username))
        else:
            error="invalid password"
            return render_template('update.html',username=username,error=error,form=form)

    return render_template('update.html',username=username,form=form)



@app.errorhandler(404)

def not_found(e):

# defining function
  return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True)
