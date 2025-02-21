'''
Exemplo dicionario agenda:
Agenda{
    dia, 
    hora,
    confirmacao_paciente,
    medico,
    tipo_consulta,
    ID_paciente,
    nome_paciente,
}


Agenda {
    segunda[
        {dia, 
        hora,
        confirmacao_paciente, pendente confirmado cancelado, se cancelado deixar so o log
        medico,
        tipo_consulta,
        ID_paciente,
        }
    ]
}

pegar os dias se ja tiver passado tipo de segunda já puxa segunda da semana que vem , e de somente de semana que vem 
 

Essa agenda fica no json
so faz a questao de adicionar e modificar ela no terminal , e pensar ja como integrar pelo telegram

cada vez que acessar a agenda ja faz uma limpa nela e adicona no log os que ja foram

with open ('agenda.json','r') as arquivo:
    agenda = json.load(arquivo)
    # Ordenar a lista de dicionários dentro da chave "segunda"
    agenda["segunda"] = sorted(agenda["segunda"], key=lambda x: (x["dia"], x["hora"]))

    # Exibir a agenda ordenada
    for entrada in agenda["segunda"]:
        print(entrada)
'''
import json
from datetime import date as dt
from datetime import timedelta
#verifica quais dias o medico esta livre
def verifica_disponibilidade_medico(arquivo):
    print('Ainda nada')

#mudar a lista de horarios da medico para false de acordo com a agenda, fechada de segunda a sexta
def agenda_para_lista_medico():
    print('Ainda nada')
#agendamento feito pelo terminal
def agendamento():
    proximo_mes = True #Enquanto não ficar false vai passando para o proximo mes, no agendamento do dia
    try:
        #parte 1 - Paciente já cadastrado, se nao estiver por favor vá para o cadastramento pelo terminal
        id_paciente = int(input("Digite o id do paciente: "))
        #parte 2 - escolher medico
        with open('lista_medicos.json', 'r') as arquivo:
            file = json.load(arquivo)
            for i in file:
                print(f'ID:{i['ID']} - Dr(a) {i['Nome']} - {i["Especializacao"]}')
            medico = int(input('Digite o ID do médico que deseja marcar a consulta: '))

        #parte 3 - escolher dia
        data_atual = dt.today()
        ultimo_dia_mes = (data_atual.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        dias = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
        while proximo_mes: #melhorar para mostrar apenas os dias que o medico tem horario
            data_corrente = data_atual
            indice = 1
            lista_dias_disponiveis = []
            while data_corrente <= ultimo_dia_mes:
                dia_da_semana = data_corrente.weekday()
                if dia_da_semana < 5:  # 0=segunda-feira, 4=sexta-feira
                    print(f"{indice}. {data_corrente.strftime('%d/%m/%Y')} - {dias[dia_da_semana]}")
                    indice += 1
                    lista_dias_disponiveis.append(data_corrente)
                data_corrente += timedelta(days=1)
            escolha_data = int(input("Selecione o indice da data a qual deseja fazer o agendamento, caso queira agendar para o próximo mes digite 0!\n Escolha: "))
            if escolha_data > indice:
                print('Data inválida!')
            elif escolha_data != 0:
                proximo_mes = False
                data = lista_dias_disponiveis[escolha_data - 1] #para pegar o dia
            elif escolha_data == 0:
                data_atual = (data_atual.replace(day=28) + timedelta(days=4)).replace(day=1)
                ultimo_dia_mes = (data_atual.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

        #parte 4 - escolher horario, disponiveis do dia do medico
        with open ("agenda.json",'r') as arquivo:
            file = json.load(arquivo)
            horarios_ofertados = ['8:00', '9:00', '10:00','11:00','13:00','14:00', '15:00', '16:00', '17:00']
            #rodará todo o arquivo e 'apagara' os horarios do dia
            for i,itens in file.items():
                for j in range(len(itens)):
                    if itens[j]['dia'] == str(data) and itens[j]['id_medico'] == medico:
                        horarios_ofertados.remove(itens[j]['hora'])
            indice = 1
            for i in horarios_ofertados:
                print(f'{indice}. {i}')
                indice+=1
            horario = int(input('Escolha o horário desejado entre os horários disponíveis: '))  
    except FileNotFoundError:
        print("The file 'lista_medicos.json' was not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON from the file. Ensure the JSON is properly formatted.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    
agendamento()