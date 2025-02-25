
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext
from datetime import date, datetime

# Variáveis globais
horario = False
data = False
dias_da_semana = ["segunda", "terça", "quarta", "quinta", "sexta"]
#funções python
import datetime

def dias_uteis_com_callback():
    hoje = datetime.datetime.now()
    dia_inicial = hoje.strftime("%A").lower()

    # Converta os dias da semana de inglês para português
    traducao_dias = {
        "monday": "segunda",
        "tuesday": "terça",
        "wednesday": "quarta",
        "thursday": "quinta",
        "friday": "sexta",
        "saturday": "sábado",
        "sunday": "domingo"
    }
    dia_inicial_portugues = traducao_dias.get(dia_inicial, "segunda")

    indice_inicial = dias_da_semana.index(dia_inicial_portugues)
    dias_uteis = []

    for i in range(5):
        indice = (indice_inicial + i) % 5
        dia_da_semana = dias_da_semana[indice]

        data = hoje + datetime.timedelta(days=(i + 1))
        while data.weekday() >= 5:  # Pular fim de semana (sábado=5, domingo=6)
            data += datetime.timedelta(days=1)

        data_formatada = data.strftime("%Y-%m-%d")
        dia_e_data = f"{dia_da_semana.capitalize()} - {data.strftime('%d/%m')}"
        dias_uteis.append((dia_e_data, data_formatada))  # Adiciona o callback com a data formatada

    return dias_uteis 


# Função para responder ao comando /start 
async def start(update: Update, context) -> None:
    await update.message.reply_text(
        "Bem-vindo à Clínica CyberMedical!\n\n"
        "Para agendar uma consulta, digite /consulta.\n"
        "Caso necessite de outra assistência, digite /help.\n\n"
        "Estamos à disposição para atendê-lo da melhor forma possível!"
    )

# Função para lidar com mensagens de texto 
async def echo(update: Update, context) -> None:
    await update.message.reply_text(f'"Olá! Como posso auxiliá-lo? \n\nPara agendar uma consulta, por favor, digite /consulta.\n Se necessitar de qualquer outra assistência, digite /help.\n\n Estamos à disposição para atendê-lo da melhor forma possível.')

# Função para exibir botões de horários de consulta
async def marcar_consulta(update: Update, context: CallbackContext):
    global dias_da_semana
    global data
    #marcar dia
    dias_uteis = dias_uteis_com_callback()
    data = True
# Criação dos botões InlineKeyboardButton com callbacks
    buttons = [
        [InlineKeyboardButton(text=f'{dia}-{data}', callback_data=f"data_{data}") for dia, data in dias_uteis]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_text("Escolha um dia para a consulta:", reply_markup=reply_markup)
    #horario

    keyboard = [
        [InlineKeyboardButton("08:00", callback_data="horario_08"),
        InlineKeyboardButton("09:00", callback_data="horario_09")],
        [InlineKeyboardButton("10:00", callback_data="horario_10"),
        InlineKeyboardButton("11:00", callback_data="horario_11")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Escolha um horário para a consulta:", reply_markup=reply_markup)

# Função para exibir os comandos disponíveis
async def help(update: Update, context) -> None:
    await update.message.reply_text(
        "Comandos disponíveis: \n"
        "  /start - Mensagem inicial\n"
        "  /help - Lista todos os comandos\n"
        "  /foto - Envia uma foto\n"
        "  /consulta - Agendar uma consulta\n"
    )

# Função para enviar uma imagem
async def imagem(update: Update, context) -> None:
    await update.message.reply_photo("Confirmação-de-consulta.png") 

# Função para lidar com os callbacks (botões clicados)
async def botao_clicado(update: Update, context: CallbackContext):
    global data
    query = update.callback_query
    '''await query.answer()  # Responde ao Telegram para remover "carregando..."'''
    if data:
        data = query
        data = False
        print(data)
    await query.answer()
    
    data_escolhida = query.data

    # Criação dos botões de horário após a escolha do dia
    keyboard = [
        [InlineKeyboardButton("08:00", callback_data="horario_08"),
        InlineKeyboardButton("09:00", callback_data="horario_09")],
        [InlineKeyboardButton("10:00", callback_data="horario_10"),
        InlineKeyboardButton("11:00", callback_data="horario_11")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=f"Data escolhida: {data_escolhida}. Escolha um horário para a consulta:", reply_markup=reply_markup)

async def horario_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    horario_escolhido = query.data

    await query.edit_message_text(text=f"Horário escolhido: {horario_escolhido}. Consulta marcada com sucesso!")
    resposta = f"Horário {query.data.replace('_', ' ')} agendado com sucesso!"
    await query.edit_message_text(text=resposta)

# Configuração e execução do bot
def main():
    token = "7043049373:AAErrO95Kh9oXSpNuKI92k2kUs1hqLtMnJk" 

    # Cria a aplicação
    application = Application.builder().token(token).build()

    # Registra os handlers
    application.add_handler(CommandHandler("marcar_consulta", marcar_consulta))
    application.add_handler(CallbackQueryHandler(button_callback, pattern="^data_"))
    application.add_handler(CallbackQueryHandler(horario_callback, pattern= "horario" )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("consulta", marcar_consulta))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("foto", imagem))
    application.add_handler(MessageHandler(filters.TEXT, echo))
    application.add_handler(CallbackQueryHandler(botao_clicado))  # Lida com botões

    print("Bot está rodando...")
    application.run_polling()

# Executa o bot
if __name__ == "__main__":
    main()