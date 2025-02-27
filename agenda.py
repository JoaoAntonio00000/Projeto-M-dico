'''
Essa agenda fica no json
so faz a questao de adicionar e modificar ela no terminal , e pensar ja como integrar pelo telegram

cada vez que acessar a agenda ja faz uma limpa nela e adicona no log os que ja foram

console.print agenda diaria

cancelar

mudar horario
'''
import json
from datetime import date as dt
from datetime import timedelta,datetime
from criando_lista_pacientes import cadastrar
from rich.console import Console
console = Console()

def cancelar():
    try:
        with open("agenda.json", "r") as f:
            agenda = json.load(f)

        while True:
            escolha = console.input("[bold cyan]Deseja cancelar por dia (1) ou por ID da consulta (2)? (Digite 0 para voltar) ")

            if escolha == "0":
                return

            if escolha == "1":
                hoje = dt.today()
                mes_atual = hoje.month
                consultas_mes = {}

                # Mapeia datas para o nome do dia da semana
                for dia_semana, consultas in agenda.items():
                    for consulta in consultas:
                        data_consulta = datetime.strptime(consulta["dia"], "%Y-%m-%d")
                        if data_consulta.month == mes_atual:
                            data_formatada = data_consulta.strftime("%d/%m/%Y")
                            consultas_mes.setdefault(data_formatada, []).append((dia_semana, consulta))

                if not consultas_mes:
                    console.print("[bold red]Nenhuma consulta encontrada para este mês.")
                    return

                while True:
                    console.print("[bold cyan]Dias com consultas no mês atual:")
                    for data in sorted(consultas_mes.keys()):
                        console.print(f"[bold yellow]{data}")

                    dia_escolhido = console.input("[bold cyan]Digite a data no formato DD/MM/AAAA (ou 0 para voltar): ")

                    if dia_escolhido == "0":
                        break  # Volta para a escolha entre dia ou ID

                    if dia_escolhido not in consultas_mes:
                        console.print("[bold red]Nenhuma consulta encontrada para essa data.")
                        continue

                    while True:
                        console.print(f"[bold cyan]Consultas para {dia_escolhido}:")
                        consultas_do_dia = consultas_mes[dia_escolhido]

                        for idx, (dia_semana, consulta) in enumerate(consultas_do_dia, 1):
                            console.print(f"{idx}. [bold yellow]ID {consulta['id_consulta']} - {consulta['hora']} - {consulta['medico']}")

                        escolha_cancelar = console.input("[bold cyan]Digite o número da consulta para cancelar (ou 0 para voltar): ")

                        if escolha_cancelar == "0":
                            break  # Volta para a escolha da data

                        try:
                            escolha_cancelar = int(escolha_cancelar) - 1
                            if 0 <= escolha_cancelar < len(consultas_do_dia):
                                dia_semana, consulta_a_remover = consultas_do_dia[escolha_cancelar]
                                agenda[dia_semana].remove(consulta_a_remover)

                                with open("agenda.json", "w") as f:
                                    json.dump(agenda, f, indent=4, ensure_ascii=False)

                                console.print("[bold green]Consulta cancelada com sucesso!")
                                return  # Sai da função após cancelar

                            else:
                                console.print("[bold red]Escolha inválida.")

                        except ValueError:
                            console.print("[bold red]Digite um número válido.")

            elif escolha == "2":
                while True:
                    id_consulta = console.input("[bold cyan]Digite o ID da consulta a ser cancelada (ou 0 para voltar): ")

                    if id_consulta == "0":
                        break  # Volta para a escolha entre dia ou ID

                    try:
                        id_consulta = int(id_consulta)
                        consulta_encontrada = False

                        for dia_semana, consultas in agenda.items():
                            for consulta in consultas:
                                if consulta["id_consulta"] == id_consulta:
                                    agenda[dia_semana].remove(consulta)
                                    consulta_encontrada = True

                                    with open("agenda.json", "w") as f:
                                        json.dump(agenda, f, indent=4, ensure_ascii=False)

                                    console.print("[bold green]Consulta cancelada com sucesso!")
                                    return  # Sai da função após cancelar

                        if not consulta_encontrada:
                            console.print("[bold red]Consulta não encontrada!")

                    except ValueError:
                        console.print("[bold red]Digite um número válido.")

    except FileNotFoundError:
        console.print("[bold red]Arquivo de agenda não encontrado.")
    except json.JSONDecodeError:
        console.print("[bold red]Erro ao ler o arquivo JSON. Verifique a formatação.")
    except Exception as e:
        console.print(f"[bold red]Ocorreu um erro inesperado: {e}")



