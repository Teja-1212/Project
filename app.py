from flask import Flask, app, request, render_template,redirect,url_for,session
import mysql.connector
import re
import numpy as np
import os
from tensorflow.keras import models
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.python.ops.gen_array_ops import concat
from tensorflow.keras.applications.inception_v3 import preprocess_input
import requests
from werkzeug.utils import secure_filename

model1 = load_model('level.h5')
model2 = load_model('body.h5')

app=Flask(__name__)
app.secret_key = 'cskmnt1'

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'ai',
}

# default home page or route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home')
def home2():
    return render_template('home.html')


# registration page
@app.route('/register', methods=["GET","POST"])
def registration():
    return render_template('register.html')

# registration page
# @app.route('/register_new')
# def register_new():
#     return render_template('login.html')
    # Your view function logic here

# @app.route('/register')
# def register():
#     return render_template('register.html')

@app.route('/afterreg', methods=['POST'])
def afterreg():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        con = mysql.connector.connect(host="localhost",user="root",password="root",database="ai")
        cur = con.cursor()
        query = "INSERT INTO users (email, password) VALUES (%s, %s)"
        cur.execute(query, (email, password))
        con.commit()
        cur.close()
        con.close()
        return redirect(url_for('login'))
    return render_template("register.html")


@app.route('/login', methods=["GET","POST"])
def login():
     return render_template('login.html')


@app.route('/afterlogin', methods=['POST'])
def afterlogin():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        print(email)
        print(password)
        con = mysql.connector.connect(host="localhost",user="root",password="root",database="ai")
        cur=con.cursor()
        cur.execute("select * from users")
        for x in cur:
                if(x[0]==email):
                        if(x[1]==password):
                                print("user found")
                                return redirect(url_for('prediction'))
                        else:
                                print("Enter valid Password")
                else:
                        print("Email id does not matched")
		
    return render_template("login.html")

@app.route('/prediction', methods=["GET","POST"] )
def prediction():
    return render_template('predict.html')


@app.route('/predict', methods=["GET","POST"])
def predict():
    if request.method=="POST":
        f=request.files['image']
        basepath=os.path.dirname(__file__)  #getting the current path i.e where app.py is present
        # print("current path",basepath)
        filepath=os.path.join(basepath,'uploads',f.filename) # from anywhere in the system we can give image
        # print("upload folder is ",filepath)
        f.save(filepath)


        img=image.load_img(filepath,target_size=(224,224))
        x=image.img_to_array(img) #img to array
        x=np.expand_dims(x,axis=0) #used for adding one more dimension
        print(x)
        img_data=preprocess_input(x)
        prediction1=np.argmax(model1.predict(img_data))
        prediction2=np.argmax(model2.predict(img_data))

        #prediction=model.predict(x) #instead of predict_classes(x) we can use predict(x)  ------>predict_classes
        #print("prediction is",prediction)
        index1=['front', 'rear', 'side']
        index2=['minor', 'moderate', 'severe']
        #result = str(index[output[0]])
        result1 = index1[prediction1]
        result2 = index2[prediction2]
        if(result1 == "front" and result2 == "minor"):
            value = "3000 - 5000 INR"
        elif(result1 == "front" and result2 == "moderate"):
            value = "6000 - 8000 INR"
        elif(result1 == "front" and result2 == "severe"):
            value = "9000 - 11000 INR"
        elif(result1 == "rear" and result2 == "minor"):
            value = "4000 - 6000 INR"
        elif(result1 == "rear" and result2 == "moderate"):
            value = "7000 - 9000 INR"
        elif(result1 == "rear" and result2 == "severe"):
            value = "11000 - 13000 INR"
        elif(result1 == "side" and result2 == "minor"):
            value = "11000 - 13000 INR"
        elif(result1 == "side" and result2 == "moderate"):
            value = "9000 - 11000 INR"
        elif(result1 == "side" and result2 == "severe"):
            value = "11000 - 120000 INR"
        else:
            value = "16000 - 50000 INR"  
        value = 'The predicted output is {}' .format(str(value)) 
        return render_template('predict.html', prediction=value)

@app.route('/logout', methods=["GET","POST"] )
def logout():
    return render_template('logout.html')
    
"""Running our application"""
if __name__ == "__main__":
    app.run(debug = True)
