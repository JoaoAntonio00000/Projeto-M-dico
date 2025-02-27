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
        "/help - Exibir esta lista de comandos\n"
        "/confirmar - Confirmar uma consulta\n"
    )
    await update.message.reply_text(comandos)

CONFIRMAR_ID = 1

async def iniciar_confirmacao(update: Update, context: CallbackContext) -> int:
    """Inicia o processo de confirmação e pede o código da consulta"""
    await update.message.reply_text("🆔 Por favor, envie o código da consulta que deseja confirmar.")
    return CONFIRMAR_ID  # Muda para o estado de espera do código

async def confirmar_consulta(update: Update, context: CallbackContext) -> int:
    """Recebe o código da consulta, verifica e confirma na agenda"""
    codigo = update.message.text.strip()  # Remove espaços extras

    try:
        with open("agenda.json", "r") as arquivo:
            agenda = json.load(arquivo)

        consulta_encontrada = None

        # Percorre todos os dias da agenda para buscar a consulta com o código informado
        for dia, consultas in agenda.items():
            for consulta in consultas:
                if consulta["codigo_consulta"] == codigo:  # Comparação direta
                    consulta_encontrada = consulta
                    break
            if consulta_encontrada:
                break  # Sai do loop se já encontrou a consulta

        if not consulta_encontrada:
            await update.message.reply_text("⚠️ Código de consulta não encontrado! Verifique e tente novamente.")
            return CONFIRMAR_ID  # Mantém a conversa ativa para nova tentativa

        # Atualiza a confirmação da consulta
        consulta_encontrada["confirmacao_paciente"] = "confirmado"

        # Salva de volta no JSON
        with open("agenda.json", "w") as arquivo:
            json.dump(agenda, arquivo, indent=4, ensure_ascii=False)

        await update.message.reply_photo('Confirmação-de-consulta.png')

    except FileNotFoundError:
        await update.message.reply_text("⚠️ O arquivo de agenda não foi encontrado.")
    except json.JSONDecodeError:
        await update.message.reply_text("⚠️ Erro ao ler os dados da agenda.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ocorreu um erro inesperado: {e}")

    return ConversationHandler.END  # Finaliza a conversa após a confirmação

async def cancelar_confirmacao(update: Update, context: CallbackContext) -> int:
    """Cancela o processo de confirmação"""
    await update.message.reply_text("🚫 Confirmação cancelada.")
    return ConversationHandler.END

def registrar_handlers():
    """Cria e retorna o handler de confirmação"""
    return ConversationHandler(
        entry_points=[CommandHandler("confirmar", iniciar_confirmacao)],
        states={
            CONFIRMAR_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmar_consulta)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar_confirmacao)],
    )

async def resposta_padrao(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Olá, como posso ajudá-lo?\nPara agendar uma consulta, digite /consulta.\n"
        "Caso necessite de outra assistência, digite /help."
    )

def main():
    token = "8192805655:AAFee0YvKt3mBezS2wb-hMWO8WV_w98ib5I"
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", listar_comandos))

    # Adiciona os handlers de cadastro, agendamento e confirmação
    application.add_handler(cadastro_handler)
    application.add_handler(agendamento_handler)
    
    conv_handler = registrar_handlers()  # Chama a função para obter o handler
    application.add_handler(conv_handler)  # Adiciona o handler de confirmação

    # Captura qualquer outra mensagem e responde com a mensagem padrão
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, resposta_padrao))

    print('Bot rodando...')
    application.run_polling()

if __name__ == "__main__":
    main()
