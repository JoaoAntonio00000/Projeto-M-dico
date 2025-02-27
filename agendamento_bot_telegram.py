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

# Mapeamento dos dias da semana para português
dias_semana_pt = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

def dias_uteis(offset=0):
    """ Retorna os próximos 5 dias úteis com base no offset."""
    hoje = datetime.datetime.now() + datetime.timedelta(weeks=offset)
    dias = []
    contador = 0

    while len(dias) < 5:
        data = hoje + datetime.timedelta(days=contador)
        if data.weekday() < 5:  # Segunda a sexta
            dia_semana = dias_semana_pt[data.strftime("%A")]
            dias.append((f"{dia_semana} - {data.strftime('%d/%m')}", data.strftime("%Y-%m-%d")))
        contador += 1

    return dias

async def iniciar_agendamento(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Por favor, digite seu *ID* ou *CPF* para continuar:", parse_mode="Markdown")
    return DIGITAR_ID_CPF

async def receber_id_ou_cpf(update: Update, context: CallbackContext) -> int:
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

        with open(ARQUIVO_MEDICOS, "r", encoding="utf-8") as file:
            dados = json.load(file)

        buttons = [[InlineKeyboardButton(f'ID:{medico["ID"]} - Dr(a) {medico["Nome"]} - {medico["Especializacao"]}', callback_data=str(medico["ID"]))] for medico in dados]
        reply_markup = InlineKeyboardMarkup(buttons)

        await update.message.reply_text("Escolha um médico para a consulta:", reply_markup=reply_markup)
        return ESCOLHER_MEDICO

    except FileNotFoundError:
        await update.message.reply_text("Erro: Banco de dados não encontrado.")
        return ConversationHandler.END

async def escolher_medico(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    with open(ARQUIVO_MEDICOS, "r", encoding="utf-8") as file:
        dados = json.load(file)

    for medico in dados:
        if query.data == str(medico["ID"]):
            context.user_data["id_medico"] = medico["ID"]
            context.user_data["medico"] = medico["Nome"]
            break

    dias = dias_uteis()
    buttons = [[InlineKeyboardButton(text=dia[0], callback_data=dia[1])] for dia in dias]
    buttons.append([InlineKeyboardButton("⏪ Semana Passada", callback_data="semana_passada"),
                    InlineKeyboardButton("Semana Seguinte ⏩", callback_data="semana_seguinte")])
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    if query.message.text != "Escolha um dia para a consulta:":
        await query.edit_message_text("Escolha um dia para a consulta:", reply_markup=reply_markup)
    
    return ESCOLHER_DIA

async def escolher_dia(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "semana_seguinte":
        context.user_data["offset"] = context.user_data.get("offset", 0) + 1
    elif query.data == "semana_passada":
        context.user_data["offset"] = context.user_data.get("offset", 0) - 1
    else:
        context.user_data["dia"] = query.data

        buttons = [[InlineKeyboardButton(text=hora, callback_data=hora)] for hora in horarios_disponiveis]
        buttons.append([InlineKeyboardButton("🔙 Voltar", callback_data="voltar")])
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        if query.message.text != "Escolha um horário para a consulta:":
            await query.edit_message_text("Escolha um horário para a consulta:", reply_markup=reply_markup)
        
        return ESCOLHER_HORARIO
    
    return await escolher_medico(update, context)

async def cancelar(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Agendamento cancelado.")
    return ConversationHandler.END

agendamento_handler = ConversationHandler(
    entry_points=[CommandHandler("consulta", iniciar_agendamento)],
    states={
        DIGITAR_ID_CPF: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_id_ou_cpf)],
        ESCOLHER_MEDICO: [CallbackQueryHandler(escolher_medico)],
        ESCOLHER_DIA: [CallbackQueryHandler(escolher_dia)],
        ESCOLHER_HORARIO: [CallbackQueryHandler(escolher_dia)],
    },
    fallbacks=[CommandHandler("cancelar", cancelar)],
)
