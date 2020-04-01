from pymongo import MongoClient

client = ''
CORE_DB_NAME = 'app_test_1'
USER_COLLECTION_NAME = 'users'
IP_ADDRESS_COLLECTION_NAME = 'ipaddress_track'
CURRENT_RUNNING_DATABASE = ''
USER_RUNNING_COLLECTION =  ''
IP_ADDRESS_RUNNING_COLLECTION = ''

def establish_mongodb_connection():
	global client,CURRENT_RUNNING_DATABASE,CORE_DB_NAME,USER_RUNNING_COLLECTION,USER_COLLECTION_NAME,IP_ADDRESS_RUNNING_COLLECTION,IP_ADDRESS_COLLECTION_NAME
	client=MongoClient("mongodb://127.0.0.1:27017")
	CURRENT_RUNNING_DATABASE=client[CORE_DB_NAME]
	USER_RUNNING_COLLECTION=CURRENT_RUNNING_DATABASE[USER_COLLECTION_NAME]
	IP_ADDRESS_RUNNING_COLLECTION=CURRENT_RUNNING_DATABASE[IP_ADDRESS_COLLECTION_NAME]

def common_error_renderer():
	return {"status":404,"text":"Keys of the response were not valid, some things were missing"}

def db_connection_error():
	return "Something went wrong"

# for testing purpose
# def list_users_from_database():
# 	global USER_RUNNING_COLLECTION
# 	response_collected = USER_RUNNING_COLLECTION
# 	for resp in response_collected.find():
# 		print(resp)

def get_details_from_db(params):
	global USER_RUNNING_COLLECTION
	if params==None:
		all_response = [resp for resp in USER_RUNNING_COLLECTION.find()]
		return all_response
	else:
		if USER_RUNNING_COLLECTION.find(params) == -1:
			all_response = []
		else:
			all_response = [resp for resp in USER_RUNNING_COLLECTION.find(params)]
		return all_response

def insert_record_in_db(params):
	global USER_RUNNING_COLLECTION
	USER_RUNNING_COLLECTION.insert_one(params)

def insert_new_user_record(params):
	if params==None:
		return common_error_renderer()
	else:
		insert_record_in_db(params)

def insert_ip_record(params):
	global IP_ADDRESS_RUNNING_COLLECTION
	try:
		params["ip_count"]=1
		IP_ADDRESS_RUNNING_COLLECTION.insert_one(params)
		return params["ip_count"]
	except Exception as ex:
		print(ex)
		return db_connection_error()


def update_ip_record(params):
	global IP_ADDRESS_RUNNING_COLLECTION
	try:
		record = [res for res in IP_ADDRESS_RUNNING_COLLECTION.find(params)][0]
		curr_count = record["ip_count"]+1
		IP_ADDRESS_RUNNING_COLLECTION.update_one(params,{"$set":{"ip_count":curr_count}})
		return curr_count
	except Exception as ex:
		print(ex)
		return db_connection_error()


def check_if_some_record_exists(params):
	global IP_ADDRESS_RUNNING_COLLECTION
	try:
		resp = [res for res in IP_ADDRESS_RUNNING_COLLECTION.find(params)]
		if IP_ADDRESS_RUNNING_COLLECTION.find() == -1 or IP_ADDRESS_RUNNING_COLLECTION.find(params)== -1 or resp==[]:
			return False
		else:
			return True
	except Exception as ex:
		print(ex)
		return db_connection_error()

def get_ip_count(params):
	global IP_ADDRESS_RUNNING_COLLECTION
	if check_if_some_record_exists(params):
		ip_count=update_ip_record(params)
	else:
		ip_count=insert_ip_record(params)
	if type(ip_count)==int:
		return ip_count
	else:
		return 0

def ip_address_for_day(params):
	global IP_ADDRESS_RUNNING_COLLECTION
	ip_count = get_ip_count(params)
	if ip_count>3:
		return {"CAPTCHA":True,"IP_COUNT":ip_count}
	else:
		return {"CAPTCHA":False,"IP_COUNT":ip_count}


