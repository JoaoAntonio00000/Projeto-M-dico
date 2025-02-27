from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
import json
import os
import datetime

ARQUIVO_AGENDA = "agenda.json"
ARQUIVO_PACIENTES = "pacientes.json"
ARQUIVO_MEDICOS = "lista_medicos.json"

# Definição dos estados da conversa
DIGITAR_ID_CPF, ESCOLHER_MEDICO, ESCOLHER_DIA, ESCOLHER_HORARIO = range(4)

# Lista de horários disponíveis
horarios_disponiveis = ["08:00", "09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

# Função para obter os próximos 5 dias úteis
DIAS_SEMANA_PT = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
}

def dias_uteis():
    hoje = datetime.datetime.now()
    dias = []
    contador = 0

    while len(dias) < 5:
        data = hoje + datetime.timedelta(days=contador)
        nome_dia = data.strftime("%A")  # Obtém o nome do dia em inglês
        if nome_dia in DIAS_SEMANA_PT:  # Apenas dias úteis (segunda a sexta)
            nome_dia_pt = DIAS_SEMANA_PT[nome_dia]
            dias.append((f"{nome_dia_pt} - {data.strftime('%d/%m')}", data.strftime("%Y-%m-%d")))
        contador += 1

    return dias
async def iniciar_agendamento(update: Update, context: CallbackContext) -> int:
    """ Inicia o processo de agendamento pedindo ID ou CPF. """
    await update.message.reply_text("Por favor, digite seu *ID* ou *CPF* para continuar:", parse_mode="Markdown")
    return DIGITAR_ID_CPF

async def receber_id_ou_cpf(update: Update, context: CallbackContext) -> int:
    """ Verifica se o ID ou CPF existe e prossegue. """
    user_input = update.message.text
    paciente_encontrado = None

    try:
        with open(ARQUIVO_PACIENTES, "r", encoding="utf-8") as file:
            dados = json.load(file)

        for paciente in dados.get("pacientes", []):
            if str(paciente.get("ID_PACIENTE")) == user_input or paciente.get("cpf") == user_input:
                paciente_encontrado = paciente
                break

        if not paciente_encontrado:
            await update.message.reply_text("⚠ ID ou CPF não encontrado. Digite novamente ou use /cancelar para sair.")
            return DIGITAR_ID_CPF

        context.user_data["id_paciente"] = paciente_encontrado["ID_PACIENTE"]
        context.user_data["email_paciente"] = paciente_encontrado.get("email", "não informado")

        # Criar os botões para escolha do médico
        with open(ARQUIVO_MEDICOS, "r", encoding="utf-8") as file:
            dados = json.load(file)

        buttons = [[InlineKeyboardButton(f'ID:{medico["ID"]} - Dr(a) {medico["Nome"]} - {medico["Especializacao"]}', callback_data=str(medico["ID"]))] for medico in dados ]
        reply_markup = InlineKeyboardMarkup(buttons)

        await update.message.reply_text("Escolha um médico para a consulta:", reply_markup=reply_markup)
        return ESCOLHER_MEDICO

    except FileNotFoundError:
        await update.message.reply_text("Erro: Banco de dados não encontrado.")
        return ConversationHandler.END

async def escolher_medico(update: Update, context: CallbackContext) -> int:
    """ Armazena o médico escolhido. """
    query = update.callback_query
    await query.answer()

    with open(ARQUIVO_MEDICOS, "r", encoding="utf-8") as file:
        dados = json.load(file)

    for medico in dados:
        if query.data == str(medico["ID"]):
            context.user_data["id_medico"] = medico["ID"]
            context.user_data["medico"] = medico["Nome"]
            break

    # Criar botões com os dias úteis
    dias = dias_uteis()
    buttons = [[InlineKeyboardButton(text=dia[0], callback_data=dia[1])] for dia in dias]
    reply_markup = InlineKeyboardMarkup(buttons)

    await query.edit_message_text("Escolha um dia para a consulta:", reply_markup=reply_markup)
    return ESCOLHER_DIA

