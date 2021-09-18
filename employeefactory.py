from hourlyemployee import HourlyEmployee as hemployee
from commissionedemployee import CommissionedEmployee as cemployee
from salaryemployee import SalaryEmployee as semployee

class EmployeeFactory():
    def packageEmployee(nome, endereco, tipo, salario, comissao):
        if tipo == 'Horista':
            newemployee = hemployee(nome, endereco, tipo, salario)
        elif tipo == 'Assalariado':
            newemployee = semployee(nome, endereco, tipo, salario)
        elif tipo == 'Comissionado':  
            newemployee = cemployee(nome, endereco, tipo, salario, comissao)
        return newemployee
        
    def repackageEmployee(oldemployee, nome, endereco, tipo, salario, comissao):
        if tipo == 'Horista':
            editemployee = hemployee(nome, endereco, tipo, salario)
            if oldemployee.category == 'Horista':
                editemployee.workedtime = oldemployee.workedtime
        elif tipo == 'Assalariado':
            editemployee = semployee(nome, endereco, tipo, salario)
        elif tipo == 'Comissionado': 
            editemployee = cemployee(nome, endereco, tipo, salario, comissao)
        
        editemployee.id = oldemployee.id
        return editemployee
