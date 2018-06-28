
''' WEB API with CRUD capabilities -- Create Read Update Delete '''
''' Python 3 - flask, sqlalchemy and marshmallow required and POSTMAN required for API Testing '''

''' SQL ALCHEMY is the python extendibility of the SQL Database '''
''' and flask_sqlalchemy is the sqlalchemy extension for Flask'''

'''flask-marshmallow is flask extension to integrate flask with marshmallow(an object serialization/deserialization library).
we use flask-marshmallow to rendered json response.'''

'''Flask-SQLAlchemy must be initialized before Flask-Marshmallow.'''


from flask import *
''' Flask is used to initialize a Flask Web Application'''
''' request get the requested data'''
''' jsonify retuens the requested data in the JSON RESPONSE Format '''
from flask_sqlalchemy import SQLAlchemy
''' sqlalchemy is used to access database'''
from flask_marshmallow import Marshmallow
'''
marshmallow schemas can be used to:

-Validate input data.
-Deserialize input data to app-level objects.
-Serialize app-level objects to primitive Python types. The serialized objects can then be rendered to standard formats such as JSON for use in an HTTP API.
'''

app = Flask(__name__)
''' initializes the flask application instance '''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle_api_database.sqlite'
''' defines the URI for the database to be created, here it is a relative path and gets created in the same directory '''
db = SQLAlchemy(app)
''' binding the SQL and MARSHMALLOW instances to our Flask Application '''
ma = Marshmallow(app)



class User(db.Model) :

	''' defining the USER Model 

	vehicle_number is the PRIMARY KEY as each vehicle is Unique and a primary key must be unique and is required i.e. can't be NULL '''

	vehicle_number = db.Column(db.String(10), primary_key = True)
	username = db.Column(db.String(20), nullable = False)
	mobile_number = db.Column(db.String(10), nullable = False)

	def __init__(self, vehicle_number, username, mobile_number) :

		self.vehicle_number = vehicle_number.upper()
		''' even if user inputs car number plate number in small we change it to CAPITAL's using upper()'''
		self.username = username
		self.mobile_number = mobile_number

class UserSchema(ma.Schema) :

	class Meta :

		fields = ('username' , 'vehicle_number' , 'mobile_number')

'''This part defined structure of response of our endpoint. We want that all of our endpoint will have JSON response. Here we define that our 
JSON response will have 3 keys. Also we defined user_schema as instance of UserSchema, and user_schemas as instances of list of UserSchema.'''

user_schema = UserSchema()
users_schema = UserSchema(many = True)


# welcome page route
@app.route("/")
def index():
	return '<h1>Welcome to Vehicle Registration CRUD API</h1>'



# creating a new user using POST method
@app.route("/user" , methods=["POST"])
def add_user() : 

	vehicle_number = request.json['vehicle_number']
	username = request.json['username']
	mobile_number = request.json['mobile_number']

	# provides the data from the request and puts it into the the respective variables 

	new_user = User(vehicle_number, username, mobile_number)
	# creates a new user from this data by filling this data in the User() class

	db.session.add(new_user) # commits this new_user into the database
	db.session.commit()
	return jsonify(new_user)

@app.route("/user", methods=["GET"])
def get_user():

    all_users = User.query.all() # collects all the users in the databse and places them in the all_users variable
    result = users_schema.dump(all_users) # response is created using the 'USERS_SCHEMA' instance
    return jsonify(result.data) # returns the json form of data



@app.route("/user/<vehicle_number>", methods = ["GET"]) # gets the information of the vehicle owner from the use of the VEHICLE NUMBER Primary Key
def user_details(vehicle_number) : # vehicle-number is transferred from route to this function for usage

	user = User.query.get(vehicle_number) # finds the user with the following vehicle from the db
	return user_schema.jsonify(user)  # return the json response of the user in the form defined by user_schema instance

# searching by primary key is usually faster than by other field 
# hence as each vehicle will have a unique ownwer and contact info so we make the vehicle the PRIMARY KEY and all the searching are done with this
# primary key 

@app.route("/user/<vehicle_number>", methods = ["PUT"]) # updating the information of the vehicle 
def user_update(vehicle_number) :

	user = User.query.get(vehicle_number) # finding the user with this vehicle

	vehicle_number = request.json['vehicle_number']
	username = request.json['username'] # taking the new information which will replace the older info
	mobile_number = request.json['mobile_number']

	user.vehicle_number = vehicle_number.upper()
	user.username = username # updating the data of the user with this vehicle
	user.mobile_number = mobile_number

	db.session.commit() # commiting the new data to the db
	return user_schema.jsonify(user)  # return the json response of the user in the form defined by user_schema instance


@app.route("/user/<vehicle_number>" , methods = ["DELETE"]) # deleting the info of a particular vehicle
def user_delete(vehicle_number) :

	user = User.query.get(vehicle_number) # get the user with the particular vehicle and create it's instance
	db.session.delete(user) # delete this user from the database
	db.session.commit() # commit this changes to db

	return user_schema.jsonify(user) # return the json response of the deleted user in the form defined by user_schema instance


if __name__ == '__main__' : 
	app.run(debug = True)