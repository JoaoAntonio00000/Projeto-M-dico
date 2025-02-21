import datetime
import json
import os

# Lista de convênios - pesquisar mais pra por aqui e ver quanto de desconto cada um da
lista_convenio = {
    'UNIMED': 0.5,
}

# Aqui eu crio o arquivo json 
pacientes_json = 'pacientes.json'

# Verifica se o arquivo JSON existe, caso nao, ele cria um

def verificar_se_arquivo_existe():
    try:
        with open(pacientes_json, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.readline()
            return conteudo
    except FileNotFoundError:
        with open(pacientes_json, 'w') as arquivo:
            json.dump({'pacientes': []}, arquivo, indent=4)
        return 'Arquivo Criado'

verificar_se_arquivo_existe()

# Função para carregar os dados do arquivo.json
def carregar_dados():
    with open(pacientes_json, 'r') as arquivo:
        return json.load(arquivo)
    


# Função para salvar os dados no arquivo.json
def salvar_dados(dados):
    with open(pacientes_json, 'w') as arquivo:  
        json.dump(dados, arquivo, indent=4)


# Função para cadastrar um novo paciente
def cadastrar():
    nome = input('Nome completo do paciente: ')
    print('Por favor, indique o gênero do paciente\nFeminino\nMasculino\nNão binário\nPrefiro não dizer')
    genero = input('Digite o gênero do paciente: ').strip()
    
    # trocar essa merda por uma função
    data_nascimento = input('Digite a data de nascimento (DD/MM/AAAA): ')
    try:
        data_formatada = datetime.datetime.strptime(data_nascimento, "%d/%m/%Y").strftime("%d/%m/%Y")
    except ValueError:
        print('⚠️ Data inválida! Tente novamente no formato DD/MM/AAAA.')
        return

    cpf = input('Digite o CPF do paciente: ').strip()
    telefone = input('Digite o telefone do paciente: ')
    cep = input('Digite o CEP do paciente: ')
    email = input('Digite o e-mail do paciente: ')
    convenio = input('Digite qual o convênio do paciente: ').strip()

    dados = carregar_dados()

    # Verifica se o CPF já está cadastrado
    for paciente in dados['pacientes']:
        if paciente['cpf'] == cpf:
            print('Paciente já cadastrado, tente com outro CPF.')
            return

    # Adicionando os pacientes ao arquivo.json
    dados['pacientes'].append({
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
    print('✅ Paciente cadastrado com sucesso.')

# Função para procurar um paciente pelo CPF
def procurar_paciente():
    dados = carregar_dados()
    filtro = input('Digite o CPF do paciente: ').strip()

    for paciente in dados['pacientes']:
        if paciente['cpf'] == filtro:
            print(f"\n📋 Paciente encontrado:\nNome: {paciente['nome']}\nGênero: {paciente['genero']}\nData de Nascimento: {paciente['data_nascimento']}\nCPF: {paciente['cpf']}\nTelefone: {paciente['telefone']}\nEmail: {paciente['email']}\nCEP: {paciente['cep']}\nConvênio: {paciente['convenio']}")
            return
    
    print('⚠️ Paciente não encontrado.')

# Menu para rodar no terminal e fazer os trem q tem q fazer
while True:
    print('\nO que deseja realizar?')
    print('1 - Cadastrar um novo paciente')
    print('2 - Listar pacientes já cadastrados')
    print('3 - Procurar por um paciente')
    print('0 - Sair do sistema')

    opcao = input('Escolha uma opção: ')

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
