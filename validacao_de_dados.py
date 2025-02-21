import json
import re
from datetime import datetime
from rich.console import Console

console = Console()
caminho_arquivo = "lista_medicos.json"

def carregar_dados():
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

dados_medico = carregar_dados()

# Validar se o horário está correto
def validar_horario(horario):
    try:
        datetime.strptime(horario, "%H:%M")
        return True
    except ValueError:
        return False

# Validar se o e-mail já existe e se é válido
def validar_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(regex, email):
        console.print("[bold red]E-mail inválido.")
        return False
    
    for usuario in dados_medico:
        if usuario["E-mail"].lower() == email.lower():
            console.print("[bold red]E-mail já cadastrado.")
            return False
    
    return True

# Validar se o CRM já existe e se é válido
def validar_crm(crm):
    padrao_crm = r"^\d{4,6}/[A-Z]{2}$"  # Exemplo: 123456/SP
    if not re.match(padrao_crm, crm):
        console.print("[bold red]CRM inválido.")
        return False
    
    for usuario in dados_medico:
        if usuario["CRM"].upper() == crm.upper():
            console.print("[bold red]CRM já cadastrado.")
            return False
    
    return True

# Validar se o CPF já existe e se é válido
def validar_cpf(cpf):
    cpf = cpf.replace("-", '').replace(".", '')
    if not cpf:
        console.print("[bold red]O CPF é obrigatório.")
        return False   
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        console.print("[bold red]CPF inválido.")
        return False
    
    soma_1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto_1 = soma_1 % 11
    digito_1 = 0 if resto_1 < 2 else 11 - resto_1
    
    soma_2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto_2 = soma_2 % 11
    digito_2 = 0 if resto_2 < 2 else 11 - resto_2
    
    if cpf[-2:] != f"{digito_1}{digito_2}":
        console.print("[bold red]CPF inválido.")
        return False
    
    for usuario in dados_medico:
        if usuario["CPF"] == cpf:
            console.print("[bold red]CPF já cadastrado.")
            return False
    
    return True

def validar_cpf_paciente(cpf):
    cpf = cpf.replace("-", '').replace(".", '')
    if not cpf:
        console.print("[bold red]O CPF é obrigatório.")
        return False   
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        console.print("[bold red]CPF inválido.")
        return False
    
    soma_1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto_1 = soma_1 % 11
    digito_1 = 0 if resto_1 < 2 else 11 - resto_1
    
    soma_2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto_2 = soma_2 % 11
    digito_2 = 0 if resto_2 < 2 else 11 - resto_2
    
    if cpf[-2:] != f"{digito_1}{digito_2}":
        console.print("[bold red]CPF inválido.")
        return False
    



def validar_data(data_nascimento):
    # Expressão regular para garantir que a data siga o formato DD/MM/AAAA
    padrao = r'^\d{2}/\d{2}/\d{4}$'

    # Verifica se a data segue o formato esperado
    if re.match(padrao, data_nascimento):
        try:
            # Tenta converter para o formato datetime para verificar se a data é válida
            data_formatada = datetime.strptime(data_nascimento, "%d/%m/%Y")
            return data_formatada.strftime("%d/%m/%Y")  # Retorna a data formatada corretamente
        except ValueError:
            # Se der erro ao tentar converter, a data não é válida
            return False
    else:
        # Se a data não segue o formato esperado, retorna False
        return False




def validar_telefone(telefone):
    # Expressão regular para validar o formato (00)00000-0000
    padrao = r'^\(\d{2}\)\d{5}-\d{4}$'
    
    if re.match(padrao, telefone):
        return telefone  
    else:
        print("⚠️ Telefone inválido! O formato correto é (00)00000-0000 (coloque o DDD).")
        return False

def validar_cep(cep):

    padrao_cep = r'^\d{5}-\d{3}$'
    
    if re.match(padrao_cep, cep):
        return True
    else:
        return False