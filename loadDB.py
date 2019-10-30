import pymongo
import hashlib
import Machine


class loadDB:
    def __init__(self):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        dbname = "test_rest"
        mydb = myclient[dbname]
        user_colection = mydb["user"]
        user1 = {
            "name": "Renzo",
            "password": hashlib.sha1(b"abc123").hexdigest()
        }
        user2 = {
            "name": "Otro",
            "password": hashlib.sha1(b"Otra").hexdigest()
        }
        user_list = [user1, user2]
        user_colection.insert_many(user_list)

        machine_colection = mydb["machine"]
        machine1 = Machine.Machine("machine1", "12345678")
        machine2 = Machine.Machine("machine2", "abcdefgh")
        machine_list = [machine1.machine_to_DB(), machine2.machine_to_DB()]
        machine_colection.insert_many(machine_list)

        print("usuario1 = ", user1)
        print("usuario2 = ", user2)
        print("mchine1 = ", machine1.machine_to_JSON())
        print("mchine2 = ", machine2.machine_to_JSON())
