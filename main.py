from flask import Flask, request
from pymongo import MongoClient
from flask_restful import Api, Resource
from bson.objectid import ObjectId
from bson.json_util import dumps

uri = "mongodb+srv://ansh:kushwaha@cluster.6vpdipl.mongodb.net/?retryWrites=true&w=majority"

app = Flask(__name__)
api = Api(app)
client = MongoClient(uri)
user = client['DATABASE']['USER']


@app.route('/')
def index():
	return dumps('Server Started Successfully')


class UserAPI(Resource):

	def get(self, id=None):
		if id == None:
			return dumps(user.find())
		else:
			return dumps(user.find_one({'_id': ObjectId(id)}))

	def post(self):
		u = dict()
		u['name'] = request.form['name']
		u['email'] = request.form['email']
		u['password'] = request.form['password']
		return dumps(user.insert_one(u).inserted_id)

	def put(self, id):
		u = dict()
		u['name'] = request.form['name']
		u['email'] = request.form['email']
		u['password'] = request.form['password']
		return dumps(user.find_one_and_update({'_id': ObjectId(id)}, {'$set': u}))

	def delete(self, id):
		return dumps(user.find_one_and_delete({'_id': ObjectId(id)}))


api.add_resource(UserAPI, '/users', '/users/<string:id>')

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
