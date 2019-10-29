import pymongo
from Machine import Machine  # , Machine_date_mngmt

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["optiagro_test"]


m_id = input("machine_id: ")
print()
if Machine.check_id("", m_id):
    machine_colection = mydb["machine"]
    m_machine = machine_colection.find_one({"_id": m_id})
    if m_machine:
        new_machine = Machine(**m_machine)
        # print(json.dumps(new_machine))
        # print(json.loads(new_machine))
        print("new_machine = ", new_machine)
    else:
        print({"error": "Not found"})
else:
    print({"error": "id mal formado"})
otra_machine = Machine("id123456", "nombre")
dict = otra_machine.machine_to_DB()
print("type(dict) ", type(dict))
print("dict = ", dict)
jdict = otra_machine.machine_to_JSON()
print("type(jdict) ", type(jdict))
print("jdict = ", jdict)


# def machines():
# 	machine_colection = mydb["machine"]
# 	maquinas = machine_colection.find()
# 	all_machines = []
# 	import json
# 	for m in maquinas:
# 		#"created": "2019-10-23 19:25:35",
# 		datestr = m["created"].strftime("%Y-%m-%d %H:%M:%S")
# 		print(datestr)
# 		m["created"] = datestr
# 		print(json.dumps(m))
# 		all_machines.append(json.dumps(m))
#
# 	return " ".join(all_machines)
