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

def ler_agendamentos(): 
    with open('agenda.json', 'r', encoding= 'utf-8') as arquivo:
        dados = json.load(arquivo)
    