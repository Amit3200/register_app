#amit3200 github
import json
import time
import base64
import requests
import project_db
import helper_apis
from datetime import datetime,timedelta
from flask import Flask, render_template, redirect, url_for, request,jsonify,make_response


KEY=helper_apis
app = Flask(__name__)
if project_db.client=='':
	print("Connection Called")
	project_db.establish_mongodb_connection()
  
@app.route("/")
def index():
	ip_address_read = request.remote_addr
	captcha_status = helper_apis.check_for_captcha(ip_address_read)
	return render_template("sign_up.html",captcha=captcha_status)

@app.route("/accounts/signup",methods=["POST"])
def signup():
	if request.method=="POST":
		response = helper_apis.filter_keys_as_required(request.form)
		response['remote_ipaddress'] = request.remote_addr
		return helper_apis.response_from_sign_up(response)
	else:
		return "Something! Went Wrong."
	return "error"


@app.errorhandler(404)
def not_found(e): 
  return "404 error! Page Not Found"