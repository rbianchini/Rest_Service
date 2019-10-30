# export FLASK_APP=main.py
# export FLASK_ENV=development
# flask run


from flask import Flask, session, escape, request
from flask_restful import Api, Resource
import pymongo
import hashlib
import json
from Machine import Machine, Machine_date_mngmt
import loadDB

app = Flask(__name__)
api = Api(app)


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dbname = "test_rest"
if dbname not in myclient.database_names():
    loadDB.loadDB()
mydb = myclient[dbname]

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
    # Retorna una maquina (2.1 y 2.2)
    def get(self, machine_id):
        machine_colection = mydb["machine"]
        machine = machine_colection.find_one({"_id": machine_id})
        if machine:
            return Machine(**machine).machine_to_JSON()
        else:
            return {"error": "Not found"}, 404

    # Borra una maquina (4)
    def delete(self, machine_id):
        machine_colection = mydb["machine"]
        machine = machine_colection.find_one({"_id": machine_id})
        if machine:
            machine_colection.delete_one({"_id": machine_id})
            return {"result": True}
        else:
            return {"result": False}

    # Actualiza una maquina (3)
    def put(self, machine_id):
        machine_colection = mydb["machine"]
        machine = machine_colection.find_one({"_id": machine_id})
        if machine:
            keys = request.form.keys()
            no_keys = True
            for k in keys:
                no_keys = False
                dic = json.loads(k)
                query = {"_id": machine_id}
                if 'owner' in dic:
                    value = {"$set": {"owner": dic["owner"]}}
                    machine_colection.update_one(query, value)
                    machine["owner"] = dic["owner"]
                elif 'name' in dic:
                    value = {"$set": {"name": dic["name"]}}
                    machine_colection.update_one(query, value)
                    machine["name"] = dic["name"]
                elif 'description' in dic:
                    value = {"$set": {"description": dic["description"]}}
                    machine_colection.update_one(query, value)
                    machine["description"] = dic["description"]
                else:
                    return {"result": False}, 400
            if no_keys:
                return {"result": False}, 400
            created = Machine_date_mngmt.date_to_str(machine["created"])
            machine["created"] = created
            return machine
        else:
            return {"result": False}, 404


class all_machines(Resource):
    # Retorna todas las máquinas (2.3)
    def get(self):
        machine_colection = mydb["machine"]
        machines = machine_colection.find()
        todas = []
        for m in machines:
            created = Machine_date_mngmt.date_to_str(m["created"])
            m["created"] = created
            todas.append(m)
        return ["machines: ", todas]


class add_machine(Resource):
    # Crea una machine y la guarda en bd (1)
    def post(self):
        keys = request.form.keys()
        no_keys = True
        for k in keys:
            no_keys = False
            kj = json.loads(k)
            machine_colection = mydb["machine"]
            machine_id = kj["machine_id"]
            machine = machine_colection.find_one({"_id": machine_id})
            if machine:
                return {"result": False}, 400
            name = kj["name"]
            owner = ""
            if 'username' in session:
                owner = session['username']
            new_machine = Machine(_id=machine_id, name=name, owner=owner)
            machine_colection.insert_one(new_machine.machine_to_DB())
            return new_machine.machine_to_JSON()
        if no_keys:
            return {"result": False}, 400


api.add_resource(login, '/api/auth/login')
api.add_resource(logout, '/api/auth/logout')
api.add_resource(one_machine, '/api/machines/<machine_id>')
api.add_resource(all_machines, '/api/machines')
api.add_resource(add_machine, '/api/machines/add-machine')
