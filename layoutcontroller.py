class LayoutController:
    def __init__(self, layout) -> None:
        self.LayoutAtivo = layout

    def get_layout(self) -> str:
        return self.LayoutAtivo
        
    def set_layout(self, layout) -> None:
        self.LayoutAtivo = layout

    def is_layout_active(self, layout) -> bool:
        return self.LayoutAtivo == layout
    
    def update_window_layout(self, janela, layoutNovo) -> None:
        janela[self.get_layout()].update(visible=False)
        self.set_layout(layoutNovo)
        janela[layoutNovo].update(visible=True)

    def reset_employee_menu(self, janela, keyprefix) -> None:
        janela[keyprefix+'-NOME'].update('')
        janela[keyprefix+'-ENDERECO'].update('')
        janela[keyprefix+'-TIPODECONTRATO'].update('Assalariado')
        janela[keyprefix+'-SINDICATO'].update(False)
        janela[keyprefix+'-VALORSINDICATO'].update('')
        janela[keyprefix+'-VALORSINDICATO'].update(disabled=True)
        janela[keyprefix+'-VALORSALARIO'].update('')
        janela[keyprefix+'-VALORCOMISSAO'].update('')
        janela[keyprefix+'-VALORCOMISSAO'].update(disabled=True)
    
    def import_employee_menu(self, janela, employee):
        janela['MEE-NOME'].update(employee.name)
        janela['MEE-ENDERECO'].update(employee.adress)
        janela['MEE-TIPODECONTRATO'].update(employee.category)
        janela['MEE-VALORCOMISSAO'].update('')
        janela['MEE-VALORCOMISSAO'].update(disabled=True)
        janela['MEE-TEXTOSALARIO'].update('Salário Mensal')

        if employee.category == 'Assalariado':
            janela['MEE-VALORSALARIO'].update(employee.salary)

        elif employee.category == 'Comissionado':
            janela['MEE-VALORSALARIO'].update(employee.salary)
            janela['MEE-VALORCOMISSAO'].update(employee.commission)
            janela['MEE-VALORCOMISSAO'].update(disabled=False)

        elif employee.category == 'Horista':
            janela['MEE-TEXTOSALARIO'].update('Valor da Hora')
            janela['MEE-VALORSALARIO'].update(employee.wage)

        if employee.sid == -1:
            janela['MEE-SINDICATO'].update(False)
            janela['MEE-VALORSINDICATO'].update('')
            janela['MEE-VALORSINDICATO'].update(disabled=True)
        else:
            janela['MEE-SINDICATO'].update(True)
            janela['MEE-VALORSINDICATO'].update(employee.mfee)
            janela['MEE-VALORSINDICATO'].update(disabled=False)