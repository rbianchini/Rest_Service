# export FLASK_APP=main.py
# export FLASK_ENV=development
# flask run


from flask import Flask, session, escape, request
from flask_restful import Api, Resource
import pymongo
import hashlib
from Machine import Machine, Machine_date_mngmt

app = Flask(__name__)
api = Api(app)


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["optiagro_test"]

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


class login(Resource):

    def get(self):
        if 'username' in session:
            return 'Logged in as %s' % escape(session['username'])
        return 'You are not logged in '

    def post(self):
        username = request.form['username']
        user_colection = mydb["user"]
        user = user_colection.find_one({"_id": username})
        if user:
            password = request.form['password'].encode('utf-8')
            password = hashlib.sha1(password).hexdigest()
            if password == user['password']:
                session['username'] = request.form['username']
                session.permanent = True
                return 'sesion iniciada'
            else:
                return 'Password incorrecta'
        else:
            return 'Usuario no válido'


class logout(Resource):

    def get(self):
        if session['username']:
            session.pop('username', None)
            session.permanent = False
            return 'Successful logout '
        return 'sesion no iniciada'


class one_machine(Resource):
    def get(self, machine_id):
        machine_colection = mydb["machine"]
        machine = machine_colection.find_one({"_id": machine_id})
        if machine:
            return machine.machine_to_JSON()
        else:
            return "machine no existe"

    def delete(self, machine_id):
        machine_colection = mydb["machine"]
        machine = machine_colection.find_one({"_id": machine_id})
        if machine:
            machine_colection.delete_one({"_id": machine_id})
            return "machine borrada con exito"
        else:
            return "machine no existe"

    def put(self, machine_id):
        machine_colection = mydb["machine"]
        machine = machine_colection.find_one({"_id": machine_id})
        if machine:
            owner = request.form['owner']
            machine_colection.update_one({"_id": machine_id}, {"owner": owner})
            machine["owner"] = owner
            created = Machine_date_mngmt.date_to_str(machine["created"])
            machine["created"] = created
            return machine
        else:
            return "machine no existe"


class all_machines(Resource):
    def get(self):
        machine_colection = mydb["machine"]
        machines = machine_colection.find()
        todas = []
        for m in machines:
            created = Machine_date_mngmt.date_to_str(m["created"])
            m["created"] = created
            todas.append(m)
        return todas


api.add_resource(login, '/api/auth/login')
api.add_resource(logout, '/api/auth/logout')
api.add_resource(one_machine, '/api/machines/<machine_id>')
api.add_resource(all_machines, '/api/machines')
