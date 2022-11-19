from flask import Flask, render_template, request,session,flash,url_for,redirect,g,send_from_directory

import os
import requests
import numpy as np
import urllib
import urllib.request
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img , img_to_array
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = "123"

class User:
    def __init__(self,id,username,email,password):
        self.id=id
        self.username=username
        self.email=email
        self.password=password

users=[]
users.append(User(id=1,username="Aravindh",email="aravindh@2014",
                  password="aravindh@2014"))

model = load_model('nutrition.h5')

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

labels = {0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot', 7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger', 14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce',
          19: 'mango', 20: 'onion', 21: 'orange', 22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple', 26: 'pomegranate', 27: 'potato', 28: 'raddish', 29: 'soy beans', 30: 'spinach', 31: 'sweetcorn', 32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'}

fruits = ['Apple','Banana','Bello Pepper','Chilli Pepper','Grapes','Jalepeno','Kiwi','Lemon','Mango','Orange','Paprika','Pear','Pineapple','Pomegranate','Watermelon']
vegetables = ['Beetroot','Cabbage','Capsicum','Carrot','Cauliflower','Corn','Cucumber','Eggplant','Ginger','Lettuce','Onion','Peas','Potato','Raddish','Soy Beans','Spinach','Sweetcorn','Sweetpotato','Tomato','Turnip']


def fetch_calories(prediction):
        calories = { 'Apple' : 52 ,  'Banana' : 87, 'Beetroot' : 60,  'Bell Pepper' : 40, 'Cabbage' : 25, 'Capsicum' : 40 ,  'Carrot' : 41,  'Cauliflower' : 25,  'Chilli Pepper' : 40, 'Corn' : 86,  'Cucumber' : 30, 'Eggplant' : 20,  'Garlic' : 13,  'Ginger' : 41,  'Grapes' : 67, 'Jalepeno' : 28, 'Kiwi' : 61,  'Lemon' : 29,  'Lettuce' : 15,
           'Mango' : 60, 'Onion' : 40, 'Orange' : 47, 'Paprika' : 282,'Pear' : 57, 'Peas' : 81,  'Pineapple' : 50,  'Pomegranate' : 234,  'Potato' : 77, 'Raddish' : 16, 'Soy Beans' : 39, 'Spinach' : 23, 'Sweetcorn' : 86,  'Sweetpotato' : 86, 'Tomato' : 18, 'Turnip' : 28, 'Watermelon' : 30}
        calorie = calories[prediction]
        return calorie

def fetch_inform(prediction):
        a=[]
        url = 'https://en.wikipedia.org/wiki/' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        # getting all the paragraphs
        for para in scrap.find_all("p"):
            text=para.get_text()
            a.append(text)
        answer = " "
        answer = answer.join(a)
        return answer

  
def processed_img(img_path):
    img=load_img(img_path,target_size=(224,224,3))
    img=img_to_array(img)
    img=img/255
    img=np.expand_dims(img,[0])
    answer=model.predict(img)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    print(res)
    return res.capitalize()

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

@app.route("/bmi")
def bmi():
    return render_template('bmi.html')

@app.route("/bmr")
def bmr():
    return render_template('bmr.html')

@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

@app.route('/prediction', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        flash('No file part',"danger")
        return redirect(request.url)
    image = request.files["image"]
    if image.filename == '':
        flash('No image selected for uploading',"danger")
        return redirect(request.url)
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        file_path=os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
        image.save(file_path)
        prediction = processed_img(file_path)
        if prediction in vegetables:
            category='Vegetables'
        else:
            category='Fruits'
        
        calories = fetch_calories(prediction)
        inform=fetch_inform(prediction)

        flash('Image successfully uploaded and displayed below','success')
        return render_template("prediction.html", uploaded_image=image.filename,filename=filename,prediction = prediction,calories=calories,category=category,inform=inform)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif',"danger")
        return redirect(request.url)

@app.route('/uploads/<filename>')
def send_uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route('/diet_tracker')
def diet_tracker():
    return render_template('diet.html')

@app.route('/diet_tracker', methods=['POST'])
def diet_tracker_calucation():
        if request.method == "POST":
            breakfast=request.form["breakfast"]
            lunch=request.form["lunch"]
            dinner=request.form["dinner"]
            exercise=request.form["exercise"]
            bmr=request.form["bmr"]

            fitness = int(bmr) + int(exercise) - (int(breakfast) + int(lunch) + int(dinner))

            weekly_deficit = 7 * fitness

            if weekly_deficit > 0 :
                ans = round((weekly_deficit /3600),3)
                result = 'You will lose ' + str(ans) + ' lbs. per week'
            elif weekly_deficit == 0 :
                result = 'Your Weight will stay the same ' 
            else:
                ans = round((-1* weekly_deficit /3600),3)
                result = 'You will gain ' + str(ans) + ' lbs. per week' 
        return render_template('diet.html',result=result)        

if __name__ == "__main__" :
    app.run()