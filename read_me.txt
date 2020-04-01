Requirements
-----------------------

-> python 3
-> flask installed
-> cryptography.fernet
-> pymongo
-> mongo db

Running Commands
------------------------

-> run -> mongod
-> for checking only run -> mongo
-> set environment variable
	Windows
	-> set FLASK_APP=run
	Linux
	-> export FLASK_APP=run
-> run > flask run

application should be running by now.


About Application
-----------------------
Design Approach 
Since the application was small I used FLASK framework with basic html.
Here I divided the requirement into 3 files.
run.py - > Maintains all the route related to the project and is responsible for rendering the data on the frontend makes the calls to the various api's/utilities.
helper_apis.py -> Contains the various apis which will do filtering of the data/encrypting and interacting with database data.
project_db.py -> Performs all the CURD operations

Control Flow
-------------
run <-> helper_apis <-> project_db

Cases Covered
-------------
Ip coming to website is tracked and the count is maintained in the database.
Once the thresold is reached the Google Captcha will come into picture.

Due to security concerns I am using default datasite-KEY which is for testing purpose only but is required field if it appears.

To Submit Form
--------------
all the fields are mandatory
same email id can't be create account
password status should be medium or strong
google-captcha is compulsory to submit if it appears
password is encrypted
datetime of the id created is noted in the db

Cases More I wanted to Cover
----------------------------
Session Management with Cookie - I could have done this but due to time contraint I dropped it.
Using Angular - I could have used Angular for frontend part but it would have taken much time.


Video Attached
--------------
Video is attached which covers the running of application and the working and the cases also.