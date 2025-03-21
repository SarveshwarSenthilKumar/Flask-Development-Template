
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_session import Session
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
        return render_template("index.html", authentication=True)

if authentication:
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            if session.get("name"):
                return redirect("/")
            else:
                return render_template("/auth/login.html", message="Invalid username or password")
        return render_template("/auth/login.html")
    
    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            if session.get("name"):
                return redirect("/")
            else:
                return render_template("/auth/signup.html", message="Invalid username or password")
        return render_template("/auth/signup.html")
    
    @app.route("/logout")
    def logout():
        session["name"] = None
        return redirect("/")

if autoRun:
    if __name__ == '__main__':
        app.run(debug=True, port=port)