def obter_semana(data_str):
    return datetime.strptime(data_str, "%Y-%m-%d").isocalendar()[1]

#verifica quais dias o medico esta livre
def verifica_disponibilidade_medico(arquivo):
    console.print('[bold red]Ainda nada')

#mudar a lista de horarios da medico para false de acordo com a agenda, fechada de segunda a sexta
def agenda_para_lista_medico():
    hoje = dt.today()

    # Criar um dicionário para armazenar a data correta de cada dia da semana
    dias_semana = ["segunda", "terca", "quarta", "quinta", "sexta"]
    datas_semana = {}

    for i, dia in enumerate(dias_semana):
        # Calcular a data correspondente a esse dia nesta semana
        data_atual_semana = hoje - timedelta(days=hoje.weekday()) + timedelta(days=i)
        
        # Se a data já passou, usamos a mesma data na próxima semana
        if data_atual_semana < hoje:
            data_atual_semana += timedelta(weeks=1)

        datas_semana[dia] = data_atual_semana

    # Carregar os arquivos JSON
    with open("agenda.json", "r") as f:
        agenda_anual = json.load(f)

    with open("lista_medicos.json", "r") as f:
        agenda_semanal = json.load(f)

    # Atualizar a agenda semanal progressivamente
    for dia, data_referencia in datas_semana.items():
        semana_referencia = data_referencia.isocalendar()[1]

        # Atualizar os horários da agenda semanal com base na agenda anual da semana correta
        for consulta in agenda_anual.get(dia, []):
            if obter_semana(consulta["dia"]) != semana_referencia:
                continue  # Ignora consultas que não pertencem à semana correta
            
            medico_id = consulta["id_medico"]
            hora = int(consulta["hora"].split(":")[0])  # Extrai a hora inteira
            
            # Buscar o médico correspondente na agenda semanal
            for medico in agenda_semanal:
                if medico["ID"] == medico_id:
                    # Atualizar apenas o dia correto na agenda semanal
                    if str(hora) in medico["Hora do Medico"].get(dia.capitalize(), {}):
                        medico["Hora do Medico"][dia.capitalize()][str(hora)] = False

    # Salvar a agenda semanal atualizada
    with open("agenda_semanal_atualizada.json", "w", encoding="utf-8") as f:
        json.dump(agenda_semanal, f, indent=4, ensure_ascii=False)

    console.print("[bold green]Agenda semanal progressivamente atualizada!")
    
