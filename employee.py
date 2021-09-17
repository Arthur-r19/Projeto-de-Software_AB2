class Employee(): 
    def __init__(self, name, adress, category) -> None:
        self._name = name
        self._adress = adress
        self._category = category
        self._mfee = 0
        self._xfee = 0
        self._id = -1
        self._sid = -1
        
    def __str__(self) -> str:
        return str(f'nome: {self._name}\nend: {self._adress}\n categ: {self._category}\nid: {self._id}\nsid: {self._sid}')

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def adress(self):
        return self._adress
    @adress.setter
    def adress(self, adress):
        self._adress = adress

    @property
    def category(self):
        return self._category
    @category.setter
    def category(self, category):
        self._category = category

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def sid(self):
        return self._sid
    @sid.setter
    def sid(self, sid):
        self._sid = sid

    @property
    def mfee(self):
        return self._mfee
    @mfee.setter
    def mfee(self, mfee):
        self._mfee = float(mfee)

    @property
    def xfee(self):
        return self._xfee
    @xfee.setter
    def xfee(self, xfee):
        self._xfee = float(xfee)



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