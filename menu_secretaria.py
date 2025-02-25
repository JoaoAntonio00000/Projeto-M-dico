import json
import os
from rich.console import Console
from validacao_de_dados import validar_email, validar_cpf_secretaria, validar_data

console = Console()

caminho_arquivo = "lista_secretaria.json"

# Verificar se o arquivo da lista de secretárias existe
def verificar_se_arquivo_existe():
    if not os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump([], arquivo, indent=4, ensure_ascii=False)
        console.print("[bold green]Arquivo criado com sucesso![/bold green]")
    else:
        console.print("[bold green]Arquivo já existe.[/bold green]")

verificar_se_arquivo_existe()

# Carregar os dados da lista de secretárias
def carregar_dados():
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        console.print("[bold red]Arquivo não encontrado ou corrompido. Retornando lista vazia.[/bold red]")
        return []

# Salvar os dados e alterações feitas na lista
def salvar_dados(dados):
    try:
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        console.print("[bold green]Dados salvos com sucesso![/bold green]")
    except IOError as e:
        console.print(f"[bold red]Erro ao salvar dados: {e}[/bold red]")

dados_secretaria = carregar_dados()

# Dando ID para as secretárias
if dados_secretaria:
    secretaria_id = max(usuario["ID"] for usuario in dados_secretaria) + 1
else:
    secretaria_id = 1

# Adicionar secretária à lista
def adicionar_secretaria():
    global secretaria_id
    while True:
        nome = console.input("[bold yellow]Informe o nome da Secretária: [/bold yellow]").strip()
        
        while True:
            cpf = console.input("[bold yellow]Informe o CPF da Secretária: [/bold yellow]").strip()
            if validar_cpf_secretaria(cpf):
                break
            else:
                console.print("[bold red]CPF inválido ou já cadastrado. Tente novamente.[/bold red]")
        
        while True:
            data_nascimento = console.input("[bold yellow]Digite a data de nascimento (DD/MM/AAAA): [/bold yellow]").strip()
            if validar_data(data_nascimento):
                break
            else:
                console.print("[bold red]Data de nascimento inválida! Tente novamente.[/bold red]")
        
        while True:
            email = console.input("[bold yellow]Informe o e-mail da Secretária: [/bold yellow]").strip()
            if validar_email(email):
                break
            else:
                console.print("[bold red]E-mail inválido! Digite novamente.[/bold red]")
        
        while True:
            genero = console.input("[bold yellow]Informe o gênero da Secretária (M/F): [/bold yellow]").strip().upper()
            if genero in ["M", "F"]:
                break
            else:
                console.print("[bold red]Gênero inválido! Use 'M' para masculino ou 'F' para feminino.[/bold red]")
        
        novo_usuario = {
            "ID": secretaria_id,
            "Nome": nome,
            "Data de Nascimento": data_nascimento,  # Chave corrigida
            "E-mail": email,
            "CPF": cpf,
            "Genero": genero
        }
        dados_secretaria.append(novo_usuario)
        secretaria_id += 1

        continuar = console.input("[bold yellow]Deseja continuar? (S/N): [/bold yellow]").strip().lower()
        if continuar == "n":
            salvar_dados(dados_secretaria)
            break

