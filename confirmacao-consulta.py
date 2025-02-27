
import smtplib
import os
import time
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import logging
import os
from dotenv import load_dotenv


logging.basicConfig(
    filename="envio_lembretes.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")


load_dotenv()

email_gerenciador = os.getenv('EMAIL_REMETENTE')
password_gerenciador = os.getenv('PASSWORD')

# Função para enviar o e-mail com anexo

def enviar_email(destinatario, nome_paciente, data_consulta, imagem_anexo=None):
    msg = MIMEMultipart()
    msg['From'] = email_gerenciador
    msg['To'] = destinatario
    msg['Subject'] = "Confirmação da sua consulta"

    
    corpo_email = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 20px; max-width: 600px; margin: auto;">
            <h2 style="color: #2c3e50; text-align: center;">Confirmação de Consulta</h2>
            <p>Olá <strong>{nome_paciente}</strong>,</p>
            <p>Sua consulta foi confirmada para o dia <strong>{data_consulta}</strong>.</p>
            <p>Qualquer dúvida, entre em contato conosco.</p>
            <br>
            <p style="text-align: center; font-size: 14px; color: #777;">Atenciosamente, <br> <strong>Sua Clínica</strong></p>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(corpo_email, 'html'))


    imagem_anexo = 'Confirmacao-de-consulta.png'
    # Anexar a imagem 
    if imagem_anexo and os.path.exists(imagem_anexo):
        with open(imagem_anexo, "rb") as img:
            mime_img = MIMEImage(img.read(), name="imagem.jpg")
            mime_img.add_header("Content-ID", "<minhaimagem>")  #pra deixar a imagem in line
            msg.attach(mime_img)

    # envia o e-mail
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



# Monitoramento das confirmações / pra n dar erro ne

def monitorar_confirmacoes(arquivo_dados, arquivo_nomes, imagem_anexo=None):
    consultas_confirmadas = set()

    while True:
        # JSON DAS CONSULTAS (AGENDA.JSON)
        with open('agenda.json',encoding='utf-8') as arquivo_agenda:
            consultas = json.load(arquivo_agenda)  

        # JSON DOS PACIENTES (PACIENTES.JSON)

        with open('pacientes.json', encoding='utf-8') as arquivo_paciente:
            pacientes = json.load(arquivo_paciente)

        for consulta in consultas:
            email = consulta["email"]
            data_consulta = consulta["data"]
            confirmado = consulta["confirmado"]

            if confirmado.lower() == "confirmado" and email not in consultas_confirmadas:
                consultas_confirmadas.add(email)

                # Buscar o nome do paciente
                nome_paciente = pacientes.get(email, "Paciente")  # Busca o nome pelo e-mail

                # Enviar o e-mail de confirmação
                enviar_email(email, nome_paciente, data_consulta, imagem_anexo)

        time.sleep(10)  # Verifica a cada 10 segundos

# Executando................
monitorar_confirmacoes("consultas.json", "pacientes.json", "imagem_anexo.jpg")