async def escolher_dia(update: Update, context: CallbackContext) -> int:
    """ Armazena o dia escolhido. """
    query = update.callback_query
    await query.answer()

    context.user_data["dia"] = query.data

    try:
        with open ("agenda.json",'r') as arquivo:
            file = json.load(arquivo)
            horarios_ofertados = ['8:00', '9:00', '10:00','11:00','13:00','14:00', '15:00', '16:00', '17:00']
            #rodará todo o arquivo e 'apagara' os horarios do dia
            for i,itens in file.items():
                for j in range(len(itens)):
                    if itens[j]['dia'] == str(context.user_data["dia"]) and itens[j]['id_medico'] == context.user_data["id_medico"]:
                        horarios_ofertados.remove(itens[j]['hora'])
    except FileNotFoundError:
        print("Arquivo nao encontrado.")
    except json.JSONDecodeError:
        print("Error decoding JSON from the file. Ensure the JSON is properly formatted.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    # Criar botões com os horários disponíveis
    buttons = [[InlineKeyboardButton(text=hora, callback_data=hora)] for hora in horarios_ofertados]
    reply_markup = InlineKeyboardMarkup(buttons)

    await query.edit_message_text("Escolha um horário para a consulta:", reply_markup=reply_markup)
    return ESCOLHER_HORARIO

async def finalizar_agendamento(update: Update, context: CallbackContext) -> int:
    """ Salva o agendamento no arquivo agenda.json. """
    query = update.callback_query
    await query.answer()

    id_paciente = context.user_data["id_paciente"]
    email = context.user_data["email_paciente"]
    data = context.user_data["dia"]
    horario = query.data
    medico = context.user_data["medico"]
    id_medico = context.user_data["id_medico"]
    tipo_consulta = "presencial"

    nova_consulta = {
        "dia": data,
        "hora": horario,
        "confirmacao_paciente": "pendente",
        "medico": medico,
        "id_medico": id_medico,
        "tipo_de_consulta": tipo_consulta,
        "id_paciente": id_paciente,
        "email_paciente": email,
    }

    # Verifica se o arquivo "agenda.json" existe
    if os.path.exists(ARQUIVO_AGENDA):
        with open(ARQUIVO_AGENDA, "r", encoding="utf-8") as arquivo:
            try:
                agenda = json.load(arquivo)
            except json.JSONDecodeError:
                agenda = {"segunda": [], "terca": [], "quarta": [], "quinta": [], "sexta": []}
    else:
        agenda = {"segunda": [], "terca": [], "quarta": [], "quinta": [], "sexta": []}

    # Adiciona a nova consulta no JSON
    dia_semana = datetime.datetime.strptime(data, "%Y-%m-%d").weekday()
    dias_semana = ["segunda", "terca", "quarta", "quinta", "sexta"]
    agenda[dias_semana[dia_semana]].append(nova_consulta)

    with open(ARQUIVO_AGENDA, "w", encoding="utf-8") as arquivo:
        json.dump(agenda, arquivo, indent=4, ensure_ascii=False)

    # Mensagem de confirmação
    mensagem_confirmacao = f"""
    ✅ *Agendamento Confirmado!*

    📅 *Data:* {data}  
    ⏰ *Horário:* {horario}  
    👨‍⚕️ *Médico:* {medico}  
    🏥 *Tipo de consulta:* {tipo_consulta}  
    """

    await query.edit_message_text(mensagem_confirmacao, parse_mode="Markdown")
    return ConversationHandler.END

async def cancelar(update: Update, context: CallbackContext) -> int:
    """ Cancela o agendamento. """
    await update.message.reply_text("Agendamento cancelado.")
    return ConversationHandler.END

# Configuração do ConversationHandler
agendamento_handler = ConversationHandler(
    entry_points=[CommandHandler("consulta", iniciar_agendamento)],
    states={
        DIGITAR_ID_CPF: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_id_ou_cpf)],
        ESCOLHER_MEDICO: [CallbackQueryHandler(escolher_medico)],
        ESCOLHER_DIA: [CallbackQueryHandler(escolher_dia)],
        ESCOLHER_HORARIO: [CallbackQueryHandler(finalizar_agendamento)],
    },
    fallbacks=[CommandHandler("cancelar", cancelar)],
)
