import datetime
import string
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
    dados = carregar_dados()
    if dados_paciente and dados_paciente['pacientes']:
        id_paciente = max(usuario["ID_PACIENTE"] for usuario in dados_paciente['pacientes']) + 1
    else:
        id_paciente = 1

    nome = input('Nome completo do paciente: ').strip()

    console.print("\nSelecione o gênero:", style="bold cyan")
    for chave, genero in lista_genero.items():
        console.print(f"[cyan]{chave}[/] - {genero}")
    genero = int(input('Digite o número correspondente ao gênero: '))
    genero = lista_genero.get(genero, "Não informado")  # Converte o número para o gênero correspondente



    data_nascimento = input('Digite a data de nascimento (DD/MM/AAAA): ').strip()
    data_formatada = validar_data(data_nascimento)
    if not data_formatada:
        console.print("[red]⚠️ Data inválida! Tente novamente.[/]")
        return  

    while True:
        cpf = input('Digite o CPF do paciente: ').strip()
        if validar_cpf_paciente(cpf):
            break
    while True:
        telefone = input('Digite o telefone do paciente: ').strip()
        if validar_telefone(telefone):
            break
    while True:
        cep = input('Digite o CEP do paciente: ').strip()
        if validar_cep(cep):
            break
    
    while True:
        email = input('Digite o e-mail do paciente: ').strip()
        if validar_email(email):
            break

    console.print("\nSelecione o convênio:", style="bold cyan")
    for chave in lista_convenio.keys():
        console.print(f"[cyan]{chave}[/]")

    convenio = input('Digite o nome do convênio do paciente (caso não possua, digite "nao"): ').strip().upper()
    convenio = lista_convenio.get(convenio, "Não informado") 

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
    filtro = int(input('Digite o ID do paciente (apenas números): '))

    for paciente in dados['pacientes']:
        if paciente['ID_PACIENTE'] == filtro:
            table = Table(title="📋 Paciente Encontrado", show_header=True, header_style="bold magenta")
            table.add_column("Campo", justify="left", style="cyan", no_wrap=True)
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


def listar_pacientes():
    dados = carregar_dados()
    if not dados["pacientes"]:
        console.print("[yellow]Nenhum paciente cadastrado.[/]")
        return
    
    table = Table(title="Lista de Pacientes")
    table.add_column("ID_PACIENTE", style="cyan")
    table.add_column("Nome", style="magenta")
    table.add_column("Telefone", style="green")
    
    for paciente in dados["pacientes"]:
    # Verificar o tipo dos dados
        print(f"ID_PACIENTE: {type(paciente['ID_PACIENTE'])}, Nome: {type(paciente['nome'])}")

    # Convertendo para string explicitamente
        table.add_row(str(paciente['ID_PACIENTE']), str(paciente['nome']))
    
    console.print(table)

def delet_pacientes():
    dados = carregar_dados()
    id_paciente = int(input('Digite o ID do paciente que deseja remover: '))

    for paciente in dados["pacientes"]:
        if paciente["ID_PACIENTE"] == id_paciente:
            dados["pacientes"].remove(paciente)
            salvar_dados(dados)
            console.print("[green]✅ Paciente removido com sucesso![/]")
            return
    
    console.print("[red]⚠️ Paciente não encontrado![/]")

def modificar_dados():
    dados = carregar_dados()
    id_paciente = int(input('Digite o CPF do paciente que deseja modificar: '))
    
    for paciente in dados["pacientes"]:
        if paciente["ID_PACIENTE"] == id_paciente:
            console.print("1 - Nome\n2 - Telefone\n3 - E-mail\n4 - CEP\n5 - Data de nascimento\n0 - Voltar")
            
            try:
                opcao = int(input("Selecione uma opção: "))
            except ValueError:
                console.print("[red]⚠️ Entrada inválida.[/]")
                return
            
            if opcao == 1:
                paciente["nome"] = input("Novo nome: ").strip()
            elif opcao == 2:
                while True:
                    telefone = input("Novo telefone: ").strip()
                    if validar_telefone(telefone):
                        paciente["telefone"] = telefone
                        break
                    console.print("[red]⚠️ Telefone inválido![/]")
            elif opcao == 3:
                email = input("Novo e-mail: ").strip()
                if validar_email(email):
                    paciente["email"] = email
                else:
                    console.print("[red]⚠️ E-mail inválido![/]")
                    return
            elif opcao == 4:
                while True:
                    cep = input("Novo CEP: ").strip()
                    if validar_cep(cep):
                        paciente["cep"] = cep
                        break
                    console.print("[red]⚠️ CEP inválido![/]")
            elif opcao == 5:
                while True:
                    data_nascimento = input("Nova data de nascimento (DD/MM/AAAA): ").strip()
                    if validar_data(data_nascimento):
                        paciente["data_nascimento"] = data_nascimento
                        break
                    console.print("[red]⚠️ Data inválida![/]")
            elif opcao == 0:
                return
            else:
                console.print("[red]⚠️ Opção inválida![/]")
                return
            
            salvar_dados(dados)
            console.print("[green]✅ Dados atualizados com sucesso![/]")
            return
    
    console.print("[red]⚠️ Paciente não encontrado![/]")




# Menu para rodar no terminal
while True:
    console.print("\n[bold yellow]📌 Menu Principal[/]")
    console.print("[bold cyan]1[/] - Cadastrar um novo paciente")
    console.print("[bold cyan]2[/] - Listar pacientes já cadastrados")
    console.print("[bold cyan]3[/] - Procurar por um paciente")
    console.print("[bold cyan]4[/] - Deletar um paciente do sistema")
    console.print("[bold cyan]5[/] - Modificar dados de um paciente")
    console.print("[bold cyan]0[/] - Sair do sistema")

    opcao = int(input('Escolha uma opção: '))
    if opcao == 1:
        cadastrar()
    elif opcao == 2:
        dados = carregar_dados()
        table = Table(title="\n📋 Lista de Pacientes", show_header=True, header_style="bold magenta")
        table.add_column("ID_PACIENTE", style="green", justify="center")
        table.add_column("Nome", style="cyan", justify="left")
        
        for paciente in dados["pacientes"]:
            table.add_row(f"{paciente['ID_PACIENTE']}" , f"{paciente['nome']}")
            
        console.print(table)

    elif opcao == 3:
        procurar_paciente()

    elif opcao == 4:
        delet_pacientes()  

    elif opcao == 5:
        modificar_dados()

    elif opcao == 0:
        console.print("[green]Saindo...[/]")
        break
    else:
        console.print("[red]⚠️ Opção inválida. Tente novamente.[/]")


