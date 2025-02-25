from criando_lista_medicos import adicionar_medico, exibir_lista_medico, excluir_medico, atualizar_contato
from criando_lista_secretaria import adicionar_secretaria, exibir_lista_secretarias,excluir_secretaria,atualizar_secretaria

from rich.console import Console
console = Console()

def menu():
    while True:
        opcao = console.input("[bold magenta][1]-Adicionar médico"
                              '\n[2] - Ver lista de médicos'
                              '\n[3] - Excluir médico'
                              '\n[4] - Atualizar médico'
                              '\n[5] - Excluir Secretaria'
                              '\n[6] - Atualizar Secretaria'
                              '\n[7] - Adicionar Secretaria'
                              '\n[8] - Exibir lista de Secretarias'
                              '\n[0] - Sair\n'
                              "[bold cyan]Escolha uma opção: [/bold cyan]")
        if opcao == '1':
            adicionar_medico()
        elif opcao == '2':
            exibir_lista_medico()
        elif opcao == '3':
            exibir_lista_medico()
            excluir_medico()
        elif opcao == '4':
            atualizar_contato()
        elif opcao =='5':
            exibir_lista_secretarias()
            excluir_secretaria()
        elif opcao == '6':
            atualizar_secretaria()
        elif opcao == '7':
            adicionar_secretaria()
        elif opcao == '8':
            exibir_lista_secretarias()
        elif opcao == '0':
            console.print("[bold cyan]Até mais![/bold cyan]")
            break
        else:
            console.print("[bold red]Valor inválido![/bold red]")

if __name__ == '__main__':
    menu()