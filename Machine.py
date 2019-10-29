import datetime


class Machine:

    def __init__(self, name, machine_id, *description, created, owner):
        if self.check_name(name):
            if self.check_id(machine_id):
                self.name = name
                self.machine_id = machine_id
                if description is None or description == "":
                    self.description = name
                else:
                    self.description = description
                if created is None or created == "":
                    self.created = datetime.datetime.now().replace(microsecond=0)
                else:
                    self.created = created
                self.owner = owner
            else:
                raise("El Id debe tener 8 caracteres")
        else:
            raise("El nombre debe tener hasta 128 caracteres")

    def check_name(self, name):
        if len(name) <= 128:
            return True
        else:
            return False

    def check_id(self, id):
        if len(id) == 8:
            return True
        else:
            return False

    def machine_to_DB(self):
        return {
            "_id": self.machine_id,
            "name": self.name,
            "description": self.description,
            "created": self.created,
            "owner": self.owner
            }
