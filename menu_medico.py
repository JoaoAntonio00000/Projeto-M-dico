from rich.console import Console
console = Console()

from criando_lista_pacientes import listar_pacientes
from criando_lista_resultado_paciente import adicionar_exames_resultados, atualizar_resultado_exame, exibir_lista_resultados, carregar_dados, salvar_dados

def buscar_pacientes_por_medico(id_medico):
    dados_resultados = carregar_dados()
    pacientes_medico = {}
    
    for resultado in dados_resultados:
        if resultado["Nome_Medico"] == id_medico:
            paciente_id = resultado["ID_PACIENTE"]
            if paciente_id not in pacientes_medico:
                pacientes_medico[paciente_id] = resultado["Nome_Paciente"]
    
    return pacientes_medico

def exibir_pacientes_medico(id_medico):
    pacientes_medico = buscar_pacientes_por_medico(id_medico)
    
    if not pacientes_medico:
        console.print("[bold red]Nenhum paciente encontrado para este médico.[/bold red]")
        return
    
    console.print("[bold cyan]Lista de Pacientes do Médico:[/bold cyan]")
    for paciente_id, nome_paciente in pacientes_medico.items():
        console.print(f"ID: {paciente_id} | Nome: {nome_paciente}")

def excluir_resultado_exame():
    dados_resultados = carregar_dados()
    
    if not dados_resultados:
        console.print("[bold red]Nenhum resultado de exame cadastrado.[/bold red]")
        return
    
    console.print("[bold cyan]Lista de Resultados de Exames:[/bold cyan]")
    for resultado in dados_resultados:
        console.print(f"ID: {resultado['ID']} | Paciente: {resultado['Nome_Paciente']} | Exame: {resultado['Exame']} | Resultado: {resultado['Resultado']}")
    
    id_exame = input("Digite o ID do exame que deseja excluir: ").strip()
    
    try:
        id_exame = int(id_exame)
    except ValueError:
        console.print("[bold red]ID inválido. Digite um número válido.[/bold red]")
        return
    
    exame_encontrado = None
    for resultado in dados_resultados:
        if resultado["ID"] == id_exame:
            exame_encontrado = resultado
            break
    
    if not exame_encontrado:
        console.print("[bold red]Exame não encontrado.[/bold red]")
        return
    
    console.print(f"[bold green]Exame encontrado: {exame_encontrado['Exame']} | Resultado: {exame_encontrado['Resultado']}[/bold green]")
    
    confirmacao = input("Tem certeza que deseja excluir este exame? (s/n): ").strip().lower()
    
    if confirmacao == 's':
        dados_resultados.remove(exame_encontrado)
        salvar_dados(dados_resultados)
        console.print("[bold green]Exame excluído com sucesso![/bold green]")
    else:
        console.print("[bold yellow]Exclusão cancelada.[/bold yellow]")

def menu_medico(id_medico):
    while True:
        opcao = console.input("[bold magenta][1]-Adicionar Resultado de Exames"
                              '\n[2] - Ver lista de Pacientes'
                              '\n[3] - Atualizar Resultado de Exames'
                              '\n[4] - Excluir Resultado de Exames'
                              '\n[5] - Ver Resultados dos Meus Pacientes'
                              '\n[0] - Sair\n'
                              "[bold cyan]Escolha uma opção: [/bold cyan]")
        if opcao == '1':
            adicionar_exames_resultados()
        elif opcao == '2':
            listar_pacientes()
        elif opcao == '3':
            atualizar_resultado_exame()
        elif opcao == '4':
            excluir_resultado_exame()
        elif opcao == '5':
            exibir_pacientes_medico(id_medico)
        elif opcao == '0':
            console.print("[bold cyan]Até mais![/bold cyan]")
            break
        else:
            console.print("[bold red]Valor inválido![/bold red]")

if __name__ == '__main__':
    # Supondo que o médico logado tenha o ID 1 (você pode modificar isso para pegar o ID do médico logado)
    id_medico_logado = 1
    menu_medico(id_medico_logado)