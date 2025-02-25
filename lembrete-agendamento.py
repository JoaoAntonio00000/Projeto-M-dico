'''
Criar um codigo que leia os emails das consultas e dos pacientes e envie um email lembrando-o da consulta 24h antes do horario marcado
'''

import json
import datetime
import smtplib
import email
import schedule
import logging
from email.message import EmailMessage
from dotenv import load_dotenv
import os


load_dotenv()

email_gerenciador = os.getenv('EMAIL_REMETENTE')
password = os.getenv('PASSWORD')



def salvar_dados():

    with open('pacientes.json', 'r', encoding= 'utf-8') as arquivo_paciente:
        pacientes = json.load(arquivo_paciente)

    # Abrindo o arquivo original e carregando os dados
    with open('agenda.json', 'r', encoding='utf-8') as arquivo_agenda:
        agendamentos = json.load(arquivo_agenda)  # Carrega os dados do JSON

    lembrete= []
    # Salvando em um novo arqui vo JSON

    for consulta in agendamentos:
        email = consulta.get('email')
        hora = consulta.get('hora')
        data = consulta.get('data')
        

    with open('emails_paciente_lembrete.json', 'w', encoding='utf-8') as arquivo:
        json.dump(lembrete, arquivo, ensure_ascii=False, indent=4)

    print("Arquivo 'emails_paciente_lembrete.json' salvo com sucesso!")

# Executando a função
salvar_dados()


def enviar_lembrete():






    msg = EmailMessage()
    msg['Subject'] = 'Lembrete de consulta agendada'
    msg['From'] = email_gerenciador
    msg['To'] = destinatario
    msg.set_content(mensagem)


# para nao esquecer - buscar o nome do paciente da lista json de pacientes - porém, buscar o horario =, email e data a ser enviado da lista de agendamentos json - Agr, pensar se é melhor ou nao criar um arquivo json com os emails e tudo que deve ser enviado do mesmo e deixar salvos