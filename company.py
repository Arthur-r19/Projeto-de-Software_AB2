from employee import Employee
from random import randint

class Company():
    employeesList = {}

    @staticmethod
    def generate_new_id() -> int:
        id = randint(0,499)
        i=0
        while id in Company.employeesList:
            id = randint(0,499)
            i=i+1
            if i>501:
                return -1
        return id

    @classmethod
    def add_employee(cls, employee):
        newid = cls.generate_new_id()
        if newid == -1:
            return False
        else:
            employee.id = newid
            cls.employeesList[employee.id] = employee
            return True

    @classmethod
    def remove_employee(cls, id):
        del cls.employeesList[id]

    @classmethod
    def edit_employee(cls, id, editedEmployee):
        del cls.employeesList[id]
        cls.employeesList[id] = editedEmployee
