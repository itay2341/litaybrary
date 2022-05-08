from datetime import datetime
from database import mydatabase
from flask import Flask, render_template
dbms = mydatabase.MyDatabase(mydatabase.SQLITE, dbname='./database/mydb.sqlite')
from admin import admin 
from user import user 

#--------------------------------------------
app = Flask(__name__)
app.register_blueprint(admin) #connect to /admin
app.register_blueprint(user) #connect to /user
#--------------------------------------------



#Home page
@app.route('/')
def home():
    return render_template("index.html")

#Test Method
@app.route('/test')
def test():
    return "test"

#404 - NOT FOUND
@app.route('/<mistake>')
def mistake(mistake):
    return render_template("mistake.html",mistake=mistake)

#Login for users
@app.route('/login')
def login_for_users():
    return render_template("login.html")

#Sign up for everyone ;)
@app.route('/signup')
def signup_for_users():
    now = datetime.now()
    year=now.year
    month=now.month
    day=now.day
    if day<10:day="0"+str(day)
    if month<10:month="0"+str(month)
    return render_template("signup.html",year=year,month=month,day=day)  

#Login for admin
@app.route('/loginAA')
def login_for_admin():
    return render_template("login_admin.html")  

#About page
@app.route('/about')
def about():
    return render_template("about.html")  

