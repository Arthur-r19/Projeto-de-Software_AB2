from commandpattern import Command_MAE_CANCELAR, Command_MAE_CONFIRMAR, Command_MAE_SINDICATO, Command_MAE_TIPODECONTRATO, Command_ME_ADICIONAR, Command_ME_LISTA, Command_ME_PONTO, Command_ME_VENDA, Command_ME_VOLTAR, Command_MEE_CANCELAR, Command_MEE_CONFIRMAR, Command_MEE_SINDICATO, Command_MEE_TIPODECONTRATO, Command_MP_EMPRESA, Command_MP_SINDICATO, Command_MS_LISTA, Command_MS_VOLTAR, Invoker, Receiver
from employeefactory import EmployeeFactory
from PySimpleGUI import PySimpleGUI as sg
from datetime import datetime as dt
from company import Company as company
from syndicate import Syndicate as syndicate
from layoutcontroller import LayoutController
from hourlyemployee import HourlyEmployee as Hemployee
from commissionedemployee import CommissionedEmployee as Cemployee
from salaryemployee import SalaryEmployee as Semployee
import re

#Funções
def CheckPassword(user, password):
    return user == 'admin' and password == 'admin'


#Janelas
def janela_login():
    #Theme
    sg.theme("Reddit")
    # Layout
    layoutLogin = [
        [sg.Text('Usuário\t'), sg.Input(key='usuario',size=(20,1))],
        [sg.Text('Senha\t'), sg.Input(key='senha', password_char='*',size=(20,1))],
        [sg.Checkbox('Salvar o login?')],
        [sg.Button('Entrar', key='LOGIN-ENTRAR')]
    ]
    # Janela
    return sg.Window('Tela de Login', layoutLogin, finalize=True)

