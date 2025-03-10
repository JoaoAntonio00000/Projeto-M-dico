import json
import datetime
import smtplib
import logging
import schedule
import time
from email.message import EmailMessage
from dotenv import load_dotenv
import os

# Configuração do log
logging.basicConfig(
    filename="envio_lembretes.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

load_dotenv()

email_gerenciador = os.getenv('EMAIL_REMETENTE')
password_gerenciador = os.getenv('PASSWORD')

# Função para buscar o nome do paciente
def nome_lembrete(email_pacient):
    try:
        with open('pacientes.json', 'r', encoding='utf-8') as arquivo_paciente:
            data = json.load(arquivo_paciente)
            pacientes = data['pacientes']  # Acessa a lista dentro da chave "pacientes"
        return next((p['nome'] for p in pacientes if p['email'] == email_pacient), "Paciente sem identificação")
    except FileNotFoundError:
        logging.error("Arquivo pacientes.json não encontrado.")
        return "Paciente sem identificação"
    except json.JSONDecodeError:
        logging.error("Erro ao decodificar pacientes.json.")
        return "Paciente sem identificação"
    except KeyError:
        logging.error("Chave 'pacientes' não encontrada no arquivo pacientes.json.")
        return "Paciente sem identificação"


# Função para carregar os IDs de consultas já enviadas
def carregar_enviados():
    try:
        with open('enviados.json', 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []  # Se o arquivo não existir, retorna lista vazia
    except json.JSONDecodeError:
        logging.error("Erro ao decodificar enviados.json.")
        return []

# Função para salvar os IDs de consultas enviadas
def salvar_enviados(enviados):
    with open('enviados.json', 'w', encoding='utf-8') as arquivo:
        json.dump(enviados, arquivo, ensure_ascii=False, indent=4)



# Função para enviar e-mail de lembrete
def enviar_email_confirmacao(destinatario, nome_paciente, codigo_confirmacao, data_consulta, hora_consulta, imagem_rodape='cabecalho-do-email.png'):
    msg = EmailMessage()
    msg['Subject'] = '📅 Lembrete de Consulta'
    msg['From'] = email_gerenciador
    msg['To'] = destinatario

    # Corpo do e-mail em HTML
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; text-align: center;">
        <h2 style="color: #2E86C1;">Olá, {nome_paciente}!</h2>
        <p style="font-size: 18px;">Este é um lembrete de que você tem uma consulta agendada.</p>
        <p style="font-size: 20px;"><strong>📅 Data:</strong> {data_consulta}</p>
        <p style="font-size: 20px;"><strong>⏰ Horário:</strong> {hora_consulta}</p>
        <p style="font-size: 16px;">Por favor, insira o código a seguir no /consulta do nosso telegram: <strong>{codigo_confirmacao}</strong>, para confirmar seu agendamento.</p>
        <p style="font-size: 16px;">Se precisar remarcar, entre em contato com a clínica.</p>
        <br>
        <p style="color: gray; font-size: 14px;">Este é um e-mail automático, por favor, não responda.</p>
        <br>
        <footer style="margin-top: 20px;">
            <img src="cid:imagem_assinatura" alt="Assinatura Digital" style="width: 600; height: auto;">
        </footer>
    </body>
    </html>
    """

    msg.add_alternative(html_message, subtype='html')

    # Adiciona a imagem inline
    if imagem_rodape:
        with open(imagem_rodape, 'rb') as img_file:
            img_data = img_file.read()
            msg.get_payload()[0].add_related(img_data, maintype='image', subtype='png', cid='imagem_assinatura')

    # Enviar e-mail
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_gerenciador, password_gerenciador)
            server.send_message(msg)
            log_message = f'E-mail de lembrete enviado para: {destinatario}'
            logging.info(log_message)
            print(log_message)
    except Exception as e:
        log_error = f'Ocorreu um erro ao enviar o e-mail para {destinatario}. Erro: {e}'
        logging.error(log_error)
        print(log_error)


# Função para verificar e enviar os e-mails
def verificar_envio():
    try:
        with open('agenda.json', 'r',   encoding='utf-8') as arquivo_agenda:
            agendamentos = json.load(arquivo_agenda)

        enviados = carregar_enviados()  # Carrega a lista de consultas já enviadas
        now = datetime.datetime.now()

        now = datetime.datetime.now()

        for dia, consultas in agendamentos.items():# Depuração

            if not isinstance(consultas, list):
                print(f"⚠️ ERRO: O valor de {dia} não é uma lista! Tipo encontrado: {type(consultas)}")
                continue  # Pula esse dia

            for consulta in consultas:
                
                id_consulta = consulta.get('id_consulta')
                if id_consulta in enviados:
                    continue

                if not isinstance(consulta, dict):
                    print(f"⚠️ ERRO: Consulta não é um dicionário! Tipo encontrado: {type(consulta)}")
                    continue  # Pula essa consulta

                email = consulta['email_paciente']  # Teste de acesso
                print(f"Email do paciente: {email}")  # Depuração

                data_consulta = consulta['dia']
                hora_consulta = consulta['hora']
                codigo_confirmacao = consulta["codigo_consulta"]

                data_hora = datetime.datetime.strptime(f"{data_consulta} {hora_consulta}", "%Y-%m-%d %H:%M")
                lembrete = data_hora - datetime.timedelta(hours=24)

                if now >= lembrete and now < data_hora:
                    nome_paciente = nome_lembrete(email)
                    enviar_email_confirmacao(email, nome_paciente, codigo_confirmacao, data_consulta, hora_consulta)
                    enviados.append(id_consulta)  # Marca como enviado
                    salvar_enviados(enviados)  # Salva a lista atualizada
    except Exception as e:
        logging.error(f"Erro ao verificar os envios: {e}")
        print(f"Erro ao verificar os envios: {e}")


# Agendamento do envio dos lembretes
schedule.every(1).minute.do(verificar_envio)
print("⏳ Sistema de lembrete de consultas iniciado...")
while True:
    schedule.run_pending()
    time.sleep(10)