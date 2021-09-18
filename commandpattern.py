"""
The Command Pattern Concept
https://sbcode.net/python/command/#commandcommand_conceptpy
"""
import re
from employeefactory import EmployeeFactory
from PySimpleGUI import PySimpleGUI as sg
from abc import ABCMeta, abstractmethod
class ICommand(metaclass=ABCMeta):  # pylint: disable=too-few-public-methods
    "The command interface, that all commands will implement"
    @staticmethod
    @abstractmethod
    def execute():
        """
        The required execute method that all command objects
        will use
        """
class Invoker:
    "The Invoker Class"
    def __init__(self):
        self._commands = {}

    def register(self, command_name, command):
        "Register commands in the Invoker"
        self._commands[command_name] = command
        
    def execute(self, command_name):
        "Execute any registered commands"
        if command_name in self._commands.keys():
            self._commands[command_name].execute()
        else:
            print(f"Command [{command_name}] not recognised")


class Receiver:
    "The Receiver"
    def __init__(self, dict, janela, empresa, sindicato, controller, id, sid) -> None:
        self._dict = dict
        self._janela = janela
        self._empresa = empresa
        self._sindicato = sindicato
        self._controller = controller
        self._id = id
        self._sid = sid 

    @property
    def dict(self):
        return self._dict
    @dict.setter
    def dict(self, dict):
        self._dict = dict

    @property
    def janela(self):
        return self._janela
    @janela.setter
    def janela(self, janela):
        self._janela = janela

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


    def run_command_mp_empresa(self):
        self._controller.update_window_layout(self.janela,'-LayoutMenuEmpresa-')
    
    def run_command_mp_sindicato(self):
        self._controller.update_window_layout(self.janela,'-LayoutMenuSindicato-')

    def run_command_me_adicionar(self):
        self._controller.update_window_layout(self.janela, '-LayoutAdicionarEmpregado-')

    def run_command_me_ponto(self):
        self.id, chave = janela_lista_gerenciar('Horista', self._empresa.employeesList)
        if self.id != -1 and chave == 'L-PONTO':
            selectedEmployee = self._empresa.employeesList.get(self.id)
            workedtime = janela_calculo(selectedEmployee, 'Ponto')
            selectedEmployee.workedtime += workedtime
            sg.popup(f'Ponto de {workedtime} horas registrado com sucesso para o seguinte funcionário:\nFuncionário {selectedEmployee.name}\nID: {selectedEmployee.id}\nHoras Acumuladas: {selectedEmployee.workedtime} Horas')

    def run_command_me_venda(self):
        self.id, chave = janela_lista_gerenciar('Comissionado', self._empresa.employeesList)
        if self.id != -1 and chave == 'L-VENDA':
            selectedEmployee = self._empresa.employeesList.get(self.id)
            valorvenda = janela_calculo(selectedEmployee, 'Venda')
            selectedEmployee.comvalue += valorvenda
            sg.popup(f'Comissão de R$ {valorvenda} registrada com sucesso para o seguinte funcionário:\nFuncionário {selectedEmployee.name}\nID: {selectedEmployee.id}\nComissao Acumulada: R$ {selectedEmployee.comvalue}')

    def run_command_me_lista(self):
        self.id, chave = janela_lista_gerenciar('Geral', self._empresa.employeesList)
        if self.id != -1 and chave == 'L-EDITAR':
            selectedEmployee = self._empresa.employeesList.get(self.id)
            self.sid = selectedEmployee.sid
            self._controller.import_employee_menu(self.janela, selectedEmployee)
            self._controller.update_window_layout(self.janela, '-LayoutEditarEmpregado-')
        elif self.id != -1 and chave == 'L-REMOVER':
            selectedEmployee = self._empresa.employeesList.get(self.id)
            self.sid = selectedEmployee.sid
            self._empresa.remove_employee(self.id)
            if self.sid != -1:
                self._sindicato.remove_affiliate(self.sid)
            sg.popup(f'Empregado {selectedEmployee.name} demitido!')

    def run_command_me_voltar(self):
        self._controller.update_window_layout(self.janela, '-LayoutMenuPrincipal-')
    
    def run_command_mae_tipodecontrato(self):
        if self.dict['MAE-TIPODECONTRATO'] == 'Comissionado':
            self.janela['MAE-TEXTOSALARIO'].update('Salário Mensal')
            self.janela['MAE-VALORCOMISSAO'].update(disabled=False)
        
        elif self.dict['MAE-TIPODECONTRATO'] == 'Horista':
            self.janela['MAE-TEXTOSALARIO'].update('Valor da Hora')
            self.janela['MAE-VALORCOMISSAO'].update('')
            self.janela['MAE-VALORCOMISSAO'].update(disabled=True)
        else:
            self.janela['MAE-TEXTOSALARIO'].update('Salário Mensal')
            self.janela['MAE-VALORCOMISSAO'].update('')
            self.janela['MAE-VALORCOMISSAO'].update(disabled=True)
    
    def run_command_mae_sindicato(self):
        if self.dict['MAE-SINDICATO']:
            self.janela['MAE-VALORSINDICATO'].update(disabled=False)
        else:
            self.janela['MAE-VALORSINDICATO'].update('')
            self.janela['MAE-VALORSINDICATO'].update(disabled=True)

    def run_command_mae_confirmar(self):
        if self.dict['MAE-NOME'] == '' or self.dict['MAE-ENDERECO'] == '':
            sg.popup('Preencha todos os Dados Pessoais!', title='Dados Incompletos')
        
        elif self.dict['MAE-VALORSALARIO'] == '':
            sg.popup('Preencha todos os Detalhes do Contrato!', title='Dados Incompletos')

        elif self.dict['MAE-TIPODECONTRATO'] == 'Comissionado' and self.dict['MAE-VALORCOMISSAO'] == '':
            sg.popup('Preencha todos os Detalhes do Contrato!', title='Dados Incompletos')

        elif self.dict['MAE-SINDICATO'] and self.dict['MAE-VALORSINDICATO'] == '':
            sg.popup('Preencha todos os Detalhes do Contrato!', title='Dados Incompletos')

        else:
            newemployee = EmployeeFactory.packageEmployee(self.dict['MAE-NOME'], self.dict['MAE-ENDERECO'], self.dict['MAE-TIPODECONTRATO'], self.dict['MAE-VALORSALARIO'], self.dict['MAE-VALORCOMISSAO'])
            self._empresa.add_employee(newemployee)
            if self.dict['MAE-SINDICATO']:
                newemployee.mfee = int(self.dict['MAE-VALORSINDICATO'])
                self._sindicato.add_affiliate(newemployee)
            
            sg.popup(f"Funcionário {self.dict['MAE-NOME']} adicionado com sucesso!\nID: {newemployee.id}", title='Cadastro Concluído')
            self._controller.reset_employee_menu(self.janela,'MAE')
            self._controller.update_window_layout(self.janela, '-LayoutMenuEmpresa-')

    def run_command_mae_cancelar(self):
        self._controller.reset_employee_menu(self.janela,'MAE')
        self._controller.update_window_layout(self.janela, '-LayoutMenuEmpresa-')

    def run_command_mee_tipodecontrato(self):
        if self.dict['MEE-TIPODECONTRATO'] == 'Comissionado':
            self.janela['MEE-TEXTOSALARIO'].update('Salário Mensal')
            self.janela['MEE-VALORCOMISSAO'].update(disabled=False)
        
        elif self.dict['MEE-TIPODECONTRATO'] == 'Horista':
            self.janela['MEE-TEXTOSALARIO'].update('Valor da Hora')
            self.janela['MEE-VALORCOMISSAO'].update('')
            self.janela['MEE-VALORCOMISSAO'].update(disabled=True)
        else:
            self.janela['MEE-TEXTOSALARIO'].update('Salário Mensal')
            self.janela['MEE-VALORCOMISSAO'].update('')
            self.janela['MEE-VALORCOMISSAO'].update(disabled=True)
    
    def run_command_mee_sindicato(self):
        if self.dict['MEE-SINDICATO']:
            self.janela['MEE-VALORSINDICATO'].update(disabled=False)
        else:
            self.janela['MEE-VALORSINDICATO'].update('')
            self.janela['MEE-VALORSINDICATO'].update(disabled=True)

    def run_command_mee_confirmar(self):
        if self.dict['MEE-NOME'] == '' or self.dict['MEE-ENDERECO'] == '':
            sg.popup('Preencha todos os Dados Pessoais!', title='Dados Incompletos')
        
        elif self.dict['MEE-VALORSALARIO'] == '':
            sg.popup('Preencha todos os Detalhes do Contrato!', title='Dados Incompletos')

        elif self.dict['MEE-TIPODECONTRATO'] == 'Comissionado' and self.dict['MEE-VALORCOMISSAO'] == '':
            sg.popup('Preencha todos os Detalhes do Contrato!', title='Dados Incompletos')

        elif self.dict['MEE-SINDICATO'] and self.dict['MEE-VALORSINDICATO'] == '':
            sg.popup('Preencha todos os Detalhes do Contrato!', title='Dados Incompletos')

        else:
            selectedEmployee = self._empresa.employeesList.get(self.id)
            print(selectedEmployee, self.id)
            editemployee = EmployeeFactory.repackageEmployee(selectedEmployee, self.dict['MEE-NOME'], self.dict['MEE-ENDERECO'], self.dict['MEE-TIPODECONTRATO'], self.dict['MEE-VALORSALARIO'], self.dict['MEE-VALORCOMISSAO'])
            self._empresa.edit_employee(self.id, editemployee)
            if self.dict['MEE-SINDICATO'] and self.sid != -1:
                editemployee.sid = self.sid
                editemployee.mfee = int(self.dict['MEE-VALORSINDICATO'])
                self._sindicato.edit_affiliate(self.sid, editemployee)

            elif self.dict['MEE-SINDICATO'] and self.sid == -1:
                editemployee.mfee = int(self.dict['MEE-VALORSINDICATO'])
                self._sindicato.add_affiliate(editemployee)
            
            elif not self.dict['MEE-SINDICATO'] and self.sid != -1:
                self._sindicato.remove_affiliate(self.sid)
            
            
            sg.popup(f"Funcionário alterado para {editemployee.name} com sucesso!\nID: {editemployee.id}", title='Edição Concluído')
            self.id = -1
            self.sid = -1
            self._controller.reset_employee_menu(self.janela,'MEE')
            self._controller.update_window_layout(self.janela, '-LayoutMenuEmpresa-')

    def run_command_mee_cancelar(self):
        sg.popup('Nenhum detalhe foi alterado.', title='')
        self.id = -1
        self.sid = -1
        self._controller.reset_employee_menu(self.janela,'MEE')
        self._controller.update_window_layout(self.janela, '-LayoutMenuEmpresa-')

    def run_command_ms_lista(self):
        self.sid, chave = janela_lista_gerenciar('Afiliados', self._sindicato.affiliatesList)
        if self.sid != -1 and chave == 'L-TAXA':
            selectedEmployee = self._sindicato.affiliatesList.get(self.sid)
            valortaxa = janela_calculo(selectedEmployee, 'Taxa')
            selectedEmployee.xfee += valortaxa
            sg.popup(f'Taxa de R$ {valortaxa} registrada com sucesso para o seguinte funcionário:\nFuncionário: {selectedEmployee.name}\nSID: {selectedEmployee.sid}\nTotal Pendente: R$ {selectedEmployee.xfee}')
    
    def run_command_ms_voltar(self):
        self._controller.update_window_layout(self.janela, '-LayoutMenuPrincipal-')


