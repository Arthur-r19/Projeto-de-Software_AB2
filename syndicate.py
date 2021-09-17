from random import randint

class Syndicate():
    affiliatesList = {}
    
    @staticmethod
    def generate_new_sid() -> int:
        id = randint(0,499)
        i=0
        while id in Syndicate.affiliatesList:
            id = randint(0,499)
            i = i+1
            if i>501:
                return -1
        return id

    @classmethod
    def add_affiliate(cls, employee):
        newsid = cls.generate_new_sid()
        if newsid == -1:
            return False
        else:
            employee.sid = newsid
            cls.affiliatesList[employee.sid] = employee
            return True

    @classmethod
    def remove_affiliate(cls, sid):
        del cls.affiliatesList[sid]

    @classmethod
    def edit_affiliate(cls, id, editedAffiliate):
        del cls.affiliatesList[id]
        cls.affiliatesList[id] = editedAffiliate
