from PySimpleGUI import PySimpleGUI as sg
from datetime import datetime as dt
from company import Company as company
from syndicate import Syndicate as syndicate
from layoutcontroller import LayoutController
from employee import HourlyEmployee as Hemployee, SalaryEmployee as Semployee, CommissionedEmployee as Cemployee
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
        [sg.Button('Entrar', key='entrar')]
    ]
    # Janela
    return sg.Window('Tela de Login', layoutLogin, finalize=True)

def janela_principal():
    data = dt.now()
    layoutMenuPrincipal = [
        [sg.Text('Sistema de Gerenciamento Empresarial', justification='center', size=(30,1))],
        [sg.Button('Menu da Empresa',key='MP-EMPRESA' ,size=(30,1))],
        [sg.Button('Menu do Sindicato',key='MP-SINDICATO', size=(30,1))],
        #[sg.Button('Pagamentos', size=(30,1))],
        [sg.Text(f'Hoje é {data.day}/{data.month}/{data.year}', justification='center', size=(30,1))]
    ]
    layoutMenuEmpresa = [
        [sg.Text('Gerenciamento de Empregados', justification='center', size=(30,1))],
        [sg.Button('Adicionar Empregado', key='ME-ADICIONAR', size=(30,1))],
        #[sg.Button('Remover Empregado', key='ME-REMOVER')],
        [sg.Button('Lançar Cartão de Ponto', key='ME-PONTO', size=(30,1))],
        [sg.Button('Registrar Resultado de Venda', key='ME-VENDA', size=(30,1))],
        [sg.Button('Lista de Empregados', key='ME-LISTA', size=(30,1))],
        [sg.Button('Voltar', key='ME-VOLTAR')]
    ]
    layoutMenuSindicato = [
        [sg.Text('Gerenciamento do Sindicato', justification='center', size=(30,1))],
        #[sg.Button('Taxa de Serviço', key='MS-TAXA', size=(30,1))],
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
            print('clicou?')
            if len(valores['L-LISTA']) != 0:
                id = re.findall('\d+', valores['L-LISTA'][0])[0]
                break
            else:
                sg.popup('Nenhum empregado selecionado.', title='')
    print(evento, evento[:2])
    window.close()
    return (int(id), evento)

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
###############################################################################

# Ready

janelaLogin = janela_login()
janelaPrincipal = None
lc = LayoutController(None)
Empresa = company()
Sindicato = syndicate()
selectedId = -1
selectedSid = -1


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
    print(janela==janelaPrincipal,'|',evento)
# FECHAR JANELA
    if evento == "Exit" or evento == sg.WIN_CLOSED:
        print(f'Fechando janela {janela}')
        janela.close()
        break
# TELA DE LOGIN
    elif janela == janelaLogin:
        if evento == 'entrar':
            if CheckPassword(valores['usuario'], valores['senha']):
                janela.close()
                janelaPrincipal = janela_principal()
                lc.set_layout('-LayoutMenuPrincipal-')
            else:
                sg.popup('Usuário ou senha incorretos',title='Erro no Login')

#######################################################################################################

# MENU PRINCIPAL
    elif janela == janelaPrincipal and lc.is_layout_active('-LayoutMenuPrincipal-'):
        if evento == 'MP-EMPRESA':
            lc.update_window_layout(janela,'-LayoutMenuEmpresa-')

        elif evento == 'MP-SINDICATO':
            lc.update_window_layout(janela,'-LayoutMenuSindicato-')

        #elif evento == 'Pagamentos':
        #    lc.update_window_layout(janela,'-LayoutMenuPagamento-')
            


#######################################################################################################

# MENU EMPREGADOS
    elif janela == janelaPrincipal and lc.is_layout_active('-LayoutMenuEmpresa-'):
        if evento == 'ME-ADICIONAR':
            lc.update_window_layout(janela, '-LayoutAdicionarEmpregado-')

        elif evento == 'ME-PONTO':
            selectedId, chave = janela_lista_gerenciar('Horista', Empresa.employeesList)
            if selectedId != -1 and chave == 'L-PONTO':
                selectedEmployee = Empresa.employeesList.get(selectedId)
                #sg.popup(f'Ponto do funcionário {selectedEmployee.name} registrado com sucesso.')
                workedtime = janela_calculo(selectedEmployee, 'Ponto')
                selectedEmployee.workedtime += workedtime
                sg.popup(f'Ponto de {workedtime} horas registrado com sucesso para o seguinte funcionário:\nFuncionário {selectedEmployee.name}\nID: {selectedEmployee.id}\nHoras Acumuladas: {selectedEmployee.workedtime} Horas')


        elif evento == 'ME-VENDA':
            selectedId, chave = janela_lista_gerenciar('Comissionado', Empresa.employeesList)
            if selectedId != -1 and chave == 'L-VENDA':
                selectedEmployee = Empresa.employeesList.get(selectedId)
                #sg.popup(f'Venda do funcionário {selectedEmployee.name} registrada com sucesso.')
                valorvenda = janela_calculo(selectedEmployee, 'Venda')
                selectedEmployee.comvalue += valorvenda
                sg.popup(f'Comissão de R$ {valorvenda} registrada com sucesso para o seguinte funcionário:\nFuncionário {selectedEmployee.name}\nID: {selectedEmployee.id}\nComissao Acumulada: R$ {selectedEmployee.comvalue}')

        elif evento == 'ME-LISTA':
            selectedId, chave = janela_lista_gerenciar('Geral', Empresa.employeesList)
            if selectedId != -1 and chave == 'L-EDITAR':
                selectedEmployee = Empresa.employeesList.get(selectedId)
                selectedSid = selectedEmployee.sid
                lc.import_employee_menu(janela, selectedEmployee)
                lc.update_window_layout(janela, '-LayoutEditarEmpregado-')
            elif selectedId != -1 and chave == 'L-REMOVER':
                selectedEmployee = Empresa.employeesList.get(selectedId)
                selectedSid = selectedEmployee.sid
                Empresa.remove_employee(selectedId)
                if selectedSid != -1:
                    Sindicato.remove_affiliate(selectedSid)
                sg.popup(f'Empregado {selectedEmployee.name} demitido!')
            else:
                pass
            continue

        elif evento == 'ME-VOLTAR':
            print('voltando?')
            lc.update_window_layout(janela, '-LayoutMenuPrincipal-')



#######################################################################################################

## SUB MENU ADICIONAR EMPREGADO
    elif janela == janelaPrincipal and lc.is_layout_active('-LayoutAdicionarEmpregado-'):
        if evento == 'MAE-TIPODECONTRATO':
            if valores['MAE-TIPODECONTRATO'] == 'Comissionado':
                janela['MAE-TEXTOSALARIO'].update('Salário Mensal')
                janela['MAE-VALORCOMISSAO'].update(disabled=False)
            
            elif valores['MAE-TIPODECONTRATO'] == 'Horista':
                janela['MAE-TEXTOSALARIO'].update('Valor da Hora')
                janela['MAE-VALORCOMISSAO'].update('')
                janela['MAE-VALORCOMISSAO'].update(disabled=True)
            else:
                janela['MAE-TEXTOSALARIO'].update('Salário Mensal')
                janela['MAE-VALORCOMISSAO'].update('')
                janela['MAE-VALORCOMISSAO'].update(disabled=True)

        elif evento == 'MAE-SINDICATO':
            if valores['MAE-SINDICATO']:
                janela['MAE-VALORSINDICATO'].update(disabled=False)
            else:
                janela['MAE-VALORSINDICATO'].update('')
                janela['MAE-VALORSINDICATO'].update(disabled=True)

        elif evento == 'MAE-CONFIRMAR':
            #verificar se os campos estão preenchidos
            if valores['MAE-NOME'] == '' or valores['MAE-ENDERECO'] == '':
                sg.popup('Preencha todos os Dados Pessoais!', title='Dados Incompletos')
            
            elif valores['MAE-VALORSALARIO'] == '':
                sg.popup('Preencha todos os Detalhes do Contrato!', title='Dados Incompletos')

            elif valores['MAE-TIPODECONTRATO'] == 'Comissionado' and valores['MAE-VALORCOMISSAO'] == '':
                sg.popup('Preencha todos os Detalhes do Contrato!', title='Dados Incompletos')

            elif valores['MAE-SINDICATO'] and valores['MAE-VALORSINDICATO'] == '':
                sg.popup('Preencha todos os Detalhes do Contrato!', title='Dados Incompletos')

            else:
                if valores['MAE-TIPODECONTRATO'] == 'Horista':
                    newemployee = Hemployee(valores['MAE-NOME'], valores['MAE-ENDERECO'], valores['MAE-TIPODECONTRATO'], valores['MAE-VALORSALARIO'])
                elif valores['MAE-TIPODECONTRATO'] == 'Assalariado':
                    newemployee = Semployee(valores['MAE-NOME'], valores['MAE-ENDERECO'], valores['MAE-TIPODECONTRATO'], valores['MAE-VALORSALARIO'])
                elif valores['MAE-TIPODECONTRATO'] == 'Comissionado':  
                    newemployee = Cemployee(valores['MAE-NOME'], valores['MAE-ENDERECO'], valores['MAE-TIPODECONTRATO'], valores['MAE-VALORSALARIO'], valores['MAE-VALORCOMISSAO'])
                
                Empresa.add_employee(newemployee)
                if valores['MAE-SINDICATO']:
                    newemployee.mfee = int(valores['MAE-VALORSINDICATO'])
                    Sindicato.add_affiliate(newemployee)
                
                sg.popup(f"Funcionário {valores['MAE-NOME']} adicionado com sucesso!\nID: {newemployee.id}", title='Cadastro Concluído')
                lc.reset_employee_menu(janela,'MAE')
                lc.update_window_layout(janela, '-LayoutMenuEmpresa-')


        elif evento == 'MAE-CANCELAR':
            lc.reset_employee_menu(janela,'MAE')
            lc.update_window_layout(janela, '-LayoutMenuEmpresa-')

#######################################################################################################

## SUB MENU EDITAR EMPREGADO

    elif janela == janelaPrincipal and lc.is_layout_active('-LayoutEditarEmpregado-'):
        if evento == 'MEE-TIPODECONTRATO':
            if valores['MEE-TIPODECONTRATO'] == 'Comissionado':
                janela['MEE-TEXTOSALARIO'].update('Salário Mensal')
                janela['MEE-VALORCOMISSAO'].update(disabled=False)
            
            elif valores['MEE-TIPODECONTRATO'] == 'Horista':
                janela['MEE-TEXTOSALARIO'].update('Valor da Hora')
                janela['MEE-VALORCOMISSAO'].update('')
                janela['MEE-VALORCOMISSAO'].update(disabled=True)
            else:
                janela['MEE-TEXTOSALARIO'].update('Salário Mensal')
                janela['MEE-VALORCOMISSAO'].update('')
                janela['MEE-VALORCOMISSAO'].update(disabled=True)

        elif evento == 'MEE-SINDICATO':
            if valores['MEE-SINDICATO']:
                janela['MEE-VALORSINDICATO'].update(disabled=False)
            else:
                janela['MEE-VALORSINDICATO'].update('')
                janela['MEE-VALORSINDICATO'].update(disabled=True)

        elif evento == 'MEE-CONFIRMAR':
            #verificar se os campos estão preenchidos
            if valores['MEE-NOME'] == '' or valores['MEE-ENDERECO'] == '':
                sg.popup('Preencha todos os Dados Pessoais!', title='Dados Incompletos')
            
            elif valores['MEE-VALORSALARIO'] == '':
                sg.popup('Preencha todos os Detalhes do Contrato!', title='Dados Incompletos')

            elif valores['MEE-TIPODECONTRATO'] == 'Comissionado' and valores['MEE-VALORCOMISSAO'] == '':
                sg.popup('Preencha todos os Detalhes do Contrato!', title='Dados Incompletos')

            elif valores['MEE-SINDICATO'] and valores['MEE-VALORSINDICATO'] == '':
                sg.popup('Preencha todos os Detalhes do Contrato!', title='Dados Incompletos')


            else:
                selectedEmployee = Empresa.employeesList.get(selectedId)
                if valores['MEE-TIPODECONTRATO'] == 'Horista':
                    editemployee = Hemployee(valores['MEE-NOME'], valores['MEE-ENDERECO'], valores['MEE-TIPODECONTRATO'], valores['MEE-VALORSALARIO'])
                    if selectedEmployee.category == 'Horista':
                        editemployee.workedtime = selectedEmployee.workedtime

                elif valores['MEE-TIPODECONTRATO'] == 'Assalariado':
                    editemployee = Semployee(valores['MEE-NOME'], valores['MEE-ENDERECO'], valores['MEE-TIPODECONTRATO'], valores['MEE-VALORSALARIO'])

                elif valores['MEE-TIPODECONTRATO'] == 'Comissionado': 
                    editemployee = Cemployee(valores['MEE-NOME'], valores['MEE-ENDERECO'], valores['MEE-TIPODECONTRATO'], valores['MEE-VALORSALARIO'], valores['MEE-VALORCOMISSAO'])

                editemployee.id = selectedId
                Empresa.edit_employee(selectedId, editemployee)
                if valores['MEE-SINDICATO'] and selectedSid != -1:
                    editemployee.sid = selectedSid
                    editemployee.mfee = int(valores['MEE-VALORSINDICATO'])
                    Sindicato.edit_affiliate(selectedSid, editemployee)

                elif valores['MEE-SINDICATO'] and selectedSid == -1:
                    editemployee.mfee = int(valores['MEE-VALORSINDICATO'])
                    Sindicato.add_affiliate(editemployee)
                
                elif not valores['MEE-SINDICATO'] and selectedSid != -1:
                    Sindicato.remove_affiliate(selectedSid)
                
                else:
                    pass
                
                print(editemployee)
                
                sg.popup(f"Funcionário alterado para {editemployee.name} com sucesso!\nID: {editemployee.id}", title='Edição Concluído')
                selectedId = -1
                selectedSid = -1
                lc.reset_employee_menu(janela,'MEE')
                lc.update_window_layout(janela, '-LayoutMenuEmpresa-')


        elif evento == 'MEE-CANCELAR':
            sg.popup('Nenhum detalhe foi alterado.', title='')
            selectedId = -1
            selectedSid = -1
            lc.reset_employee_menu(janela,'MEE')
            lc.update_window_layout(janela, '-LayoutMenuEmpresa-')


#######################################################################################################

# MENU SINDICATO
    elif janela == janelaPrincipal and lc.is_layout_active('-LayoutMenuSindicato-'):
        
        if evento == 'MS-LISTA':
            selectedSid, chave = janela_lista_gerenciar('Afiliados', Sindicato.affiliatesList)
            if selectedSid != -1 and chave == 'L-TAXA':
                selectedEmployee = Sindicato.affiliatesList.get(selectedSid)
                valortaxa = janela_calculo(selectedEmployee, 'Taxa')
                selectedEmployee.xfee += valortaxa
                sg.popup(f'Taxa de R$ {valortaxa} registrada com sucesso para o seguinte funcionário:\nFuncionário: {selectedEmployee.name}\nSID: {selectedEmployee.sid}\nTotal Pendente: R$ {selectedEmployee.xfee}')
            pass
        
        
        elif evento == 'MS-VOLTAR':
            lc.update_window_layout(janela, '-LayoutMenuPrincipal-')


#######################################################################################################

# MENU PAGAMENTO
    elif janela == janelaPrincipal and lc.is_layout_active('-LayoutMenuPagamento-'):
        if evento[0:6] == 'voltar':
            lc.update_window_layout(janela, '-LayoutMenuPrincipal-')
