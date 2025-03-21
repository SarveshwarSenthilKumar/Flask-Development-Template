
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_session import Session
from datetime import datetime
import pytz
from sql import * #Used for database connection and management
from SarvAuth import * #Used for user authentication functions

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

autoRun = False #Change to True if you want to run the server automatically by running the app.py file
port = 5000 #Change to any port of your choice if you want to run the server automatically
authentication = True #Change to False if you want to disable user authentication

#This route is the base route for the website which renders the index.html file
@app.route("/", methods=["GET", "POST"])
def index():
    if authentication == False:
        return render_template("index.html")
    else:
        if not session.get("name"):
            return render_template("index.html", authentication=True)
        else:
            return render_template("/auth/loggedin.html")

if authentication:
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if session.get("name"):
            return redirect("/")
        if request.method == "GET":
            return render_template("/auth/login.html")
        else:
            username = request.form.get("username").strip().lower()
            password = request.form.get("password").strip()

            password = hash(password)

            db = SQL("sqlite:///users.db")
            users=db.execute("SELECT * FROM users WHERE username = :username", username=username)

            if len(users) == 0:
                return render_template("/auth/login.html", error="No account has been found with this username!")
            user = users[0]
            if user["password"] == password:
                session["name"] = username
                return redirect("/")

            return render_template("/auth/login.html", error="You have entered an incorrect password! Please try again!")
    
    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if session.get("name"):
            return redirect("/")
        if request.method=="GET":
            return render_template("/auth/signup.html")
            
        emailAddress = request.form.get("emailaddress").strip().lower()
        fullName = request.form.get("name").strip()
        username = request.form.get("username").strip().lower()
        password = request.form.get("password").strip()

        validName = verifyName(fullName)
        if not validName[0]:
            return render_template("/auth/signUp.html", error=validName[1])
        fullName = validName[1]

        db = SQL("sqlite:///users.db")
        results = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        if len(results) != 0:
            return render_template("/auth/signup.html", error="This username is already taken! Please select a different username!")
        if not checkEmail(emailAddress):
            return render_template("/auth/signup.html", error="You have not entered a valid email address!")
        if len(checkUserPassword(username, password)) > 1:
            return render_template("/auth/signup.html", error=checkUserPassword(username, password)[1])
        
        tz_NY = pytz.timezone('America/New_York') 
        now = datetime.now(tz_NY)
        dateJoined = now.strftime("%d/%m/%Y %H:%M:%S")

        password = hash(password)
        
        db = SQL("sqlite:///users.db")
        db.execute("INSERT INTO users (username, password, emailaddress, name, dateJoined) VALUES (?,?,?,?,?)", username, password, emailAddress, fullName, dateJoined)

        session["name"] = username
        
        return redirect("/")
    
    @app.route("/logout")
    def logout():
        session["name"] = None
        return redirect("/")

if autoRun:
    if __name__ == '__main__':
        app.run(debug=True, port=port)
