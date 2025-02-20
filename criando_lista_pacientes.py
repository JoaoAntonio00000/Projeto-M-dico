import datetime
import json
import os

'''
criar a lista de pacientes a serem cadastrados
'''

lista_convenio = {
    'UNIMED' : 0.5,

}


pacientes_json = 'pacientes.json'

if not os.path.exists(pacientes_json):
    with open (pacientes_json, 'w') as arquivo:
        json.dump({'pacientes' : []}, arquivo, indent= 4)

def carregar_dados():
    with open(pacientes_json, 'r') as arquivo:
        return json.load(arquivo)
    
def salvar_dados(dados):
    with open(pacientes_json, 'r') as arquivo:
        json.dump(dados, arquivo, indent= 4)

def cadastrar():
    nome = input('Nome completo do paciente: ')
    print('Por favor, indique o genêro do paciente\nFeminino\nMasculino\nNão binário\nPrefiro não dizer')
    genero = input('Digite o genêro do paciente: ')
    data_nascimento = input('Digite a data de nascimento do paciente(no modelo DD/MM/AAAA): ')
    try:
        data_formatada = datetime.strptime(data_nascimento)
        print(data_formatada)
    except ValueError:
        print('Formato de data inválida, tente novamente')

    cpf = float(input('Digite o cpf do paciente: '))
    telefone = input('Digite o telefone co paciente: ')
    cep = input('Digite o CEP do paciente: ')
    email = input('Digite o e-mail do paciente: ')
    convenio = input('Digite qual o convênio do paciente: ')

    if convenio in lista_convenio:
        #código de conta do convenio - verificar preços com o pessoal
        print() # só pro código n ficar dando erro
    
    dados = carregar_dados()

    for paciente in dados['pacientes']:
        if paciente['cpf'] == cpf:
            print('Paciente já cadastrado, tente com outro cpf')
            return
        

    dados['pacientes'].append({
        'nome' : nome,
        'cpf' : cpf,
        'telefone' : telefone,
        'email' : email,
        'cep' : cep,
        'convenio' : convenio
    })