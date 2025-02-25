from rich.console import Console
from rich.table import Table
from criando_lista_pacientes import cadastrar, listar_pacientes, modificar_dados, delet_pacientes
from agenda import agendamento  

console = Console()

def menu():
    while True:
        opcao = console.input("[bold magenta][1]-Cadastrar paciente"
                              '\n[2] - Ver lista de Pacientes'
                              '\n[3] - Agendar Consulta'
                              '\n[4] - Cancelar Consulta'
                              '\n[5] - Atualizar Dados do Paciente'
                              '\n[6] - Deletar Paciente'
                              '\n[0] - Sair\n'
                              "[bold cyan]Escolha uma opção: [/bold cyan]")
        if opcao == '1':
            cadastrar()  # Cadastrar novo paciente
        elif opcao == '2':
            listar_pacientes()  # Listar todos os pacientes
        elif opcao == '3':
            agendamento()  # Agendar consulta para um paciente
        elif opcao == '4':
            cancelar_consulta()  # Função para cancelar consulta (precisa ser implementada)
        elif opcao == '5':
            modificar_dados()  # Atualizar dados de um paciente
        elif opcao == '6':
            delet_pacientes()  # Deletar um paciente do sistema
        elif opcao == '0':
            console.print("[bold cyan]Até mais![/bold cyan]")
            break
        else:
            console.print("[bold red]Valor inválido![/bold red]")

# Função para cancelar consulta (precisa ser implementada)
def cancelar_consulta():
    console.print("[bold yellow]Função de cancelar consulta ainda não implementada.[/bold yellow]")
    # Aqui você pode implementar a lógica para cancelar uma consulta.
    # Seria necessário acessar a agenda.json, localizar a consulta e removê-la.

if __name__ == '__main__':
    menu()