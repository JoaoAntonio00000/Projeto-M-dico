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

def carregar_dados_secretaria():
    caminho_secretaria = "lista_secretaria.json"
    try:
        with open(caminho_secretaria, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

dados_secretaria = carregar_dados_secretaria()  # Corrigido para carregar dados da secretaria

# Validar se o horário está correto
def validar_horario(horario):
    try:
        datetime.strptime(horario, "%H:%M")
        return True  # Retorna True se o horário estiver no formato correto
    except ValueError:
        console.print("[bold red]Horário inválido. Use o formato HH:MM.[/bold red]")
        return False

# Validar se o e-mail já existe e se é válido
def validar_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(regex, email):
        console.print("[bold red]E-mail inválido.[/bold red]")
        return False
    
    for usuario in dados_medico:
        if usuario["E-mail"].lower() == email.lower():
            console.print("[bold red]E-mail já cadastrado.[/bold red]")
            return False
    
    return True  # Retorna True se o e-mail for válido e não estiver cadastrado
    

# Validar se o CRM já existe e se é válido
def validar_crm(crm):
    padrao_crm = r"^\d{4,6}/[A-Z]{2}$"  # Exemplo: 123456/SP
    if not re.match(padrao_crm, crm):
        console.print("[bold red]CRM inválido.[/bold red]")
        return False
    
    for usuario in dados_medico:
        if usuario["CRM"].upper() == crm.upper():
            console.print("[bold red]CRM já cadastrado.[/bold red]")
            return False
    
    return True  # Retorna True se o CRM for válido e não estiver cadastrado

# Validar se o CPF já existe e se é válido (para médicos)
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

# Validar CPF para pacientes
def validar_cpf_paciente(cpf):
    cpf = cpf.replace("-", '').replace(".", '')
    if not cpf:
        console.print("[bold red]O CPF é obrigatório.[/bold red]")
        return False  # Retorna False se o CPF estiver vazio.
    
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        console.print("[bold red]CPF inválido.[/bold red]")
        return False  # Retorna False se o CPF tiver tamanho inválido ou for uma sequência de números repetidos.
    
    soma_1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto_1 = soma_1 % 11
    digito_1 = 0 if resto_1 < 2 else 11 - resto_1
    
    soma_2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto_2 = soma_2 % 11
    digito_2 = 0 if resto_2 < 2 else 11 - resto_2
    
    # Comparando os dois últimos dígitos com os valores calculados
    if cpf[-2:] != f"{digito_1}{digito_2}":
        console.print("[bold red]CPF inválido.[/bold red]")
        return False  # Retorna False se os dígitos verificadores não coincidirem.
    
    return True  # Retorna True se o CPF for válido

# Validar CPF para secretárias
def validar_cpf_secretaria(cpf):
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
    
    # Verifica se o CPF já está cadastrado na lista de secretárias
    for usuario in dados_secretaria:
        if usuario["CPF"] == cpf:
            console.print("[bold red]CPF já cadastrado.")
            return False
    
    return True

# Validar data de nascimento
def validar_data(data_nascimento):
    # Expressão regular para garantir que a data siga o formato DD/MM/AAAA
    padrao = r'^\d{2}/\d{2}/\d{4}$'

    # Verifica se a data segue o formato esperado
    if re.match(padrao, data_nascimento):
        try:
            # Tenta converter para o formato datetime para verificar se a data é válida
            datetime.strptime(data_nascimento, "%d/%m/%Y")
            return True  # Retorna True se a data for válida
        except ValueError:
            # Se der erro ao tentar converter, a data não é válida
            console.print("[bold red]Data inválida.[/bold red]")
            return False
    else:
        # Se a data não segue o formato esperado, retorna False
        console.print("[bold red]Formato de data inválido. Use DD/MM/AAAA.[/bold red]")
        return False

# Validar telefone
def validar_telefone(telefone):
    # Expressão regular para validar o formato (00)00000-0000
    padrao = r'^\(\d{2}\)\d{5}-\d{4}$'
    
    if re.match(padrao, telefone):
        return telefone  
    else:
        console.print("⚠️ Telefone inválido! O formato correto é (00)00000-0000 (coloque o DDD).")
        return False

# Validar CEP
def validar_cep(cep):
    padrao_cep = r'^\d{5}-\d{3}$'
    if re.match(padrao_cep, cep):
        return True  # Retorna True se o CEP estiver no formato correto
    else:
        console.print("[bold red]CEP inválido. O formato correto é 00000-000.[/bold red]")
        return False

# Validar força da senha
def validar_forca_senha(senha):
    if len(senha) < 8:
        console.print("A senha deve ter pelo menos 8 caracteres.", style='error')
        return False
    if not re.search(r'\d', senha):
        console.print("A senha deve conter pelo menos um número.", style='error')
        return False
    if not re.search(r'[a-z]', senha):
        console.print("A senha deve conter pelo menos uma letra minúscula.", style='error')
        return False
    if not re.search(r'[A-Z]', senha):
        console.print("A senha deve conter pelo menos uma letra maiúscula.", style='error')
        return False
    if not re.search(r'[^a-zA-Z0-9\s]', senha):
        console.print("A senha deve conter pelo menos um caractere especial.", style='error')
        return False
    console.print("Senha adicionada com sucesso!", style='certo')
    return True  # Retorna True se a senha atender a todos os critérios