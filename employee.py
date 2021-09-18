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