#agendamento feito pelo terminal
def agendamento():
    proximo_mes = True #Enquanto não ficar false vai passando para o proximo mes, no agendamento do dia
    try:
        #parte 1 - Paciente já cadastrado, se nao estiver por favor vá para o cadastramento pelo terminal
        id_paciente = int(console.input("[bold cyan]Digite o id do paciente: "))
        #verificação de id
        with open('pacientes.json','r') as arquivo:
            file = json.load(arquivo)
            paciente_existe = False
            for i in range (len(file['pacientes'])):
                if file["pacientes"][i]['ID_PACIENTE'] == id_paciente:
                    paciente_existe = True
                    j = i
            if paciente_existe:
                email = file["pacientes"][int(j)]['email'] 
            else:
                console.print('[bold red]ID não encontrado, por favor faça o cadastramento!\nRedirecionando!')
                cadastrar()

        #parte 2 - tipo de consulta
        tipo_consulta = console.input('[bold cyan]Digite o tipo de consulta: ')
        #parte 3 - escolher medico
        with open('lista_medicos.json', 'r') as arquivo:
            file = json.load(arquivo)
            for i in file:
                console.print(f'[bold cyan]ID:{i['ID']} - Dr(a) {i['Nome']} - {i["Especializacao"]}')
            id_medico = int(console.input('[bold cyan]Digite o ID do médico que deseja marcar a consulta: '))
            for i in file:
                if id_medico == i['ID']:
                    medico = i['Nome']

        #parte 4 - escolher dia
        data_atual = dt.today()
        ultimo_dia_mes = (data_atual.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        dias = ["segunda", "terca", "quarta", "quinta", "sexta", "sábado", "domingo"]
        while proximo_mes: #melhorar para mostrar apenas os dias que o medico tem horario
            data_corrente = data_atual
            indice = 1
            lista_dias_disponiveis = []
            while data_corrente <= ultimo_dia_mes:
                dia_da_semana = data_corrente.weekday()
                if dia_da_semana < 5:  # 0=segunda-feira, 4=sexta-feira
                    console.print(f"[bold cyan]{indice}. {data_corrente.strftime('%d/%m/%Y')} - {dias[dia_da_semana]}")
                    indice += 1
                    lista_dias_disponiveis.append(data_corrente)
                data_corrente += timedelta(days=1)
            escolha_data = int(console.input("[bold cyan]Selecione o indice da data a qual deseja fazer o agendamento, caso queira agendar para o próximo mes digite 0!\n Escolha: "))
            if escolha_data > indice:
                console.print('[bold red]Data inválida!')
            elif escolha_data != 0:
                proximo_mes = False
                data = lista_dias_disponiveis[escolha_data - 1] #para pegar o dia
            elif escolha_data == 0:
                data_atual = (data_atual.replace(day=28) + timedelta(days=4)).replace(day=1)
                ultimo_dia_mes = (data_atual.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

        #parte 5 - escolher horario, disponiveis do dia do medico
        try:
            with open ("agenda.json",'r') as arquivo:
                file = json.load(arquivo)
                horarios_ofertados = ['8:00', '9:00', '10:00','11:00','13:00','14:00', '15:00', '16:00', '17:00']
                #rodará todo o arquivo e 'apagara' os horarios do dia
                for i,itens in file.items():
                    for j in range(len(itens)):
                        if itens[j]['dia'] == str(data) and itens[j]['id_medico'] == id_medico:
                            horarios_ofertados.remove(itens[j]['hora'])
                indice = 1
                for i in horarios_ofertados:
                    console.print(f'[bold cyan]{indice}. {i}')
                    indice+=1
                escolha_horario = int(console.input('[bold cyan]Escolha o horário desejado entre os horários disponíveis: '))  
                horario = horarios_ofertados[escolha_horario-1]
        except FileNotFoundError:
            #caso arquivo não criado
            horarios_ofertados = ['8:00', '9:00', '10:00','11:00','13:00','14:00', '15:00', '16:00', '17:00']
            indice = 1
            for i in horarios_ofertados:
                console.print(f'[bold cyan]{indice}. {i}')
                indice+=1
            escolha_horario = int(console.input('[bold cyan]Escolha o horário desejado entre os horários disponíveis: '))
            horario = horarios_ofertados[escolha_horario-1]
        except json.JSONDecodeError:
            console.print("[bold red]Error decoding JSON from the file. Ensure the JSON is properly formatted.")
        except Exception as e:
            console.print(f"[bold red]An unexpected error occurred: {e}")

        try:
            with open("id_consulta.json","r") as file:
                arquivo = json.load(file)
                id_consulta = arquivo["id"] + 1
            with open("id_consulta.json","w") as file:
                dados = {"id":id_consulta}
                json.dump(dados,file)
            
        except FileNotFoundError:
            with open("id_consulta.json","w") as file:
                dados = {"id":1}
                json.dump(dados,file)
        except json.JSONDecodeError:
            console.print("[bold red]Error decoding JSON from the file. Ensure the JSON is properly formatted.")
        except Exception as e:
            console.print(f"[bold red]An unexpected error occurred: {e}")
        dia_da_semana = data.weekday()
        dia_semana = dias[dia_da_semana]
        nova_consulta = {

                    "id_consulta": id_consulta,
                    "dia": str(data),
                    "hora": horario,
                    "confirmacao_paciente": "pendente",
                    "medico": medico,
                    "id_medico": id_medico,
                    "tipo_de_consulta": tipo_consulta,
                    "id_paciente": id_paciente,
                    "email_paciente": email,
                }
        try:
            with open("agenda.json", "r") as arquivo:
                agenda = json.load(arquivo)
        except FileNotFoundError:
            agenda = {"segunda": [], "terca": [], "quarta": [], "quinta": [], "sexta": []}
        agenda[dia_semana.lower()].append(nova_consulta)
        with open("agenda.json", "w") as arquivo:
            json.dump(agenda, arquivo, indent=4)
        console.print('[bold green]Agendamento realizado.')
    except FileNotFoundError:
        console.print("The file 'lista_medicos.json' was not found.")
    except json.JSONDecodeError:
        console.print("[bold red]Error decoding JSON from the file. Ensure the JSON is properly formatted.")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}")
# Iniciar o programa
if __name__ == "__main__":
    agendamento()
    agenda_para_lista_medico()