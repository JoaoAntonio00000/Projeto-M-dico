import json
import smtplib
import logging
import schedule
import time
from email.message import EmailMessage
from dotenv import load_dotenv
import os

# Configuração do log
logging.basicConfig(
    filename="envio_confirmacoes.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

load_dotenv()

email_gerenciador = os.getenv('EMAIL_REMETENTE')
password_gerenciador = os.getenv('PASSWORD')

# Função para buscar o nome do paciente
def nome_confirmacao(email_pacient):
    try:
        with open('pacientes.json', 'r', encoding='utf-8') as arquivo_paciente:
            data = json.load(arquivo_paciente)
            pacientes = data['pacientes']
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

# Função para carregar os IDs de confirmações já enviadas
def carregar_enviados():
    try:
        with open('enviados_confirmacoes.json', 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        logging.error("Erro ao decodificar enviados_confirmacoes.json.")
        return []

# Função para salvar os IDs de confirmações enviadas
def salvar_enviados(enviados):
    with open('enviados_confirmacoes.json', 'w', encoding='utf-8') as arquivo:
        json.dump(enviados, arquivo, ensure_ascii=False, indent=4)

# Função para carregar o estado anterior da agenda
def carregar_estado_anterior():
    try:
        with open('agenda_anterior.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        logging.error("Erro ao decodificar agenda_anterior.json.")
        return {}

# Função para salvar o estado atual como anterior
def salvar_estado_anterior(agendamentos):
    with open('agenda_anterior.json', 'w', encoding='utf-8') as f:
        json.dump(agendamentos, f, ensure_ascii=False, indent=4)

# Função para enviar e-mail de confirmação
def enviar_email_confirmacao(destinatario, nome_paciente, data_consulta, hora_consulta, imagem_rodape='cabecalho-do-email.png'):
    msg = EmailMessage()
    msg['Subject'] = '✅ Consulta Confirmada'
    msg['From'] = email_gerenciador
    msg['To'] = destinatario

    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; text-align: center;">
        <h2 style="color: #2E86C1;">Olá, {nome_paciente}!</h2>
        <p style="font-size: 18px;">Sua consulta foi confirmada com sucesso!</p>
        <p style="font-size: 20px;"><strong>📅 Data:</strong> {data_consulta}</p>
        <p style="font-size: 20px;"><strong>⏰ Horário:</strong> {hora_consulta}</p>
        <p style="font-size: 16px;">Aguardamos você no dia e horário marcados. Se precisar remarcar, entre em contato com a clínica.</p>
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

    if imagem_rodape:
        with open(imagem_rodape, 'rb') as img_file:
            img_data = img_file.read()
            msg.get_payload()[0].add_related(img_data, maintype='image', subtype='png', cid='imagem_assinatura')

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_gerenciador, password_gerenciador)
            server.send_message(msg)
            log_message = f'E-mail de confirmação enviado para: {destinatario}'
            logging.info(log_message)
            print(log_message)
    except Exception as e:
        log_error = f'Ocorreu um erro ao enviar o e-mail de confirmação para {destinatario}. Erro: {e}'
        logging.error(log_error)
        print(log_error)

# Função para verificar e enviar as confirmações
def verificar_confirmacao():
    try:
        with open('agenda.json', 'r', encoding='utf-8') as arquivo_agenda:
            agendamentos = json.load(arquivo_agenda)

        enviados = carregar_enviados()
        agenda_anterior = carregar_estado_anterior()

        for dia, consultas in agendamentos.items():
            if not isinstance(consultas, list):
                print(f"⚠️ ERRO: O valor de {dia} não é uma lista! Tipo encontrado: {type(consultas)}")
                continue

            consultas_anteriores = agenda_anterior.get(dia, [])

            for consulta in consultas:
                if not isinstance(consulta, dict):
                    print(f"⚠️ ERRO: Consulta não é um dicionário! Tipo encontrado: {type(consulta)}")
                    continue

                id_consulta = consulta.get('id_consulta')
                if id_consulta in enviados:
                    continue

                email = consulta['email_paciente']
                data_consulta = consulta['dia']
                hora_consulta = consulta['hora']
                status_atual = consulta.get('confirmacao_paciente')

                consulta_anterior = next((c for c in consultas_anteriores if c.get('id_consulta') == id_consulta), None)
                status_anterior = consulta_anterior.get('confirmacao_paciente') if consulta_anterior else None

                if status_anterior == 'pendente' and status_atual == 'confirmado':
                    nome_paciente = nome_confirmacao(email)
                    enviar_email_confirmacao(email, nome_paciente, data_consulta, hora_consulta)
                    enviados.append(id_consulta)
                    salvar_enviados(enviados)

        salvar_estado_anterior(agendamentos)

    except Exception as e:
        logging.error(f"Erro ao verificar as confirmações: {e}")
        print(f"Erro ao verificar as confirmações: {e}")

# Agendamento do envio das confirmações
schedule.every(1).minute.do(verificar_confirmacao)
print("⏳ Sistema de confirmação de consultas iniciado...")
while True:
    schedule.run_pending()
    time.sleep(60)