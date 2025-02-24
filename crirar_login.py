import json
import os
from rich.console import Console

console = Console()

# Caminho do arquivo JSON onde os dados dos login serão salvos
caminho_login = "login.json"

# Função para carregar os dados dos login do arquivo JSON
def carregar_dados_login():
    try:
        with open(caminho_login, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            return dados["login"]
    except (FileNotFoundError, json.JSONDecodeError):
        console.print("[bold red]Arquivo de login não encontrado ou corrompido. Retornando lista vazia.[/bold red]")
        return []

# Função para salvar os dados dos login no arquivo JSON
def salvar_dados_login(dados):
    try:
        with open(caminho_login, 'w', encoding='utf-8') as arquivo:
            json.dump({"login": dados}, arquivo, indent=4, ensure_ascii=False)
        console.print("[bold green]Dados dos login salvos com sucesso![/bold green]")
    except IOError as e:
        console.print(f"[bold red]Erro ao salvar dados: {e}[/bold red]")

# Função para gerar um novo ID para o login
def gerar_novo_id(dados_login):
    if dados_login:
        return max(login["ID_login"] for login in dados_login) + 1
    else:
        return 1

# Função para cadastrar um novo login
def cadastrar_login():
    console.print("[bold cyan]Cadastro de Novo login[/bold cyan]")
    
    # Carregar os dados existentes
    dados_login = carregar_dados_login()
    
    # Gerar um novo ID para o login
    novo_id = gerar_novo_id(dados_login)
    
    # Solicitar os dados do login
    nome = input("Digite o seu nome: ")
    genero = input("Digite o seu gênero (Masculino/Feminino/Outro): ")
    data_nascimento = input("Digite a sua data de nascimento (DD/MM/AAAA): ")
    cpf = input("Digite o seu CPF: ")
    telefone = input("Digite o seu telefone: ")
    email = input("Digite o seu email: ")
    cep = input("Digite o seu CEP: ")
    senha = input("Digite a sua senha: ")
    
    # Verificar se o email ou CPF já estão cadastrados
    for login in dados_login:
        if login["email"] == email or login["cpf"] == cpf:
            console.print("[bold red]Email ou CPF já cadastrado. Tente novamente.[/bold red]")
            return
    
    # Criar o dicionário com os dados do login
    novo_login = {
        "ID_login": novo_id,
        "nome": nome,
        "genero": genero,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "telefone": telefone,
        "email": email,
        "cep": cep,
        "senha": senha  # Adicionando a senha ao cadastro
    }
    
    # Adicionar o novo login à lista de login
    dados_login.append(novo_login)
    
    # Salvar os dados atualizados no arquivo JSON
    salvar_dados_login(dados_login)
    
    console.print(f"[bold green]Login {nome} cadastrado com sucesso! ID: {novo_id}[/bold green]")

# Função para fazer login
def fazer_login():
    console.print("[bold cyan]Faça seu login[/bold cyan]")
    
    # Carregar os dados existentes
    dados_login = carregar_dados_login()
    
    # Solicitar email/CPF e senha
    identificador = input("Digite seu email ou CPF: ")
    senha = input("Digite sua senha: ")
    
    # Verificar se o login existe
    for login in dados_login:
        if (login["email"] == identificador or login["cpf"] == identificador) and login["senha"] == senha:
            console.print(f"[bold green]Login bem-sucedido! Bem-vindo, {login['nome']}.[/bold green]")
            return login  # Retorna os dados do usuário logado
    
    # Se não encontrar o login
    console.print("[bold red]Email/CPF ou senha incorretos. Tente novamente.[/bold red]")
    return None

# Menu principal
def menu():
    while True:
        console.print("\n[bold]MENU PRINCIPAL[/bold]")
        console.print("1. Cadastrar novo login")
        console.print("2. Fazer login")
        console.print("3. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_login()
        elif opcao == "2":
            usuario_logado = fazer_login()
            if usuario_logado:
                console.print(f"[bold]Você está logado como: {usuario_logado['nome']}[/bold]")
                # Aqui você pode adicionar funcionalidades para o usuário logado
        elif opcao == "3":
            console.print("[bold]Saindo...[/bold]")
            break
        else:
            console.print("[bold red]Opção inválida. Tente novamente.[/bold red]")

# Executar o menu
menu()