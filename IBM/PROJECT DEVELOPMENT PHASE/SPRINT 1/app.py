from flask import Flask, render_template, request,session,flash,url_for,redirect,g,send_from_directory

import os


app = Flask(__name__)
app.secret_key = "123"

class User:
    def __init__(self,id,username,email,password):
        self.id=id
        self.username=username
        self.email=email
        self.password=password

users=[]
users.append(User(id=1,username="Ram",email="ram@2014",password="1234"))
users.append(User(id=2,username="Aravindh",email="aravindh@2014",password="aravindh@2014"))




@app.route("/Login")
def Login():
    return render_template('login.html')

@app.route("/Login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        email=request.form["email"]
        password=request.form["password"]

        for data in users:
            if data.email == email and data.password==password:
                session['userid']=data.id
                g.record=1
                return redirect(url_for("dashboard"))
            else:
                g.record=0
        if g.record != 1 :
            flash("Username or Password Mismatching...!!!","danger")
            return redirect(url_for('Login'))
    return render_template("login.html")

@app.before_request
def before_request():
    if "userid" in session:
        for data in users:
            if data.id == session["userid"]:
                g.user=data

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/forgot_password")
def forgot_password():
    return render_template('forgot-password.html')

@app.route("/dashboard")
def dashboard():
    if not g.user :
        return redirect(url_for('Login'))
    return render_template('dashboard.html')



if __name__ == "__main__" :
    app.run()