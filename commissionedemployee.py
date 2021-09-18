from employee import Employee


class CommissionedEmployee(Employee):
    def __init__(self, name, adress, category, salary, commission) -> None:
        super().__init__(name, adress, category)
        self._salary = salary
        self._commission = commission
        self._comvalue = 0

    @property
    def salary(self):
        return self._salary
    @salary.setter
    def salary(self, salary):
        self._salary = float(salary)

    @property
    def commission(self):
        return self._commission
    @commission.setter
    def commission(self, commission):
        self._commission = float(commission)

    @property
    def comvalue(self):
        return self._comvalue
    @comvalue.setter
    def comvalue(self, comvalue):
        self._comvalue = float(comvalue)