def janela_principal():
    data = dt.now()
    layoutMenuPrincipal = [
        [sg.Text('Sistema de Gerenciamento Empresarial', justification='center', size=(30,1))],
        [sg.Button('Menu da Empresa',key='MP-EMPRESA' ,size=(30,1))],
        [sg.Button('Menu do Sindicato',key='MP-SINDICATO', size=(30,1))],
        [sg.Text(f'Hoje é {data.day}/{data.month}/{data.year}', justification='center', size=(30,1))]
    ]
    layoutMenuEmpresa = [
        [sg.Text('Gerenciamento de Empregados', justification='center', size=(30,1))],
        [sg.Button('Adicionar Empregado', key='ME-ADICIONAR', size=(30,1))],
        [sg.Button('Lançar Cartão de Ponto', key='ME-PONTO', size=(30,1))],
        [sg.Button('Registrar Resultado de Venda', key='ME-VENDA', size=(30,1))],
        [sg.Button('Lista de Empregados', key='ME-LISTA', size=(30,1))],
        [sg.Button('Voltar', key='ME-VOLTAR')]
    ]
    layoutMenuSindicato = [
        [sg.Text('Gerenciamento do Sindicato', justification='center', size=(30,1))],
        [sg.Button('Lista de Afiliados', key='MS-LISTA', size=(30,1))],
        [sg.Button('Voltar', key='MS-VOLTAR')]
    ]
    layoutMenuPagamento = [
        [sg.Text('Folha de Pagamento', justification='center')],
        [sg.Button('Rodar Pagamento', key='pagamento')],
        [sg.Button('Agendas de Pagamento', key='agendas')],
        [sg.Button('Voltar', key='voltar')]
    ]
    layoutAdicionarEmpregado = [
        [sg.Frame('Dados Pessoais', [
                                    [sg.Column([[sg.Text('Nome')],
                                                [sg.Text('Endereço')]]),
                                    sg.Column([ [sg.Input(size=(30,1), key='MAE-NOME',)],
                                                [sg.Input(size=(30,1), key='MAE-ENDERECO')]])]
                                    ])
        ],
        [sg.Frame('Detalhes do Contrato', [[sg.Column([ [sg.Combo(values=('Horista', 'Assalariado', 'Comissionado'), default_value='Assalariado', readonly=True, key='MAE-TIPODECONTRATO',enable_events=True)],
                                                        [sg.Text(text='Salário Mensal', key='MAE-TEXTOSALARIO')],
                                                        [sg.Text('Comissão')],
                                                        [sg.Text('Tarifa Sindical')]
                                                        ]),
                                            sg.Column([ [sg.Checkbox('Afiliado ao Sindicato', default=False, key='MAE-SINDICATO', enable_events=True)],
                                                        [sg.Input(size=(20,1),key='MAE-VALORSALARIO')],
                                                        [sg.Input(size=(20,1),key='MAE-VALORCOMISSAO', disabled=True)],
                                                        [sg.Input(size=(20,1),key='MAE-VALORSINDICATO', disabled=True)]
                                                        ])]])
        ],
        [sg.Button('Cancelar', key='MAE-CANCELAR'), sg.Button('Confirmar', key='MAE-CONFIRMAR')]
                                ]
    layoutEditarEmpregado = [
        [sg.Frame('Dados Pessoais', [
                                    [sg.Column([[sg.Text('Nome')],
                                                [sg.Text('Endereço')]]),
                                    sg.Column([ [sg.Input(size=(30,1), key='MEE-NOME',)],
                                                [sg.Input(size=(30,1), key='MEE-ENDERECO')]])]
                                    ])
        ],
        [sg.Frame('Detalhes do Contrato', [[sg.Column([ [sg.Combo(values=('Horista', 'Assalariado', 'Comissionado'), default_value='Assalariado', readonly=True, key='MEE-TIPODECONTRATO',enable_events=True)],
                                                        [sg.Text(text='Salário Mensal', key='MEE-TEXTOSALARIO')],
                                                        [sg.Text('Comissão')],
                                                        [sg.Text('Tarifa Sindical')]
                                                        ]),
                                            sg.Column([ [sg.Checkbox('Afiliado ao Sindicato', default=False, key='MEE-SINDICATO', enable_events=True)],
                                                        [sg.Input(size=(20,1),key='MEE-VALORSALARIO')],
                                                        [sg.Input(size=(20,1),key='MEE-VALORCOMISSAO', disabled=True)],
                                                        [sg.Input(size=(20,1),key='MEE-VALORSINDICATO', disabled=True)]
                                                        ])]])
        ],
        [sg.Button('Cancelar', key='MEE-CANCELAR'), sg.Button('Confirmar', key='MEE-CONFIRMAR',)]
                                ]
    layoutFinal = [
        [
            sg.Column(layoutMenuPrincipal, key='-LayoutMenuPrincipal-', visible=True),
            sg.Column(layoutMenuEmpresa, key='-LayoutMenuEmpresa-', visible=False),
            sg.Column(layoutMenuSindicato, key='-LayoutMenuSindicato-', visible=False),
            sg.Column(layoutMenuPagamento, key='-LayoutMenuPagamento-', visible=False),
            sg.Column(layoutAdicionarEmpregado, key='-LayoutAdicionarEmpregado-', visible=False),
            sg.Column(layoutEditarEmpregado, key='-LayoutEditarEmpregado-', visible=False)
        ]
    ]

    return sg.Window('Software Empresarial', layoutFinal, finalize=True)

###############################################################################

# Ready
janelaLogin = janela_login()
janelaPrincipal = None
lc = LayoutController(None)
Empresa = company()
Sindicato = syndicate()


RECEIVER = Receiver({}, None, Empresa, Sindicato, lc, -1, -1)
COMMAND_MP_EMPRESA = Command_MP_EMPRESA(RECEIVER)
COMMAND_MP_SINDICATO = Command_MP_SINDICATO(RECEIVER)

COMMAND_ME_ADICIONAR = Command_ME_ADICIONAR(RECEIVER)
COMMAND_ME_PONTO = Command_ME_PONTO(RECEIVER)
COMMAND_ME_VENDA = Command_ME_VENDA(RECEIVER)
COMMAND_ME_LISTA = Command_ME_LISTA(RECEIVER)
COMMAND_ME_VOLTAR = Command_ME_VOLTAR(RECEIVER)

