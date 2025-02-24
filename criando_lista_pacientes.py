import datetime
from datetime import date, datetime
import json
import os
from rich.console import Console
from rich.table import Table
from rich.text import Text
from validacao_de_dados import validar_cpf_paciente, validar_data, validar_email, validar_telefone, validar_cep

console = Console()

# Lista de convênios
lista_convenio = {
    'UNIMED': 0.5,
    'BRADESCO-SAUDE' : 0.3,
    'SULAMERICA' : 0.35,
    'NOTREDAME-INTERMEDICA' : 0.25,
    'GOLDEN-CROSS' : 0.3,
    'PAX-NACIONAL' : 0.5,
    'HAPVIDA' : 0.2,
    'nao' : 0
}

lista_genero = {
    1 : 'Feminino',
    2 : 'Masculino',
    3 : 'Não Binário',
    4 : 'Prefiro não dizer'
}

pacientes_json = 'pacientes.json'

# Função para verificar e criar o arquivo json caso ele não exista
def verificar_se_arquivo_existe():
    try:
        with open(pacientes_json, "r", encoding="utf-8") as arquivo:
            conteudo = json.load(arquivo)
            return conteudo
    except (FileNotFoundError, json.JSONDecodeError):
        with open(pacientes_json, 'w', encoding="utf-8") as arquivo:
            json.dump({'pacientes': []}, arquivo, indent=4)
        return {'pacientes': []}
verificar_se_arquivo_existe()

# Carregar os dados
def carregar_dados():
    with open(pacientes_json, 'r', encoding="utf-8") as arquivo:
        return json.load(arquivo)

# Salvar os dados
def salvar_dados(dados):
    with open(pacientes_json, 'w', encoding="utf-8") as arquivo:  
        json.dump(dados, arquivo, indent=4)

dados_paciente = carregar_dados()

if dados_paciente and dados_paciente['pacientes']:
    id_paciente = max(usuario["ID_PACIENTE"] for usuario in dados_paciente['pacientes']) + 1
else:
    id_paciente = 1

# Função para cadastrar um novo paciente
def cadastrar():
    global id_paciente

    nome = input('Nome completo do paciente: ').strip()

    console.print("\nSelecione o gênero:", style="bold cyan")
    for chave, genero in lista_genero.items():
        console.print(f"[cyan]{chave}[/] - {genero}")
    genero = int(input('Digite o número correspondente ao gênero: '))


    data_nascimento = input('Digite a data de nascimento (DD/MM/AAAA): ').strip()
    data_formatada = validar_data(data_nascimento)
    if not data_formatada:
        console.print("[red]⚠️ Data inválida! Tente novamente.[/]")
        return  

    while True:
        cpf = input('Digite o CPF do paciente: ').strip()
        if validar_cpf_paciente:
            break
        else:
            console.print("[red]⚠️ CPF inválido! Tente novamente.[/]")
            return
    while True:
        telefone = input('Digite o telefone do paciente: ').strip()
        if validar_telefone:
            break
        else:
            console.print("[red]⚠️ Telefone inválido! Tente novamente.[/]")
            return
    while True:
        cep = input('Digite o CEP do paciente: ').strip()
        if validar_cep:
            break
        else:
            console.print("[red]⚠️ CEP inválido! Tente novamente.[/]")
            return
    
    while True:
        email = input('Digite o e-mail do paciente: ').strip()
        if validar_email(email):
            break

    console.print("\nSelecione o convênio:", style="bold cyan")
    for chave in lista_convenio.keys():
        console.print(f"[cyan]{chave}[/]")

    convenio = input('Digite o nome do convênio do paciente (caso não possua, digite "nao"): ').strip().upper()

    dados = carregar_dados()

    # Verifica se o CPF já está cadastrado
    for paciente in dados['pacientes']:
        if paciente['cpf'] == cpf:
            console.print("[red]⚠️ Paciente já cadastrado. Tente com outro CPF.[/]")
            return

    # Adicionando os pacientes ao arquivo json
    dados['pacientes'].append({
        'ID_PACIENTE' : id_paciente,
        'nome': nome,
        'genero': genero,
        'data_nascimento': data_formatada,
        'cpf': cpf,
        'telefone': telefone,
        'email': email,
        'cep': cep,
        'convenio': convenio
    })

    salvar_dados(dados)
    console.print("[green]✅ Paciente cadastrado com sucesso.[/]")

