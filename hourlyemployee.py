from employee import Employee

class HourlyEmployee(Employee):
    def __init__(self, name, adress, category, wage) -> None:
        super().__init__(name, adress, category)
        self._wage = wage
        self._workedtime = 0

    @property
    def wage(self):
        return self._wage
    @wage.setter
    def wage(self, wage):
        self._wage = float(wage)

    @property
    def workedtime(self):
        return self._workedtime
    @workedtime.setter
    def workedtime(self, workedtime):
        self._workedtime = float(workedtime)