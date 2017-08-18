from flask_httpauth import HTTPBasicAuth
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'Abdo':
        return '123456'
    return None
'''
@auth.error_handler
def unathorized():
    return make_response(jsonify({'error': 'unathorized access'}),401)
'''
class Employees(Resource):
    @auth.login_required 
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from employees") # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID

class Tracks(Resource):
    @auth.login_required
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
class Employees_Name(Resource):
    @auth.login_required
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
@app.route('/delete/<int:trackid>', methods=['DELETE', 'GET']) #deletes a track with a specific track id
def delete(trackid):
    if request.method=='GET':
        return ""
    else:
        print(request.method)
        conn = db_connect.connect()
        query = conn.execute("delete from tracks where trackid =%d " %int(trackid))

api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3
#api.add_resource(delete, '/delete/<track_id>')#Route_4 #optional since i used @app.route with this route