# Função para procurar um paciente pelo CPF
def procurar_paciente():
    dados = carregar_dados()
    filtro = input('Digite o ID do paciente (apenas números): ').strip()

    for paciente in dados['pacientes']:
        if paciente['ID_PACIENTE'] == filtro:
            table = Table(title="📋 Paciente Encontrado", show_header=True, header_style="bold magenta")
            table.add_column("Campo", justify="right", style="cyan", no_wrap=True)
            table.add_column("Valor", style="bold green")
            table.add_row("Nome", paciente['nome'])
            table.add_row("Gênero", paciente['genero'])
            table.add_row("Data de Nascimento", paciente['data_nascimento'])
            table.add_row("CPF", paciente['cpf'])
            table.add_row("Telefone", paciente['telefone'])
            table.add_row("Email", paciente['email'])
            table.add_row("CEP", paciente['cep'])
            table.add_row("Convênio", paciente['convenio'])
            
            console.print(table)
            return

    console.print("[red]⚠️ Paciente não encontrado.[/]")


def listar_pacientes(pacientes):
    #adicionar print do ID e nome completo dos pacientes ja cadastrados
    if not pacientes:
        print('Sem pacientes registrados no sistema.')
    else:
        for paciente in pacientes:
            print(f'ID: {dados['ID_PACIENTE']}\nNome: {dados['nome']}\nTelefone: {dados['telefone']}')

def delet_pacientes():
    #funcao para deletar pacientes do arquivo json
    paciente = procurar_paciente()
    if paciente:
        dados.remove(paciente)
        salvar_dados(paciente)
        print('Paciente removido do sistema.')


def modificar_dados():
    paciente = procurar_paciente()
    if paciente:
        print('O que gostaria de alterar:\n1 - Nome\n2 - Genero\n3 - Data de nascimento\n4 - CPF\n5 - Telefone\n6 - E-mail\n7 - CEP\n8 - Convenio do paciente')
        while True:
            try:
                decisao = int(input('- '))
                break
            except ValueError:
                print('Valor inválido, tente novamente.')
                return
        if decisao == 1:
            dados['nome'] = input('Digite o novo nome: ')


        elif decisao == 2:
            while True:
                try:
                    for chave, genero in lista_genero.items():
                        console.print(f"[cyan]{chave}[/] - {genero}")

                    dados['genero'] = int(input('Digite o novo genero a ser adicionado'))
                    break
                except ValueError:
                    print('Valor inválido, tente novamente.')
                    return
                
        elif decisao == 3:
            while True:
                try:
                    dados['data_nascimento'] = input('Digite a nova data de nascimento:').strip()
                    if validar_data:
                        break
                except:
                    print('Inválido, tente novamente.')
                    return
        
        elif decisao == 4:
            while True:
                try:
                    dados['cpf'] = input('Digite o novo CPF: ')
                    if validar_cpf_paciente:
                        break
                except ValueError:
                    print('CPF inválido, tente novamente.')
                    return
        elif decisao == 5:
            while True:
                try:
                    dados['telefone'] = input('Digite o novo telefone a ser adicionado: ')
                    if validar_telefone:
                        break
                except ValueError:
                    print('Telefone inválido, tente novamente.')
        elif decisao == 6:
            while True:
                try:
                    dados['email'] = input('Digite o novo E-mail do paciente: ')
                    if validar_email:
                        break
                except:
                    print('E-mail inválido, tente novamente')
                    return
        elif decisao == 7:
            while True:
                




# Menu para rodar no terminal
while True:
    console.print("\n[bold yellow]📌 Menu Principal[/]")
    console.print("[bold cyan]1[/] - Cadastrar um novo paciente")
    console.print("[bold cyan]2[/] - Listar pacientes já cadastrados")
    console.print("[bold cyan]3[/] - Procurar por um paciente")
    console.print("[bold cyan]0[/] - Sair do sistema")

    opcao = input('Escolha uma opção: ').strip()

    if opcao == '1':
        cadastrar()
    elif opcao == '2':
        dados = carregar_dados()
        table = Table(title="📋 Lista de Pacientes", show_header=True, header_style="bold magenta")
        table.add_column("Nome", style="cyan", justify="left")
        table.add_column("CPF", style="green", justify="left")

        for paciente in dados["pacientes"]:
            table.add_row(paciente['nome'], paciente['cpf'])

        console.print(table)
    elif opcao == '3':
        procurar_paciente()
    elif opcao == '0':
        console.print("[green]Saindo...[/]")
        break
    else:
        console.print("[red]⚠️ Opção inválida. Tente novamente.[/]")

