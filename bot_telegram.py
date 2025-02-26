from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
import json

from cadastro_bot_telegram import cadastro_handler
from agendamento_bot_telegram import agendamento_handler


with open('pacientes.json', 'r') as arquivo:
    file = json.load(arquivo)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Bem-vindo à Clínica CyberMedical!\n\n"
        "Para agendar uma consulta, digite /consulta.\n"
        "Caso necessite de outra assistência, digite /help.\n\n"
        "Estamos à disposição para atendê-lo da melhor forma possível!"
    )

async def listar_comandos(update: Update, context: CallbackContext) -> None:
    comandos = (
        "Comandos disponíveis:\n"
        "/start - Iniciar o bot\n"
        "/consulta - Agendar uma consulta\n"
        "/cadastro - Cadastrar-se na clínica\n"
        "/help - Exibir esta lista de comandos"
    )
    await update.message.reply_text(comandos)

async def resposta_padrao(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Olá, como posso ajudá-lo? Para agendar uma consulta, digite /consulta. Caso necessite de outra assistência, digite /help.")

def main():
    token = "7043049373:AAErrO95Kh9oXSpNuKI92k2kUs1hqLtMnJk" 
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", listar_comandos))
    
    # Adiciona os handlers de cadastro e agendamento
    application.add_handler(cadastro_handler)
    application.add_handler(agendamento_handler)
    
    # Captura qualquer outra mensagem e responde com a mensagem padrão
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, resposta_padrao))

    print('Bot rodando...')
    application.run_polling()

if __name__ == "__main__":
    main()
