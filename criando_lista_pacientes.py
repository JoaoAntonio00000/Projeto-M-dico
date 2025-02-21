import datetime
from datetime import date, datetime
import json
import os
from validacao_de_dados import validar_cpf_paciente, validar_data, validar_email, validar_telefone, validar_cep

# Lista de convênios - preciso pesquisar mais convenios 
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
    '1' : 'Feminino',
    '2' : 'Masculino',
    '3' : 'Não Binário',
    '4' : 'Prefiro não dizer'
}
#pesquisar mais depoios 


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

if dados_paciente:
    if dados_paciente['pacientes']:
        id_paciente = max(usuario["ID_PACIENTE"] for usuario in dados_paciente['pacientes']) + 1
    else:
        id_paciente = 1


# Função para cadastrar um novo paciente

def cadastrar():
    global id_paciente

    nome = input('Nome completo do paciente: ').strip()

    for chave, genero in lista_genero.items():
        print(f"{chave} - {genero}")
    genero = int(input('Digite o gênero do paciente: '))

    data_nascimento = input('Digite a data de nascimento (DD/MM/AAAA): ').strip()
    data_formatada = validar_data(data_nascimento)
    if not data_formatada:
        print("⚠️ Data inválida! Tente novamente.")
        return  
    else:
        print(f"Data válida: {data_formatada}")


    if not data_formatada:
        print("⚠️ Data inválida! Tente novamente.")
        return

    # Validação de CPF
    while True:
            cpf = input('Digite o CPF do paciente: ').strip()
            if validar_cpf_paciente:
                break
            else:
                print("⚠️ CPF inválido! Tente novamente.")
                return

        
    telefone = input('Digite o telefone do paciente: ').strip()
    cep = input('Digite o CEP do paciente: ').strip()
    cep_validado = validar_cep(cep)
    while True:
        email = input('Digite o e-mail do paciente: ').strip()
        if validar_email(email):
            break
        
    for chave, genero in lista_convenio.items():
        print(f"{chave} - {genero}")

    convenio = input('Digite qual o convênio do paciente(caso nao possua digitar "nao"): ').strip().upper()

    
    dados = carregar_dados()
    # Verifica se o CPF já está cadastrado
    for paciente in dados['pacientes']:
        if paciente['cpf'] == cpf:
            print('⚠️ Paciente já cadastrado. Tente com outro CPF.')
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
        'cep': cep_validado,
        'convenio': convenio
    })

    salvar_dados(dados)
    print('✅ Paciente cadastrado com sucesso.')

# Função para procurar um paciente pelo CPF
def procurar_paciente():
    dados = carregar_dados()
    filtro = input('Digite o CPF do paciente (apenas números): ').strip()
    cpf_formatado = validar_cpf_paciente(filtro)

    if not cpf_formatado:
        print("⚠️ CPF inválido! Tente novamente.")
        return

    for paciente in dados['pacientes']:
        if paciente['cpf'] == cpf_formatado:
            print(f"\n📋 Paciente encontrado:\n"
                f"Nome: {paciente['nome']}\n"
                f"Gênero: {paciente['genero']}\n"
                f"Data de Nascimento: {paciente['data_nascimento']}\n"
                f"CPF: {paciente['cpf']}\n"
                f"Telefone: {paciente['telefone']}\n"
                f"Email: {paciente['email']}\n"
                f"CEP: {paciente['cep']}\n"
                f"Convênio: {paciente['convenio']}")
            
    print('⚠️ Paciente não encontrado.')


# Menu para rodar no terminal
while True:
    print('\nO que deseja realizar?')
    print('1 - Cadastrar um novo paciente')
    print('2 - Listar pacientes já cadastrados')
    print('3 - Procurar por um paciente')
    print('0 - Sair do sistema')

    opcao = input('Escolha uma opção: ').strip()

    if opcao == '1':
        cadastrar()
    elif opcao == '2':
        dados = carregar_dados()
        print("\n📋 Lista de Pacientes:")
        for paciente in dados["pacientes"]:
            print(f"- {paciente['nome']} ({paciente['cpf']})")
    elif opcao == '3':
        procurar_paciente()
    elif opcao == '0':
        print('Saindo...')
        break
    else:
        print('⚠️ Opção inválida. Tente novamente.')
