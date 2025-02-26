'''
Criar um codigo que leia os emails das consultas e dos pacientes e envie um email lembrando-o da consulta 24h antes do horario marcado
'''

import json
import datetime
import smtplib
import email
import schedule
import time
import logging
from email.message import EmailMessage
from dotenv import load_dotenv
import os


# Configuração do log
logging.basicConfig(
    filename="envio_lembretes.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")




load_dotenv()

email_gerenciador = os.getenv('EMAIL_REMETENTE')
password_gerenciador = os.getenv('PASSWORD')


#buscando o nome do paciente pra enviar o email personalizado com o nome dos trem

def nome_lembrete(email_pacient):
    with open('pacientes.json', 'r', encoding= 'utf-8') as arquivo_paciente:
        pacientes = json.load(arquivo_paciente)
    return next((p['nome'] for p in pacientes if p['email'] == email_pacient), "Paciente sem identificação")


def 






def enviar_email_confirmacao(destinatario, nome_paciente, data_consulta, hora_consulta):
    msg = EmailMessage()
    msg['Subject'] = '📅 Lembrete de Consulta'
    msg['From'] = email_gerenciador
    msg['To'] = destinatario

    html_message = f""""
    <html>
    <body style="font-family: Arial, sans-serif; text-align: center;">
        <h2 style="color: #2E86C1;">Olá, {nome_paciente}!</h2>
        <p style="font-size: 18px;">Este é um lembrete de que você tem uma consulta agendada.</p>
        <p style="font-size: 20px;"><strong>📅 Data:</strong> {data_consulta}</p>
        <p style="font-size: 20px;"><strong>⏰ Horário:</strong> {hora_consulta}</p>
        <p style="font-size: 16px;">Se precisar remarcar, entre em contato com a clínica.</p>
        <br>
        <p style="color: gray; font-size: 14px;">Este é um e-mail automático, por favor, não responda.</p>
    </body>
    </html>

    """

    msg.add_alternative(html_message, subtype = 'html')
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_gerenciador, password_gerenciador)
            server.send_message(msg)
            log_message = f'E-mail de lembrete enviado para: {destinatario}'
            logging.info(log_message)
            print(log_message)

    except Exception as e:
        log_error = f'Ocorreu um erro o enviar o e-mail de lembre para: {destinatario}. Erro: {e}'
        logging.error(log_error)
        print(log_error)

def verificar_envio():
    try:
        with open('agendamento_semanal_atualizada.json', 'r', encoding= 'utf-8') as arquivo_agenda:
            agendamentos = json.load(arquivo_agenda)
        now = datetime.datetime.now()

        for consulta in agendamentos:
            email = consulta['email']
            data_consulta = consulta['data']
            hora_consulta = consulta['hora']
            #CONVERTER A HORA E Data
            data_hora = datetime.datetime.strftime(f'{data_consulta}{hora_consulta}','%D/%M/%A %H:%M' )
            #calculo das 24h antes
            lembrete = data_hora - datetime.timedelta(hours=24)

            #envio dos emails

            if now >= lembrete and now < data_hora:
                nome_paciente = nome_lembrete(email)
                enviar_email_confirmacao(email, nome_paciente, data_consulta, hora_consulta)
    except Exception as e:
        logging.error(f"Erro ao verificar os envios: {e}")
        print(f"Erro ao verificar os envios: {e}")



# Rodar a função de verificação a cada 1 hora

schedule.every(1).hours.do(verificar_envio)
print("⏳ Sistema de lembrete de consultas iniciado...")
while True:
    schedule.run_pending()
    time.sleep(60)



