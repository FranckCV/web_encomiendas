from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
# from flask_jwt import JWT, jwt_required, current_identity
# import uuid
# from functools import wraps
import hashlib
import base64
from datetime import datetime, date


app = Flask(__name__, template_folder='templates')


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/")
@app.route("/login")
def login():
    return render_template("login_2.html")


@app.route("/login_2")
def login_2():
    return render_template("login_2.html")


@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
