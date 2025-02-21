import random
import string
import json
from datetime import datetime, timedelta

def gerar_codigo():
    # Define os caracteres possíveis: letras maiúsculas e números
    caracteres = string.ascii_uppercase + string.digits  # Letras maiúsculas + números
    
    # Gera 9 caracteres aleatórios
    codigo = ''.join(random.choices(caracteres, k=9))
    
    # Formata o código no padrão XXX-XXX-XXX
    codigo_formatado = '-'.join([codigo[i:i+3] for i in range(0, 9, 3)])
    
    return codigo_formatado

def salvar_codigo_json(codigo, arquivo='Prova5/codigos.json'):
    # Obtém a data e hora atual
    data_criacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Define o status inicial como True (código válido)
    status = True
    
    # Cria um dicionário com o código, a data de criação e o status
    novo_codigo = {
        "codigo": codigo,
        "data_criacao": data_criacao,
        "Status": status
    }
    
    try:
        # Tenta carregar os códigos existentes do arquivo JSON
        with open(arquivo, 'r') as f:
            codigos = json.load(f)
    except FileNotFoundError:
        # Se o arquivo não existir, cria uma lista vazia
        codigos = []
    
    # Verifica se o código já existe
    for item in codigos:
        if item["codigo"] == codigo:
            raise ValueError("Código já existe.")
    
    # Adiciona o novo código (com data e status) à lista
    codigos.append(novo_codigo)
    
    # Salva a lista atualizada no arquivo JSON
    with open(arquivo, 'w') as f:
        json.dump(codigos, f, indent=4)

def verificar_validade(codigo, arquivo='Prova5/codigos.json'):
    # Carrega os códigos do arquivo JSON
    with open(arquivo, 'r') as f:
        codigos = json.load(f)
    
    # Procura o código na lista
    for item in codigos:
        if item["codigo"] == codigo:
            data_criacao = datetime.strptime(item["data_criacao"], '%Y-%m-%d %H:%M:%S')
            # Define a validade como 30 dias a partir da data de criação
            validade = data_criacao + timedelta(days=30)
            # Verifica se o cupom ainda é válido
            if datetime.now() <= validade and item["Status"]:
                return True  # Código válido
            else:
                # Atualiza o status para False se o código expirou
                item["Status"] = False
                # Salva a lista atualizada no arquivo JSON
                with open(arquivo, 'w') as f:
                    json.dump(codigos, f, indent=4)
                return False  # Código expirado ou já utilizado
    
    return False  # Código não encontrado