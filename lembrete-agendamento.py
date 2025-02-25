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
    with open('emails_paciente_lembrete', 'w', encoding= 'utf-8') as arquivo:
        


def ler_agendamentos(destinatario, mensagem): 
    with open('agenda.json', 'r', encoding= 'utf-8') as arquivo:
        dados = json.load(arquivo)
    email = dados.get('email')
    hora = dados.get('hora')
    data = dados.get('dia')


def enviar_lembrete():
    msg = EmailMessage()
    msg['Subject'] = 'Lembrete de consulta agendada'
    msg['From'] = email_gerenciador
    msg['To'] = destinatario
    msg.set_content(mensagem)


# para nao esquecer - buscar o nome do paciente da lista json de pacientes - porém, buscar o horario =, email e data a ser enviado da lista de agendamentos json - Agr, pensar se é melhor ou nao criar um arquivo json com os emails e tudo que deve ser enviado do mesmo e deixar salvos