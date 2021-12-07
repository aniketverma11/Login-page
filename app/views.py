from app import app
from flask import render_template,request,redirect, url_for, redirect
from app import search
import re

passreg="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
emailreg="^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"


@app.route("/")
def home():
    return render_template("login.html")

@app.route("/form_login", methods=["GET","POST"])
def login():
    
    msg = ''
    if request.method == 'POST' and 'u_email' in request.form and 'u_pass' in request.form:
        usr = request.form["u_email"]
        pwd = request.form["u_pass"]
        res = search.search(usr, pwd)
        res2 = search.search_phone(usr,pwd)
        if not re.match(passreg, pwd):
            msg = 'Warning! Password must contain only characters and numbers !'
        elif not re.match(emailreg, usr):
            msg = 'Warning! Invalid email address !'  

        if res or res2:
            return render_template('index.html', msg=usr)
        else:
            msg="user not found"

    else:
        return render_template('index.html', msg=msg)
             

    



@app.route("/form")
def register():
    return render_template("form.html", name="Registration Form")

@app.route("/register_auth", methods=["GET", "POST"])
def register_auth():

    if request.method == 'POST' and 'u_phone' in request.form and 'u_email' in request.form and 'u_pass' in request.form :    
        name = request.form["u_name"]
        phone = request.form["u_phone"]
        email = request.form["u_email"]
        password = request.form["u_pass"]
        index = "userdata"
        if not re.match(emailreg, email):
            msg = 'Warning! Invalid email address !'
        elif len(phone)!=10:
            msg='Warning! Please Provide Full Length of Phone number'
        elif not re.match(passreg, password):
            msg = 'Warning! Password must contain alphanumeric with special characters !'
        elif not phone or not password or not email:
            msg = 'Warning! Please fill out the form !'
        #elif search.search(email,password):
         #   msg = 'user exist already'

        
        else :
            search.insert(index,name,email,phone,password)
            msg='Registered Succesfully! Back to Login!'
            print("values inserted")
            
            
    else:
        msg='Please fill out the form !'      
    return render_template("form.html", msg=msg)

@app.route('/update_email')
def email_updation_form():
    return render_template('update_email.html')
@app.route("/update_email", methods=['GET', 'POST'])
def update_email():
    if request.method == 'POST' and 'u_email' in request.form and 'u_pass' in request.form and 'u_email' in request.form :    
        name = request.form["c_email"]
        phone = request.form["u_phone"]
        email = request.form["u_email"]
        password = request.form["u_pass"]
        index = "userdata"
        
        if len(phone)!=10:
            msg='Warning! Please Provide Full Length of Phone number'
        elif not re.match(passreg, password):
            msg = 'Warning! Password must contain only characters and numbers !'
        elif not phone or not password or not email:
            msg = 'Warning! Please fill out the form !'

        else:
            if not re.match(emailreg, email):
                msg = 'Warning! Invalid email address !'
            elif search.search_phone(phone, password):
                search.update_email(phone,password, email)
                msg = "Email update succesfully, back to login"
            else:
                msg="User Not Found. can't update email!"

    else:
        msg="Don't Sign up!"
    return render_template("update_email.html", msg=msg)


@app.route('/update_phone')
def phone_updation_form():
    return render_template('update_phone.html')
@app.route("/update_phone", methods=['GET', 'POST'])
def update_phone():
    if request.method == 'POST' and 'u_email' in request.form and 'u_pass' in request.form and 'u_email' in request.form :    
        name = request.form["c_phone"]
        phone = request.form["u_phone"]
        email = request.form["u_email"]
        password = request.form["u_pass"]
        index = "userdata"
        if not re.match(emailreg, email):
            msg = 'Warning! Invalid email address !'
        elif not re.match(passreg, password):
            msg = 'Warning! Password must contain only characters and numbers !'
        elif not phone or not password or not email:
            msg = 'Warning! Please fill out the form !'

        else:

            if len(phone)!=10:
                msg='Warning! Please Provide Full Length of Phone number'
            elif search.search(email, password):
                res=search.update_phone(email,password,phone)
                msg = "Phone Number update succesfully, back to login"
            else:
                msg="wrong credentials. can't update phone!"

    else:
        msg="wrong entity"
    return render_template("update_phone.html", msg=msg)

    
    


            
            

        