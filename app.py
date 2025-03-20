
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_session import Session
from sql import * #Used for database connection and management
from SarvAuth import * #Used for user authentication functions

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

port = 5000 #Change to any port of your choice if you want to run the server automatically

#This route is the base route for the website which renders the index.html file
@app.route("/", methods=["GET", "POST"])
def index():
   return render_template("index.html")

"""
#Un-comment this code to run the server automatically by running the app.py file
if __name__ == '__main__':
    app.run(debug=True, port=port)
"""