class Command_MP_EMPRESA(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_mp_empresa()

class Command_MP_SINDICATO(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_mp_sindicato()

class Command_ME_ADICIONAR(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_me_adicionar()

class Command_ME_PONTO(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_me_ponto()

class Command_ME_VENDA(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_me_venda()

class Command_ME_LISTA(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_me_lista()

class Command_ME_VOLTAR(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_me_voltar()


class Command_MAE_TIPODECONTRATO(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_mae_tipodecontrato()

class Command_MAE_SINDICATO(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_mae_sindicato()

class Command_MAE_CONFIRMAR(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_mae_confirmar()

class Command_MAE_CANCELAR(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_mae_cancelar()


class Command_MEE_TIPODECONTRATO(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_mee_tipodecontrato()

class Command_MEE_SINDICATO(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_mee_sindicato()

class Command_MEE_CONFIRMAR(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_mee_confirmar()

class Command_MEE_CANCELAR(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_mee_cancelar()

class Command_MS_LISTA(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_ms_lista()

class Command_MS_VOLTAR(ICommand):
    def __init__(self, receiver):
        self._receiver = receiver
    def execute(self):
        self._receiver.run_command_ms_voltar()

def janela_lista_gerenciar(categoria: str,dicionario: dict):
    lista = []
    id = -1
    #Lista Geral
    if categoria == 'Geral':
        for key, employee in dicionario.items():
            lista.append(f'ID: {key} Categoria: {employee.category} Nome: {employee.name}')
    
    #Lista Horista
    elif categoria == 'Horista':
        for key, employee in dicionario.items():
            if employee.category == 'Horista':
                lista.append(f'ID: {key} Categoria: {employee.category} Nome: {employee.name}')

    #Lista Comissionado
    elif categoria == 'Comissionado':
        for key, employee in dicionario.items():
            if employee.category == 'Comissionado':
                lista.append(f'ID: {key} Categoria: {employee.category} Nome: {employee.name}')

    #Lista Comissionado
    elif categoria == 'Afiliados':
        for key, employee in dicionario.items():
            lista.append(f'SID: {key} Categoria: {employee.category} Nome: {employee.name}')


    layout_lista = [
        [sg.Listbox(values= lista, size=(60,12),key='L-LISTA', enable_events=True)],
        [sg.Button('Voltar', key='L-VOLTAR')]
    ]
    frame_geral = [[sg.Frame(title='',size=(12,12),layout=[ [sg.Button('Editar\nDetalhes do\nEmpregado', key='L-EDITAR', size=(12,3))],
                                                            [sg.Button('Demitir\nEmpregado', key='L-REMOVER', size=(12,3))]])]]
    frame_horista = [[sg.Frame(title='',size=(12,12),layout=[   [sg.Button('Lançar Cartão de Ponto', key='L-PONTO', size=(12,3))]
                                                                ])]]
    frame_comissionado = [[sg.Frame(title='',size=(12,12),layout=[  [sg.Button('Lançar Resultado de Venda', key='L-VENDA', size=(12,3))]
                                                                    ])]]
    frame_afiliados = [[sg.Frame(title='',size=(12,12),layout=[  [sg.Button('Lançar Taxa de Serviço', key='L-TAXA', size=(12,3))]
                                                                    ])]]
    layout_final = [[
        sg.Column(layout_lista,key='-LayoutLista-',visible=True),
        sg.Column(frame_geral,key='-LayoutGeral-',visible=(categoria == 'Geral')),
        sg.Column(frame_horista,key='-LayoutHorista-',visible=(categoria == 'Horista')),
        sg.Column(frame_comissionado,key='-LayoutComissionado-',visible=(categoria == 'Comissionado')),
        sg.Column(frame_afiliados,key='-LayoutAfiliados-',visible=(categoria == 'Afiliados'))
    ]]
    window = sg.Window('Listagem de '+categoria, layout=layout_final, modal=True)
    while True:
        evento, valores = window.read()
        if evento == "Exit" or evento == sg.WIN_CLOSED or evento == 'L-VOLTAR':
            id = -1
            break
        
        elif evento != 'L-LISTA':
            if len(valores['L-LISTA']) != 0:
                id = re.findall('\d+', valores['L-LISTA'][0])[0]
                break
            else:
                sg.popup('Nenhum empregado selecionado.', title='')
    print(evento, evento[:2])
    window.close()
    return (int(id), evento)

def CheckPassword(user, password):
    return user == 'admin' and password == 'admin'

def janela_calculo(employee, tipolayout):
    totaltime = 0
    
    if tipolayout == 'Ponto':
        titulo = 'Lançar Cartão de Ponto'
        layout = [  [sg.Text(text=f'Funcionário: {employee.name}\nID: {employee.id}', size=(30,2),justification='left')],
                    [sg.Frame('Cartão de Ponto',[  [sg.Text('Entrada', size=(7,1)),sg.Input(size=(2,1),key='C-ENTRADAHORA'),sg.Text(':'),sg.Input(size=(2,1),key='C-ENTRADAMINUTO')],
                                    [sg.Text('Saída', size=(7,1)),sg.Input(size=(2,1),key='C-SAIDAHORA'),sg.Text(':'),sg.Input(size=(2,1),key='C-SAIDAMINUTO')]])],
                    [sg.Button('Voltar', key='C-VOLTAR'), sg.Button('Confirmar', key='C-CONFIRMAR')]]
    elif tipolayout == 'Venda':
        titulo = 'Lançar Resultado de Venda'
        layout = [  [sg.Text(text=f'Funcionário: {employee.name}\nID: {employee.id}', size=(30,2),justification='left')],
                    [sg.Frame('Resultado de Venda',[[sg.Text('Valor da Venda', size=(14,1)),sg.Input(size=(16,1),key='C-VALOR')]])],
                    [sg.Button('Voltar', key='C-VOLTAR'), sg.Button('Confirmar', key='C-CONFIRMAR')]]
    elif tipolayout == 'Taxa':
        titulo = 'Lançar Taxa de Serviço'
        layout = [  [sg.Text(text=f'Funcionário: {employee.name}\nSID: {employee.sid}', size=(30,2),justification='left')],
                    [sg.Frame('Serviço',[[sg.Text('Valor da Taxa', size=(14,1)),sg.Input(size=(16,1),key='C-VALOR')]])],
                    [sg.Button('Voltar', key='C-VOLTAR'), sg.Button('Confirmar', key='C-CONFIRMAR')]]
    
    window = sg.Window(titulo, layout, modal=True)
    while True:
        evento, valores = window.read()
        if evento == 'Exit' or evento == sg.WIN_CLOSED or evento == 'C-VOLTAR':
            break
        elif evento == 'C-CONFIRMAR' and tipolayout == 'Ponto':
            if valores['C-ENTRADAHORA'] == '' or valores['C-ENTRADAMINUTO'] == '' or valores['C-SAIDAHORA'] == '' or valores['C-SAIDAMINUTO'] == '':
                sg.popup('Preencha todos os campos!')
                continue
            Bhour   = int(valores['C-ENTRADAHORA'])
            Bmin    = int(valores['C-ENTRADAMINUTO'])
            Ehour   = int(valores['C-SAIDAHORA'])
            Emin    = int(valores['C-SAIDAMINUTO'])
            if (Bhour < 0 or Bhour > 23) or (Bmin<0 or Bmin>59):
                sg.popup('ERRO: Valor da Hora de Entrada inválido.', title='ERRO')
            elif (Ehour < 0 or Ehour > 23) or (Emin<0 or Emin>59):
                sg.popup('ERRO: Valor da Hora de Saída inválido.', title='ERRO')
            else:
                totaltime = ((Ehour*60 + Emin) - (Bhour*60 + Bmin))/60
                if totaltime < 0:
                    sg.popup('ERRO: A hora da Entrada não pode ser posterior a hora da Saída.', title='ERRO')
                    continue
                elif totaltime > 8:
                    totaltime = (totaltime-8)*1.5 + 8
                break
        elif evento == 'C-CONFIRMAR' and tipolayout == 'Venda':
            totaltime = int(valores['C-VALOR'])
            if totaltime > 0:
                totaltime = totaltime * (employee.commission/100)
                break
            else:
                sg.popup('ERRO: O valor da venda não pode ser negativo.', title='ERRO')
        elif evento == 'C-CONFIRMAR' and tipolayout == 'Taxa':
            totaltime = int(valores['C-VALOR'])
            if totaltime > 0:
                break
            else:
                sg.popup('ERRO: O valor da taxa não pode ser negativo.', title='ERRO')
    window.close()
    return totaltime
