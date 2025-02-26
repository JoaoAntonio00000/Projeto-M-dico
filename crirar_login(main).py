import json
import os
import random
import string
from rich.console import Console
from validacao_de_dados import validar_crm, validar_forca_senha, validar_cpf, validar_email, validar_telefone, validar_cep, validar_data

# Importando os menus correspondentes
from menu_gestor import menu as menu_gestor
from menu_secretaria import menu as menu_secretaria
from menu_medico import menu_medico

console = Console()

# Caminhos dos arquivos JSON para cada tipo de usuário
caminho_login_gestor = "gestor.json"
caminho_login_medico = "medico.json"
caminho_login_secretaria = "secretaria.json"

# Função para carregar os dados dos login do arquivo JSON
def carregar_dados_login(caminho):
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(caminho):
            # Se o arquivo não existir, cria um novo com uma lista vazia
            with open(caminho, 'w', encoding='utf-8') as arquivo:
                json.dump({"login": []}, arquivo, indent=4, ensure_ascii=False)
            console.print(f"[bold yellow]Arquivo {caminho} criado com sucesso.[/bold yellow]")
            return []  # Retorna uma lista vazia para o primeiro uso
        
        # Se o arquivo existir, carrega os dados
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            return dados["login"]
    except json.JSONDecodeError:
        console.print(f"[bold red]Arquivo {caminho} está corrompido. Retornando lista vazia.[/bold red]")
        return []

# Função para salvar os dados dos login no arquivo JSON
def salvar_dados_login(caminho, dados):
    try:
        with open(caminho, 'w', encoding='utf-8') as arquivo:
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

# Função para gerar um código aleatório para o Gestor
def gerar_codigo_gestor():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Função para cadastrar um novo login
def cadastrar_login():
    console.print("[bold cyan]Cadastro de Novo login[/bold cyan]")
    
    # Solicitar o tipo de usuário
    tipo = console.input("Digite o tipo de usuário (Gestor/Médico/Secretária): ").strip().lower()
    
    if tipo not in ["gestor", "médico", "secretária"]:
        console.print("[bold red]Tipo de usuário inválido. Tente novamente.[/bold red]")
        return
    
    # Carregar os dados existentes
    if tipo == "gestor":
        dados_login = carregar_dados_login(caminho_login_gestor)
    elif tipo == "médico":
        dados_login = carregar_dados_login(caminho_login_medico)
    else:
        dados_login = carregar_dados_login(caminho_login_secretaria)
    
    # Gerar um novo ID para o login
    novo_id = gerar_novo_id(dados_login)
    
    # Solicitar os dados do login
    nome = console.input("[bold yellow]Digite o seu nome: ")
    genero = console.input("[bold yellow]Digite o seu gênero (Masculino/Feminino/Outro): ")
    data_nascimento = console.input("[bold yellow]Digite a sua data de nascimento (DD/MM/AAAA): ")
    while True:
        if validar_data(data_nascimento):
            console.print("[bold red]Data de nascimento inválida. Tente novamente.[/bold red]")
            break
    while True:
        cpf = console.input("[bold yellow]Digite o seu CPF: ")
        if validar_cpf(cpf):
            console.print("[bold red]CPF inválido ou já cadastrado. Tente novamente.[/bold red]")
            break
    while True:    
        telefone = console.input("[bold yellow]Digite o seu telefone: ")
        if validar_telefone(telefone):
            console.print("[bold red]Telefone inválido. Tente novamente.[/bold red]")
            break
    while True:    
        email = console.input("[bold yellow]Digite o seu email: ")
        if validar_email(email):
            console.print("[bold red]E-mail inválido ou já cadastrado. Tente novamente.[/bold red]")
            break
    while True: 
        cep = console.input("[bold yellow]Digite o seu CEP: ")
        if validar_cep(cep):
            console.print("[bold red]CEP inválido. Tente novamente.[/bold red]")
            break
    while True:
        senha = console.input("[bold yellow]Digite a sua senha: ")
        if validar_forca_senha(senha):
            console.print("[bold red]Senha não atende aos requisitos de segurança. Tente novamente.[/bold red]")
            break
        
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
        "senha": senha,
        "tipo": tipo
    }
    
    # Adicionar campos específicos para Gestor e Médico
    if tipo == "gestor":
        novo_login["codigo_gestor"] = gerar_codigo_gestor()
    elif tipo == "médico":
        while True:
            crm = console.input("[bold yellow]Digite o seu CRM: ")
            if validar_crm(crm):
                console.print("[bold red]CRM inválido ou já cadastrado. Tente novamente.[/bold red]")
                break
            novo_login["crm"] = crm
    
    # Adicionar o novo login à lista de login
    dados_login.append(novo_login)
    
    # Salvar os dados atualizados no arquivo JSON correspondente
    if tipo == "gestor":
        salvar_dados_login(caminho_login_gestor, dados_login)
    elif tipo == "médico":
        salvar_dados_login(caminho_login_medico, dados_login)
    else:
        salvar_dados_login(caminho_login_secretaria, dados_login)
    
    console.print(f"[bold green]Login {nome} cadastrado com sucesso! ID: {novo_id}[/bold green]")

