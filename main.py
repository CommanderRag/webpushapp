from flask import Flask, render_template, request, json, jsonify, flash, send_from_directory
from flask_pymongo import MongoClient
import urllib
from werkzeug.utils import secure_filename
import os
import datetime
import requests
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
import random
#client =OneSignal(app_id="6844009f-6ec9-481f-a425-0f9da3d85c75",rest_api_key="YTc2OGQzMWItMDI2ZC00NmQ4LWJjN2EtY2NkM2FjYmRiZmMz")


def true():
    number=request.get_json(force=True)
    data = number['number']
    message = "Episode {} is out now!".format(data) 
    print(message)
    request_header = {
        'Content-Type' : 'application/json'
    }
    dict_to_send = {
        'title' : 'Notification',
        'body' : message,
    }
    req = requests.post("https://mywebpushapp.herokuapp.com/triggerPushNotifications", headers=request_header, json=dict_to_send)
    print(req.status_code, req.reason)


def false():
    number=request.get_json(force=True)
    data = number['number']
    message = "Episode {} is not out yet!".format(data) 
    print(message)
    request_header = {
        'Content-Type' : 'application/json'
    }
    dict_to_send = {
        'title' : 'Notification',
        'body' : message,
    }
    req = requests.post("https://mywebpushapp.herokuapp.com/triggerPushNotifications", headers=request_header, json=dict_to_send)
    print(req.status_code, req.reason)



app=Flask(__name__, instance_relative_config=True)

UPLOAD_FOLDER='keep'

app.secret_key=b'ooolalalahwallahmullahhohohoh%^&*()'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_pyfile('secrets.cfg.py')

mongo_uri = "mongodb+srv://admin:" + urllib.parse.quote("a@777security") + "@webservice.btgcm.mongodb.net/Users?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)

directory="keep"
path=os.path.join(app.root_path,directory)


ALLOWED_EXTENSIONS={'apk'}

from webpush_handler import trigger_push_notifications_for_subscriptions


@app.route('/',methods=['GET','POST'])
def work():
    return render_template('index.html')



@app.route('/true',methods=['GET','POST'])
def out():
    if request.method == 'POST':
        true()

    return render_template('invalid.html')

@app.route('/false',methods=['GET','POST'])
def not_out():
    if request.method == 'POST':
        false()    
    return render_template('invalid.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')



@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        retype = request.form['retype']
        if len(username) == 0 and len(password) == 0 or len(username) ==0 or len(password) ==0:
            flash('Username or Password field cannot be empty!')
        elif password != retype:
            flash('Passwords do not match!')
        else:
            try:
                with sqlite3.connect('test.db') as con:
                    cur = con.cursor()
                    cur.execute('SELECT * FROM records WHERE Username = ? AND Password = ? ',(username,password))
                    c= cur.fetchone()
                    a = c is not None
                    if a is True:
                        flash('Account already exists!')
                    else:
                        cur.execute('INSERT INTO records (Username, Password) VALUES(?,?)', (username, password))
                        con.commit()
                        flash('Signup successfull!')
            except:
                con.rollback()
                flash('Failed to signup!')
                #flash('Create database to store records first u dumb')
                con.close()
            finally:
                con.close()
    return render_template('signup.html')


@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global username, password
        username = request.form['username']
        password = request.form['password']
        if len(username) == 0 and len(password) == 0 or len(username) == 0 or len(password) == 0:
            flash('Username or Password field cannot be empty!')
        else:
            try:
                with sqlite3.connect('test.db') as con:
                    cur = con.cursor()
                    cur.execute('SELECT * FROM records WHERE Username = ? AND Password = ? ',(username,password))
                    c= cur.fetchone()
                   
                    a = c is not None
                    if a is True:
                        username = cur.execute('SELECT * FROM records WHERE Username = ?', [username])
                        username = cur.fetchone()
                        username =  username[0]
                        flash('Login successful!')
                        flash('Redirecting..')
                        return render_template('show_user.html',data=username)
                    else:
                        flash('Account does not exist.')
            except Exception as e:
                print(e)
                #con.rollback()
                flash('Error connecting to database...')
            finally:
                con.close()
    return render_template('login.html')


@app.route('/delete',methods=['POST'])
def delete():
    try:
        with sqlite3.connect('test.db') as con:
            cur = con.cursor()
            cur.execute('DELETE FROM records WHERE Username=? AND Password = ?',(username,password))
    except Exception as e:
        print(e)
    finally:
        con.close()
    return 'deleted'

hourss = random.randint(6,23)
minutess = random.randint(0,60)
scheduler = BackgroundScheduler(timezone="Asia/Calcutta")


@app.route('/list',methods=['GET','POST'])
def list_show():
    con = sqlite3.connect("test.db")
    con.row_factory = sqlite3.Row
   
    cur = con.cursor()
    cur.execute("select * from records")
   
    rows = cur.fetchall()
    return render_template("list.html",rows = rows)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload',methods=['POST'])
def upload_file():
    version_header=(dict(request.headers))

    #version=version_header.get('Version',"not found!")
    #str(version)

    if 'file' not in request.files:
        return 'Error'
    file = request.files['file']

    if file.filename=='':
        return 'Error' 
    
    if file and allowed_file(file.filename):
        with open('version.txt','w+') as write:
            value = version_header.get('Version')
            print(write.write(value))
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path,'keep',filename))
            print(os.path.join(app.config['UPLOAD_FOLDER']))        
            return '\n saved successfully'
    else:
        return 'Extension not allowed'


@app.route('/registerSubscriptions', methods=['POST'])
def registerSubscriptions():
    json_data = request.get_json(force=True)
    db = client['Users']
    column = db['tokens']

    print(json_data)
    print("\n")

    first = column.find_one({"endpoint": json_data['endpoint']})
    if first is None:
        print("Inserting Data!")
        column.insert_one({"subscription_json" : json_data})
    else:
        print("Service Worker already registered!")    

    return jsonify({
        'status' : 200,
        'result' : 'success'
    })

from webpush_handler import trigger_push_notifications_for_subscriptions
@app.route('/triggerPushNotifications', methods=['POST'])
def triggerPushNotifications():
    json_data = request.get_json(force=True)
    print(str(json_data))
    db = client['Users']
    column = db['tokens']

    subscriptions = column.find()
    subscriptions_list = []
    for subscription in subscriptions:
        subscriptions_list.append(subscription)
    
    
    trigger_push_notifications_for_subscriptions(subscriptions=subscriptions_list, title=json_data['title'], body=json_data['body'], column=column)

    return jsonify({
        'status' : "success",
        "result" : 200
    })

@app.route('/triggerTestPushNotification', methods=['POST'])
def triggerTestPushNotification():
    json_dict = request.get_json(force=True)
    print(str(json_dict))
    db = client['Users']
    column = db['tokens']

    subscriptions = column.find()
    subscriptions_list = []
    for subscription in subscriptions:
        subscriptions_list.append(subscription)
    
    
    trigger_push_notifications_for_subscriptions(subscriptions=subscriptions_list, title=json_dict['title'], body=json_dict['body'], column=column)

    return jsonify({
        'status' : 200,
        'result' : "success"
    })

@app.route('/get-public-key', methods=['GET'])
def get_public_key():
    return app.config['VAPID_PUBLIC_KEY']    