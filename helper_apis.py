import json
import project_db
from cryptography.fernet import Fernet
from datetime import datetime,timedelta
# For Demonstartion Purpose Other Wise Reccomended To Store In Environment Variable
SECURITY_CRYPTIC_KEY="Ht1EaxLc6vijk-QW9VFg206b0JGPIG5vH54yP3-HOKs="
fernet_encrypt_obj = Fernet(SECURITY_CRYPTIC_KEY)

def filter_keys_as_required(response):
	new_response={}
	new_response["email_id"]=response["email"]
	new_response["user_name"]=response["username"]
	new_response["pass_key"]=response["password"]
	return new_response

def valid_keys_in_response(response):
	response_keys=list(response.keys())
	keys_in_db = ["email_id","pass_key","user_name"]
	return all(ele in response_keys for ele in keys_in_db)

def search_if_valid_email_id(email_id):
	params = {"email_id":email_id}
	resp = project_db.get_details_from_db(params)
	# new id found
	if len(resp) == 0:
		return True
	else:
		return False

def encrypt_user_password(pass_code):
	pass_key=str(fernet_encrypt_obj.encrypt(bytes(pass_code,'utf-8')))
	return pass_key

def search_in_database(response):
	return search_if_valid_email_id(response['email_id'])

def validate_response(response):
	if valid_keys_in_response(response):
		return search_in_database(response)
	else:
		return project_db.common_error_renderer()

def check_for_captcha(ip_address_response):
	try:
		params ={"ip_address":ip_address_response,"ip_date":datetime.now().date().strftime("%Y-%m-%d")}
		status_captcha=project_db.ip_address_for_day(params)
		if status_captcha["CAPTCHA"]:
			return True
		else:
			return False
	except Exception as ex:
		print(ex)
		return "Sorry! Something went wrong here"

def response_from_sign_up(response):
	if validate_response(response):
		response["pass_key"]=encrypt_user_password(response['pass_key'])	
		response["time_created"]=datetime.now().timestamp()
		try:
			project_db.insert_new_user_record(response)
			return "Account Created for "+response["user_name"].title()
		except Exception as ex:
			print(ex)
			return "Sorry! Something went wrong here"
	else:
		return "Email Id Already Registered!"