# Função para fazer login
def fazer_login():
    console.print("[bold cyan]Faça seu login[/bold cyan]")
    
    # Solicitar o tipo de usuário
    tipo = console.input("[bold yellow]Digite o tipo de usuário (Gestor/Médico/Secretária): ").strip().lower()
    
    if tipo not in ["gestor", "médico", "secretária"]:
        console.print("[bold red]Tipo de usuário inválido. Tente novamente.[/bold red]")
        return None
    
    # Carregar os dados existentes
    if tipo == "gestor":
        dados_login = carregar_dados_login(caminho_login_gestor)
        identificador = console.input("[bold yellow]Digite seu código de gestor: ")
    elif tipo == "médico":
        dados_login = carregar_dados_login(caminho_login_medico)
        identificador = console.input("[bold yellow]Digite seu CRM: ")
    else:
        dados_login = carregar_dados_login(caminho_login_secretaria)
        identificador = console.input("[bold yellow]Digite seu email ou CPF: ")
    
    senha = console.input("[bold yellow]Digite sua senha: ")
    
    # Verificar se o login existe
    for login in dados_login:
        if tipo == "gestor":
            if login["codigo_gestor"] == identificador and login["senha"] == senha:
                console.print(f"[bold green]Login bem-sucedido! Bem-vindo, {login['nome']}.[/bold green]")
                return login
        elif tipo == "médico":
            if login["crm"] == identificador and login["senha"] == senha:
                console.print(f"[bold green]Login bem-sucedido! Bem-vindo, {login['nome']}.[/bold green]")
                return login
        else:
            if (login["email"] == identificador or login["cpf"] == identificador) and login["senha"] == senha:
                console.print(f"[bold green]Login bem-sucedido! Bem-vindo, {login['nome']}.[/bold green]")
                return login
    
    # Se não encontrar o login
    console.print("[bold red]Identificador ou senha incorretos. Tente novamente.[/bold red]")
    return None

# Função principal que inicia o login e redireciona para o menu correto
def main():
    while True:
        console.print("\n[bold blue]SISTEMA DE LOGIN[/bold blue]")
        console.print("[bold yellow]1. Fazer login")
        console.print("[bold yellow]2. Cadastrar novo login")
        console.print("[bold red]3. Sair")
        opcao = console.input("Escolha uma opção: ")
        
        if opcao == "1":
            usuario_logado = fazer_login()
            if usuario_logado:
                console.print(f"[bold]Você está logado como: {usuario_logado['nome']}[/bold]")
                
                # Redirecionar para o menu correto com base no tipo de usuário
                if usuario_logado["tipo"] == "gestor":
                    menu_gestor()
                elif usuario_logado["tipo"] == "secretária":
                    menu_secretaria()
                elif usuario_logado["tipo"] == "médico":
                    menu_medico(usuario_logado["ID_login"])  # Passando o ID do médico
        elif opcao == "2":
            cadastrar_login()
        elif opcao == "3":
            console.print("[bold blue]Saindo...[/bold blue]")
            break
        else:
            console.print("[bold red]Opção inválida. Tente novamente.[/bold red]")

# Iniciar o programa
if __name__ == "__main__":
    main()