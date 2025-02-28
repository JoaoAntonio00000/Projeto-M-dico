import re
from datetime import datetime
from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, CallbackContext
import os
import json
from criando_lista_pacientes import lista_genero, lista_convenio

ARQUIVO_PACIENTES = "pacientes.json"

# Função para salvar os dados no JSON
def salvar_paciente(dados_paciente):
    if os.path.exists(ARQUIVO_PACIENTES):
        with open(ARQUIVO_PACIENTES, "r", encoding="utf-8") as arquivo:
            try:
                dados = json.load(arquivo)
            except json.JSONDecodeError:
                dados = {"pacientes": []}
    else:
        dados = {"pacientes": []}

    # Definir um novo ID_PACIENTE automaticamente
    novo_id = max([p["ID_PACIENTE"] for p in dados["pacientes"]], default=1) + 1
    dados_paciente["ID_PACIENTE"] = novo_id

    # Adicionar novo paciente à lista
    dados["pacientes"].append(dados_paciente)

    # Salvar no arquivo
    with open(ARQUIVO_PACIENTES, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

# Definição dos estados do cadastro
NOME, CPF, DATA_NASC, GENERO, TELEFONE, EMAIL, CEP, CONVENIO = range(8)

async def iniciar_cadastro(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Olá! Vamos começar seu cadastro. Digite seu nome:")
    return NOME  

async def receber_nome(update: Update, context: CallbackContext) -> int:
    context.user_data["nome"] = update.message.text
    await update.message.reply_text("Digite seu CPF (apenas números, 11 dígitos):")
    return CPF

async def receber_cpf(update: Update, context: CallbackContext) -> int:
    cpf = update.message.text
    if not cpf.isdigit() or len(cpf) != 11:
        await update.message.reply_text("❌ CPF inválido! Digite novamente (11 números, sem pontos ou traços).")
        return CPF
    
    context.user_data["cpf"] = cpf
    await update.message.reply_text("Digite sua data de nascimento (DD/MM/AAAA):")
    return DATA_NASC

async def receber_data_nasc(update: Update, context: CallbackContext) -> int:
    data_nasc = update.message.text
    try:
        data = datetime.strptime(data_nasc, "%d/%m/%Y")
        if data > datetime.now():
            raise ValueError  # Evita datas futuras
    except ValueError:
        await update.message.reply_text("❌ Data inválida! Digite no formato DD/MM/AAAA.")
        return DATA_NASC
    
    context.user_data["data_nasc"] = data_nasc
    
    for chave, genero in lista_genero.items():
        await update.message.reply_text(f"{chave} - {genero}")
    await update.message.reply_text("Digite seu gênero:")
    return GENERO

async def receber_genero(update: Update, context: CallbackContext) -> int:
    context.user_data["genero"] = update.message.text
    await update.message.reply_text("Digite seu telefone (somente números, 9 a 11 dígitos):")
    return TELEFONE

async def receber_telefone(update: Update, context: CallbackContext) -> int:
    telefone = update.message.text
    if not telefone.isdigit() or not (9 <= len(telefone) <= 11):
        await update.message.reply_text("❌ Telefone inválido! Digite novamente (9 a 11 números, sem traços ou espaços).")
        return TELEFONE

    context.user_data["telefone"] = telefone
    await update.message.reply_text("Digite seu e-mail:")
    return EMAIL

async def receber_email(update: Update, context: CallbackContext) -> int:
    email = update.message.text
    padrao_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if not re.match(padrao_email, email):
        await update.message.reply_text("❌ E-mail inválido! Digite novamente (exemplo: seuemail@email.com).")
        return EMAIL

    context.user_data["email"] = email
    await update.message.reply_text("Digite seu CEP (8 dígitos numéricos):")
    return CEP

async def receber_cep(update: Update, context: CallbackContext) -> int:
    cep = update.message.text
    if not cep.isdigit() or len(cep) != 8:
        await update.message.reply_text("❌ CEP inválido! Digite novamente (8 números, sem traços).")
        return CEP

    context.user_data["cep"] = cep
    for chave, genero in lista_convenio.items():
        await update.message.reply_text(f"{chave} - {genero}")
    await update.message.reply_text("Possui convênio?")
    return CONVENIO

async def receber_convenio(update: Update, context: CallbackContext) -> int:
    context.user_data["convenio"] = update.message.text
    await update.message.reply_text("✅ Cadastro finalizado! Agora você pode agendar uma consulta com /consulta")
    dados_paciente = {
        "nome": context.user_data["nome"],
        "cpf": context.user_data["cpf"],
        "data_nascimento": context.user_data["data_nasc"],
        "genero": context.user_data["genero"],
        "telefone": context.user_data["telefone"],
        "email": context.user_data["email"],
        "cep": context.user_data["cep"],
        "convenio": context.user_data["convenio"],
        "desconto": 50.0 
    }

    # Salvar no JSON
    salvar_paciente(dados_paciente)

    return ConversationHandler.END

async def cancelar(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Cadastro cancelado. Digite /start para reiniciar.")
    return ConversationHandler.END

# Configuração do ConversationHandler
cadastro_handler = ConversationHandler(
    entry_points=[CommandHandler("cadastro", iniciar_cadastro)],
    states={
        NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_nome)],
        CPF: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_cpf)],
        DATA_NASC: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_data_nasc)],
        GENERO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_genero)],
        TELEFONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_telefone)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_email)],
        CEP: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_cep)],
        CONVENIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_convenio)],
    },
    fallbacks=[CommandHandler("cancelar", cancelar)],
)
