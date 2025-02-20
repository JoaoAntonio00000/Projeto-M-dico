from datetime import datetime
from rich.console import Console
console = Console()
#Validadr o horario 
def validar_horario(horario):
    try:
        datetime.strptime(horario, "%H:%M")
        return True
    except ValueError:
        return False

#Validar o Email
def validar_email(email):
    import re
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

#Validar CRM
import re

def validar_crm(crm):
    padrao_crm = r"^\d{4,6}/[A-Z]{2}$"  # Exemplo: 123456/SP
    return bool(re.match(padrao_crm, crm))


#Validar CPF:
def validar_cpf(cpf):
    cpf = cpf.lower().replace("-", '').replace(".", '')
    if not cpf:
        console.print("[bold red]O CPF é obrigatório.")   
        return False   
    if len(cpf) != 11:
        console.print("[bold red]O número de CPF deve ter 11 dígitos.")
        return False
    if cpf == cpf[0] * 11:
        console.print("[bold red]CPF inválido por conter números repetidos.")
        return False
    
    soma_1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto_1 = soma_1 % 11
    digito_1 = 0 if resto_1 < 2 else 11 - resto_1
    
    soma_2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto_2 = soma_2 % 11
    digito_2 = 0 if resto_2 < 2 else 11 - resto_2
    
    if cpf[-2:] == f"{digito_1}{digito_2}":
        return True
    else:
        console.print("[bold red]CPF inválido.")
        return False