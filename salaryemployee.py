from employee import Employee


class SalaryEmployee(Employee):
    def __init__(self, name, adress, category, salary) -> None:
        super().__init__(name, adress, category)
        self._salary = float(salary)

    @property
    def salary(self):
        return self._salary
    @salary.setter
    def salary(self, salary):
        self._salary = float(salary)