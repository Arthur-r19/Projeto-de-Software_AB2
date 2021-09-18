# Projeto de Software - Refactoring
Etapa de refatoração do código do projeto de folha de pagamento.

# Code Smells
Identifiquei os seguintes code smells ao longo da primeira e da segunda etapada do projeto:
1. Duplicated Code
2. Dead Code
3. Large Class
4. Switch Statements
5. Comments 

# Refactoring
Para resolver os codes foi utilizado:
- **Extract Class**, **Move Field** e **Move Method**: Para subdividir a classe dos empregados em subclasses e agrupar as propriedades e métodos em suas respectivas subclasses, além de criar a classe para lidar com a criação dos empregados.
- **Command**: Para lidar com toda a interface gráfica, foi utilizado essa pattern para lidar com os diversos botões, separando-os em classes de comando.
- **Extract Method**: Os códigos duplicados foram agrupados em métodos para auxiliar na manutenção do código e para ajudar a criar a classe de controle do layout gráfico.
- **Rename Method**: Todas os métodos foram nomeados para evitar o uso de comentários e facilitar na leitura e interpretação do código.

