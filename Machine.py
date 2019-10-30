import datetime


class Machine:

    def __init__(self, _id, name, description="",
                 created=datetime.datetime.now().replace(microsecond=0),
                 owner=""):
        if self.check_name(name):
            if self.check_id(_id):
                self.name = name
                self._id = _id
                if description == "":
                    self.description = name
                else:
                    self.description = description
                if isinstance(created, datetime.datetime):
                    self.created = datetime.datetime.now().\
                        replace(microsecond=0)
                else:
                    self.created = Machine_date_mngmt.str_to_date(created)
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
            "_id": self._id,
            "name": self.name,
            "description": self.description,
            "created": self.created,
            "owner": self.owner
            }

    def machine_to_JSON(self):
        dic = {
            "_id": self._id,
            "name": self.name,
            "description": self.description,
            "created": Machine_date_mngmt.date_to_str(self.created),
            "owner": self.owner
            }
        return dic


class Machine_date_mngmt:
    def date_to_str(created):
        return created.strftime("%Y-%m-%d %H:%M:%S")

    def str_to_date(created):
        return(datetime.strptime(created, '%Y-%m-%d %H:%M:%S'))
