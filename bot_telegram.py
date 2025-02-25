
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext
from datetime import date as dt
from datetime import datetime, timedelta

# Variáveis globais
horario = False
data = False
dias_da_semana = ["segunda", "terça", "quarta", "quinta", "sexta"]
data_atual = 0
ultimo_dia_mes = 0
cadastro =''
entrar_genero = False
entrar_cep = False
entrar_convenio = False
entrar_cpf = False
entrar_data_nasc = False
entrar_dia = False
entrar_nome = False
entrar_telefone = False
escolha_convenio = False
entrar_email = False
entrar_cadastro = False
entrar_dia = False


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

async def dia(update: Update, context: CallbackContext) -> int:
    data_atual = dt.today()
    ultimo_dia_mes = (data_atual.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    dias_semana = ["segunda", "terca", "quarta", "quinta", "sexta"]
    lista_dias_disponiveis = [data_atual + timedelta(days=i) for i in range((ultimo_dia_mes - data_atual).days + 1) if (data_atual + timedelta(days=i)).weekday() < 5]

    buttons = [
        [InlineKeyboardButton(text=f'{dias_semana[data.weekday()]}-{data}', callback_data=str(data)) for data in lista_dias_disponiveis]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_text("Escolha um dia para a consulta:", reply_markup=reply_markup)
            
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
    global entrar_cep
    global entrar_convenio
    global entrar_cpf
    global entrar_data_nasc
    global entrar_dia
    global entrar_telefone
    global entrar_nome
    global entrar_genero
    global escolha_convenio
    global entrar_email
    global entrar_cadastro
    global entrar_dia
    
    user_message = update.message.text
    cadastro = user_message
    print(user_message)
    
    if (cadastro == 's' or cadastro == 'S') and entrar_cadastro:
        entrar_dia = True
        entrar_cadastro = False
    elif (cadastro =='n'or cadastro == 'N') and entrar_cadastro:
        await update.message.reply_text('Olá! Vamos começar seu cadastro. Por favor, digite seu nome:')
        entrar_nome = True
        entrar_cadastro = False
    elif entrar_nome:
        nome = user_message
        await update.message.reply_text('Digite seu CPF:')
        entrar_cpf = True
        entrar_nome = False
    elif entrar_cpf:
        cpf = user_message
        await update.message.reply_text('Digite sua data de nascimento (DD/MM/AAAA):')
        entrar_data_nasc = True
        entrar_cpf = False
    elif entrar_data_nasc:
        data_nasc = user_message
        await update.message.reply_text('Digite seu gênero:')
        entrar_genero = True
        entrar_data_nasc = False
    elif entrar_genero:
        genero = user_message
        await update.message.reply_text('Digite seu telefone:')
        entrar_telefone = True
        entrar_genero = False
    elif entrar_telefone:
        telefone = user_message
        await update.message.reply_text('Digite seu e-mail:')
        entrar_email = True
        entrar_telefone = False
    elif entrar_email:
        email = user_message
        await update.message.reply_text('Digite seu CEP:')
        entrar_cep = True
        entrar_email = False
    elif entrar_cep:
        cep = user_message
        await update.message.reply_text('Possui convênio (s/n)?')
        escolha_convenio = True
        entrar_cep = False
    elif escolha_convenio:
        escolha = user_message.lower()
        if escolha == 's' or escolha == 'S':
            await update.message.reply_text('Digite seu convênio:')
            entrar_convenio = True
            escolha_convenio = False
        else:
            await update.message.reply_text('Cadastro completo. Obrigado!')     
            escolha_convenio = False
            entrar_dia = True
    elif entrar_convenio:
        convenio = user_message
        entrar_convenio = False
        await update.message.reply_text('Cadastro completo. Obrigado!')
        entrar_dia = True
    elif entrar_dia:
        dias_uteis = dias_uteis_com_callback()
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
    else:
        await update.message.reply_text(f'"Olá! Como posso auxiliá-lo? \n\nPara agendar uma consulta, por favor, digite /consulta.\n Se necessitar de qualquer outra assistência, digite /help.\n\n Estamos à disposição para atendê-lo da melhor forma possível.')

# Função para exibir botões de horários de consulta
async def marcar_consulta(update: Update, context: CallbackContext) -> None:
    global entrar_cadastro
    await update.message.reply_text('Possui cadastro?(s/n): ')
    entrar_cadastro = True
    

'''
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
'''
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
    global data_atual
    global ultimo_dia_mes
    query = update.callback_query
    '''await query.answer()  # Responde ao Telegram para remover "carregando..."'''
    if data:
        dia = query
        if query == 0:
                data_atual = (data_atual.replace(day=28) + timedelta(days=4)).replace(day=1)
                ultimo_dia_mes = (data_atual.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
                
        else:
            data = False
            print(dia)
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
    application.add_handler(CallbackQueryHandler(dia, pattern="data"))
    application.add_handler(CallbackQueryHandler(horario_callback, pattern= "horario" ))
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