import json
import os
from rich.console import Console
from datetime import datetime

console = Console()

caminho_arquivo = "PROJETO-M-DICO/lista_medicos.json"

def verificar_se_arquivo_existe():
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.readline()
            return conteudo
    except FileNotFoundError:
        with open(caminho_arquivo, 'w') as arquivo:
            return 'Arquivo Criado'

verificar_se_arquivo_existe()

def carregar_dados():
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            try:
                return json.load(arquivo)
            except json.JSONDecodeError:
                console.print("[bold red]Arquivo JSON corrompido. Retornando lista vazia.[/bold red]")
                return []
    except FileNotFoundError:
        console.print("[bold red]Arquivo não encontrado. Retornando lista vazia.[/bold red]")
        return []

def salvar_dados(dados):
    try:
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        console.print("[bold green]Dados salvos com sucesso![/bold green]")
    except IOError as e:
        console.print(f"[bold red]Erro ao salvar dados: {e}[/bold red]")

dados_email = carregar_dados()

if dados_email:
    medico_id = max(usuario["ID"] for usuario in dados_email) + 1
else:
    medico_id = 1

def validar_horario(horario):
    try:
        datetime.strptime(horario, "%H:%M")
        return True
    except ValueError:
        return False

def validar_email(email):
    import re
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def adicionar_medico():
    global medico_id
    dia_da_semana = ["Segunda".,"Terça","Quarta","Quinta","Sexta","Sabado","Domingo"]
    while True:
        nome = console.input("[bold yellow]Informe o nome do usuário: [/bold yellow]").strip()
        email = console.input("[bold yellow]Informe o email do usuário: [/bold yellow]").strip()
        crm = console.input("[bold yellow]Informe o crm do médico: ").strip()
        dia-da-semana = ("[bold yellow]Informe o dia da semana que o médico irá trabalhar: ").strip()
        if not validar_email(email):
            console.print("[bold red]E-mail inválido![/bold red]")
            continue

        mensagem = console.input("[bold yellow]Informe a mensagem para o usuário: [/bold yellow]").strip()
        tempo = console.input("[bold yellow]Informe a hora que você deseja enviar o email (HH:MM): [/bold yellow]").strip()
        if not validar_horario(tempo):
            console.print("[bold red]Horário inválido! Use o formato HH:MM.[/bold red]")
            continue

        novo_usuario = {
            "ID": medico_id,
            "Nome": nome,
            "E-mail": email,
            "Mensagem": mensagem,
            "Hora do Envio da Mensagem": tempo,
            "Enviado": False
        }
        dados_email.append(novo_usuario)
        medico_id += 1

        continuar = console.input("[bold yellow]Deseja continuar? (S/N): [/bold yellow]").strip().lower()
        if continuar == "n":
            salvar_dados(dados_email)
            break

def atualizar_contato():
    buscar = console.input("[bold yellow]Informe o ID do usuário que deseja atualizar: [/bold yellow]").strip()

    try:
        buscar = int(buscar)
    except ValueError:
        console.print("[bold red]Erro: O ID deve ser um número válido![/bold red]")
        return

    for usuario in dados_email:
        if usuario["ID"] == buscar:
            novo_nome = console.input("[bold yellow]Informe o novo nome: [/bold yellow]").strip()
            novo_email = console.input("[bold yellow]Informe o novo e-mail: [/bold yellow]").strip()
            nova_mensagem = console.input("[bold yellow]Informe a nova mensagem: [/bold yellow]").strip()
            novo_tempo = console.input("[bold yellow]Informe o novo horário para enviar o E-mail (HH:MM): [/bold yellow]").strip()

            if novo_tempo and novo_tempo != usuario['Hora do Envio da Mensagem']:
                usuario['Hora do Envio da Mensagem'] = novo_tempo
                hora_atual = datetime.now().strftime("%H:%M")
                if novo_tempo > hora_atual:
                    usuario["Enviado"] = False
                    console.print(f"[bold yellow]Horário alterado para {novo_tempo}. 'Enviado' redefinido como False.[/bold yellow]")

            usuario["Nome"] = novo_nome if novo_nome else usuario['Nome']
            usuario["E-mail"] = novo_email if novo_email else usuario['E-mail']
            usuario['Mensagem'] = nova_mensagem if nova_mensagem else usuario['Mensagem']
            salvar_dados(dados_email)
            console.print("[bold green]Contato atualizado com sucesso![/bold green]")
            return

    console.print("[bold red]ID não encontrado![/bold red]")

def excluir_contato():
    buscar = console.input("[bold yellow]Informe o ID do usuário que deseja excluir: [/bold yellow]").strip()

    try:
        buscar = int(buscar)
    except ValueError:
        console.print("[bold red]Erro: O ID deve ser um número válido![/bold red]")
        return

    for usuario in dados_email:
        if usuario["ID"] == buscar:
            console.print(f"[bold red]Tem certeza que deseja excluir o contato {usuario['Nome']}? (S/N)[/bold red]")
            confirmar = console.input().strip().lower()

            if confirmar == "s":
                dados_email.remove(usuario)
                salvar_dados(dados_email)
                console.print("[bold green]Contato excluído com sucesso![/bold green]")
            else:
                console.print("[bold yellow]Operação cancelada.[/bold yellow]")
            return

    console.print("[bold red]ID não encontrado![/bold red]")

def exibir_lista_contatos():
    from rich.table import Table
    if not dados_email:
        console.print("[bold red]Nenhum contato encontrado![/bold red]")
        return

    tabela = Table(title="Lista de Contatos", show_lines=True)
    tabela.add_column("ID", justify="center", style="bold cyan")
    tabela.add_column("Nome", justify="left", style="bold yellow")
    tabela.add_column("E-mail", justify="left", style="bold green")
    tabela.add_column("Mensagem", justify="left", style="bold green")
    tabela.add_column("Hora do Envio", justify="left", style="bold green")
    tabela.add_column("Enviado", justify="left", style="bold green")

    for usuario in dados_email:
        enviado = "Sim" if usuario["Enviado"] else "Não"
        tabela.add_row(
            str(usuario["ID"]),
            usuario["Nome"],
            usuario["E-mail"],
            usuario['Mensagem'],
            usuario['Hora do Envio da Mensagem'],
            enviado
        )

    console.print(tabela)