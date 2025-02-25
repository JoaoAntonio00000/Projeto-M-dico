from rich.console import Console
from rich.table import Table

from criando_lista_pacientes import cadastrar
console = Console()


def menu():
    while True:
        opcao = console.input("[bold magenta][1]-Cadastrar paciente"
                              '\n[2] - Ver lista Paciente'
                              '\n[3] - Agendar Paciente'
                              '\n[4] - Cancelar Paciente'
                              '\n[0] - Sair\n'
                              "[bold cyan]Escolha uma opção: [/bold cyan]")
        if opcao == '1':
            cadastrar()
        elif opcao == '2':
            exibir_lista_medico()
        elif opcao == '3':
            exibir_lista_medico()
            excluir_medico()
        elif opcao == '4':
            atualizar_contato()
        elif opcao == '0':
            console.print("[bold cyan]Até mais![/bold cyan]")
            break
        else:
            console.print("[bold red]Valor inválido![/bold red]")

if __name__ == '__main__':
    menu()