COMMAND_MAE_TIPODECONTRATO = Command_MAE_TIPODECONTRATO(RECEIVER)
COMMAND_MAE_SINDICATO = Command_MAE_SINDICATO(RECEIVER)
COMMAND_MAE_CONFIRMAR = Command_MAE_CONFIRMAR(RECEIVER)
COMMAND_MAE_CANCELAR = Command_MAE_CANCELAR(RECEIVER)

COMMAND_MEE_TIPODECONTRATO = Command_MEE_TIPODECONTRATO(RECEIVER)
COMMAND_MEE_SINDICATO = Command_MEE_SINDICATO(RECEIVER)
COMMAND_MEE_CONFIRMAR = Command_MEE_CONFIRMAR(RECEIVER)
COMMAND_MEE_CANCELAR = Command_MEE_CANCELAR(RECEIVER)

COMMAND_MS_LISTA = Command_MS_LISTA(RECEIVER)
COMMAND_MS_VOLTAR = Command_MS_VOLTAR(RECEIVER)

INVOKER = Invoker()
INVOKER.register('MP-EMPRESA', COMMAND_MP_EMPRESA)
INVOKER.register('MP-SINDICATO', COMMAND_MP_SINDICATO)

INVOKER.register('ME-ADICIONAR', COMMAND_ME_ADICIONAR)
INVOKER.register('ME-PONTO', COMMAND_ME_PONTO)
INVOKER.register('ME-VENDA', COMMAND_ME_VENDA)
INVOKER.register('ME-LISTA', COMMAND_ME_LISTA)
INVOKER.register('ME-VOLTAR', COMMAND_ME_VOLTAR)

INVOKER.register('MAE-TIPODECONTRATO', COMMAND_MAE_TIPODECONTRATO)
INVOKER.register('MAE-SINDICATO', COMMAND_MAE_SINDICATO)
INVOKER.register('MAE-CONFIRMAR', COMMAND_MAE_CONFIRMAR)
INVOKER.register('MAE-CANCELAR', COMMAND_MAE_CANCELAR)

INVOKER.register('MEE-TIPODECONTRATO', COMMAND_MEE_TIPODECONTRATO)
INVOKER.register('MEE-SINDICATO', COMMAND_MEE_SINDICATO)
INVOKER.register('MEE-CONFIRMAR', COMMAND_MEE_CONFIRMAR)
INVOKER.register('MEE-CANCELAR', COMMAND_MEE_CANCELAR)

INVOKER.register('MS-LISTA', COMMAND_MS_LISTA)
INVOKER.register('MS-VOLTAR', COMMAND_MS_VOLTAR)

# Fake database
Empresa.add_employee(Hemployee('Manoel Primeiro', 'Ponta Grossa', 'Horista', 45))
Empresa.add_employee(Hemployee('Manoel Segundo', 'Ponta Grossa', 'Horista', 50))
Empresa.add_employee(Hemployee('Manoel Terceiro', 'Ponta Grossa', 'Horista', 55))
Empresa.add_employee(Cemployee('Ullyanne Espada', 'Japão', 'Comissionado', 2000, 3))
Empresa.add_employee(Cemployee('Ullyanne Escudo', 'Japão', 'Comissionado', 2500, 2))
Empresa.add_employee(Semployee('Robson Turista', 'Rio de Janeiro', 'Assalariado', 3000))

# Eventos
while True:
    janela, evento, valores = sg.read_all_windows()
    RECEIVER.dict = valores
    RECEIVER.janela = janela

    print(janela==janelaPrincipal,'|',evento)

# FECHAR JANELA
    if evento == "Exit" or evento == sg.WIN_CLOSED:
        print(f'Fechando janela {janela}')
        janela.close()
        break

# TELA DE LOGIN
    elif janela == janelaLogin:
        if evento == 'LOGIN-ENTRAR':
            if CheckPassword(valores['usuario'], valores['senha']):
                janela.close()
                janelaPrincipal = janela_principal()
                lc.set_layout('-LayoutMenuPrincipal-')
            else:
                sg.popup('Usuário ou senha incorretos',title='Erro no Login')

    INVOKER.execute(evento)