# Atualizar secretária na lista
def atualizar_secretaria():
    buscar = console.input("[bold yellow]Informe o ID da Secretária que deseja atualizar: [/bold yellow]").strip()

    try:
        buscar = int(buscar)
    except ValueError:
        console.print("[bold red]Erro: O ID deve ser um número válido![/bold red]")
        return

    for usuario in dados_secretaria:
        if usuario["ID"] == buscar:
            novo_nome = console.input("[bold yellow]Informe o novo nome da Secretária: [/bold yellow]").strip()
            
            while True:
                novo_email = console.input("[bold yellow]Informe o novo e-mail da Secretária: [/bold yellow]").strip()
                if not novo_email:  # Se o campo estiver vazio, mantém o atual
                    novo_email = usuario['E-mail']
                    break
                elif validar_email(novo_email):
                    break
                else:
                    console.print("[bold red]E-mail inválido! Digite novamente.[/bold red]")
            
            while True:
                nova_data_nascimento = console.input("[bold yellow]Informe a nova data de nascimento (DD/MM/AAAA): [/bold yellow]").strip()
                if not nova_data_nascimento:  # Se o campo estiver vazio, mantém o atual
                    nova_data_nascimento = usuario['Data de Nascimento']
                    break
                elif validar_data(nova_data_nascimento):
                    break
                else:
                    console.print("[bold red]Data de nascimento inválida! Tente novamente.[/bold red]")
            
            usuario["Nome"] = novo_nome if novo_nome else usuario['Nome']
            usuario["E-mail"] = novo_email if novo_email else usuario['E-mail']
            usuario["Data de Nascimento"] = nova_data_nascimento if nova_data_nascimento else usuario['Data de Nascimento']
            salvar_dados(dados_secretaria)
            console.print("[bold green]Contato atualizado com sucesso![/bold green]")
            return

    console.print("[bold red]ID não encontrado![/bold red]")

# Excluir secretária da lista
def excluir_secretaria():
    buscar = console.input("[bold yellow]Informe o ID da Secretária que deseja excluir: [/bold yellow]").strip()

    try:
        buscar = int(buscar)
    except ValueError:
        console.print("[bold red]Erro: O ID deve ser um número válido![/bold red]")
        return

    for usuario in dados_secretaria:
        if usuario["ID"] == buscar:
            console.print(f"[bold red]Tem certeza que deseja excluir a Secretária {usuario['Nome']}? (S/N)[/bold red]")
            confirmar = console.input().strip().lower()

            if confirmar == "s":
                dados_secretaria.remove(usuario)
                salvar_dados(dados_secretaria)
                console.print("[bold green]Contato excluído com sucesso![/bold green]")
            else:
                console.print("[bold yellow]Operação cancelada.[/bold yellow]")
            return

    console.print("[bold red]ID não encontrado![/bold red]")

# Exibir lista de secretárias
def exibir_lista_secretaria():
    from rich.table import Table
    if not dados_secretaria:
        console.print("[bold red]Nenhuma Secretária encontrada![/bold red]")
        return

    tabela = Table(title="Lista de Secretárias", show_lines=True)
    tabela.add_column("ID", justify="center", style="bold cyan")
    tabela.add_column("Nome", justify="left", style="bold yellow")
    tabela.add_column("E-mail", justify="left", style="bold green")
    tabela.add_column("Data de Nascimento", justify="left", style="bold green")  # Chave corrigida
    tabela.add_column("Gênero", justify="left", style="bold green")
    tabela.add_column("CPF", justify="left", style="bold magenta")

    for usuario in dados_secretaria:
        tabela.add_row(
            str(usuario["ID"]),
            usuario["Nome"],
            usuario["E-mail"],
            usuario["Data de Nascimento"],  # Chave corrigida
            usuario['Genero'],
            usuario['CPF']
        )

    console.print(tabela)

# Menu principal
def menu():
    while True:
        opcao = console.input("[bold magenta][1]-Adicionar Secretária"
                              '\n[2] - Ver lista de Secretárias'
                              '\n[3] - Excluir Secretária'
                              '\n[4] - Atualizar Secretária'
                              '\n[0] - Sair\n'
                              "[bold cyan]Escolha uma opção: [/bold cyan]")
        if opcao == '1':
            adicionar_secretaria()
        elif opcao == '2':
            exibir_lista_secretaria()
        elif opcao == '3':
            exibir_lista_secretaria()
            excluir_secretaria()
        elif opcao == '4':
            atualizar_secretaria()
        elif opcao == '0':
            console.print("[bold cyan]Até mais![/bold cyan]")
            break
        else:
            console.print("[bold red]Valor inválido![/bold red]")

if __name__ == '__main__':
    menu()