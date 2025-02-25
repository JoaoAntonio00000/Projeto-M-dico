import json
import os
from rich.console import Console

console = Console()

# Verificar se o arquivo da lista de médicos existe
caminho_arquivo = "resultado_pacientes.json"
caminho_medico = "lista_medicos.json"
caminho_pacientes = "pacientes.json"

def abrir_dados_medicos():
    try: 
        with open(caminho_medico, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        console.print("[bold red]Arquivo de médicos não encontrado ou corrompido. Retornando lista vazia.[/bold red]")
        return []

def abrir_dados_pacientes():
    try: 
        with open(caminho_pacientes, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            return dados["pacientes"]
    except (FileNotFoundError, json.JSONDecodeError):
        console.print("[bold red]Arquivo de pacientes não encontrado ou corrompido. Retornando lista vazia.[/bold red]")
        return []

def verificar_se_arquivo_existe():
    if not os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump([], arquivo, indent=4, ensure_ascii=False)
        console.print("[bold green]Arquivo criado com sucesso![/bold green]")


verificar_se_arquivo_existe()

# Carregar os dados da lista de resultados
def carregar_dados():
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        console.print("[bold red]Arquivo não encontrado ou corrompido. Retornando lista vazia.[/bold red]")
        return []

# Salvar os dados e alterações feitas na lista
def salvar_dados(dados):
    try:
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        console.print("[bold green]Dados salvos com sucesso![/bold green]")
    except IOError as e:
        console.print(f"[bold red]Erro ao salvar dados: {e}[/bold red]")

dados_resultados = carregar_dados()
dados_medicos = abrir_dados_medicos()
dados_pacientes = abrir_dados_pacientes()

# Dando ID para os resultados
if dados_resultados:
    resultados_id = max(usuario["ID"] for usuario in dados_resultados) + 1
else:
    resultados_id = 1

def buscar_paciente(id_paciente):
    for paciente in dados_pacientes:
        if paciente["ID_PACIENTE"] == id_paciente:
            return paciente
    return None

def buscar_medico(id_medico):
    for medico in dados_medicos:
        if medico['ID'] == id_medico:
            return medico
    return None

def criar_documento_exame(id_paciente, nome_paciente, nome_medico, nome_exame, resultado_exame):
    # Criar o nome do arquivo
    nome_arquivo = f"{id_paciente}_{nome_paciente}_resultado_exame.txt"
    
    # Conteúdo do arquivo
    conteudo = f"""
    ID do Paciente: {id_paciente}
    Nome do Paciente: {nome_paciente}
    Nome do Médico: {nome_medico}
    Nome do Exame: {nome_exame}
    Resultado do Exame: {resultado_exame}
    """
    
    # Salvar o arquivo
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(conteudo)
    
    console.print(f"[bold green]Documento do exame criado com sucesso: {nome_arquivo}[/bold green]")

def adicionar_exames_resultados():
    id_paciente = int(input("Digite o ID do paciente: "))
    paciente = buscar_paciente(id_paciente)
    
    if paciente:
        console.print(f"[bold green]Paciente encontrado: {paciente['nome']}[/bold green]")
        id_medico = int(input("Digite o ID do médico: "))
        medico = buscar_medico(id_medico)
        
        if medico:
            console.print(f"[bold green]Médico encontrado: {medico['Nome']}[/bold green]")
            
            while True:
                nome_exame = input("Digite o nome do exame: ")
                resultado_exame = input("Digite o resultado do exame: ")
                
                novo_resultado = {
                    "ID": resultados_id,
                    "ID_PACIENTE": id_paciente,
                    "Nome_Paciente": paciente["nome"],
                    "Email_Paciente": paciente["email"],
                    "Telefone_Paciente": paciente["telefone"],
                    "Nome_Medico": medico["Nome"],
                    "Exame": nome_exame,
                    "Resultado": resultado_exame
                }
                
                dados_resultados.append(novo_resultado)
                salvar_dados(dados_resultados)
                console.print("[bold green]Exame e resultado adicionados com sucesso![/bold green]")
                
                # Criar o documento do exame
                criar_documento_exame(id_paciente, paciente["nome"], medico["Nome"], nome_exame, resultado_exame)
                
                # Perguntar se deseja adicionar outro exame
                continuar = input("Deseja adicionar outro exame? (s/n): ").strip().lower()
                if continuar != 's':
                    break
        else:
            console.print("[bold red]Médico não encontrado.[/bold red]")
    else:
        console.print("[bold red]Paciente não encontrado.[/bold red]")

def atualizar_resultado_exame():
    if not dados_resultados:
        console.print("[bold red]Nenhum resultado de exame cadastrado.[/bold red]")
        return

    console.print("[bold cyan]Lista de Resultados de Exames:[/bold cyan]")
    for resultado in dados_resultados:
        console.print(f"ID: {resultado['ID']} | Paciente: {resultado['Nome_Paciente']} | Exame: {resultado['Exame']} | Resultado: {resultado['Resultado']}")

    id_exame = input("Digite o ID do exame que deseja atualizar: ").strip()
    
    try:
        id_exame = int(id_exame)
    except ValueError:
        console.print("[bold red]ID inválido. Digite um número válido.[/bold red]")
        return

    exame_encontrado = None
    for resultado in dados_resultados:
        if resultado["ID"] == id_exame:
            exame_encontrado = resultado
            break

    if not exame_encontrado:
        console.print("[bold red]Exame não encontrado.[/bold red]")
        return

    console.print(f"[bold green]Exame encontrado: {exame_encontrado['Exame']} | Resultado atual: {exame_encontrado['Resultado']}[/bold green]")

    # Solicitar o novo resultado
    novo_resultado = input("Digite o novo resultado do exame (ou pressione Enter para manter o atual): ").strip()

    # Atualizar apenas se o usuário fornecer um novo resultado
    if novo_resultado:
        exame_encontrado["Resultado"] = novo_resultado
        console.print("[bold green]Resultado atualizado com sucesso![/bold green]")
    else:
        console.print("[bold yellow]Nenhum novo resultado fornecido. Mantendo o resultado original.[/bold yellow]")

    # Salvar os dados atualizados
    salvar_dados(dados_resultados)

    # Atualizar o documento do exame
    criar_documento_exame(
        exame_encontrado["ID_PACIENTE"],
        exame_encontrado["Nome_Paciente"],
        exame_encontrado["Nome_Medico"],
        exame_encontrado["Exame"],
        exame_encontrado["Resultado"]
    )

def exibir_lista_resultados():
    if not dados_resultados:
        console.print("[bold red]Nenhum resultado de exame cadastrado.[/bold red]")
        return

    console.print("[bold cyan]Lista de Resultados de Exames:[/bold cyan]")
    for resultado in dados_resultados:
        console.print(f"ID: {resultado['ID']} | Paciente: {resultado['Nome_Paciente']} | Exame: {resultado['Exame']} | Resultado: {resultado['Resultado']}")

def exibir_resultado_paciente():
    if not dados_resultados:
        console.print("[bold red]Nenhum resultado de exame cadastrado.[/bold red]")
        return

    # Solicitar o ID do paciente
    id_paciente = input("Digite o ID do paciente para exibir os resultados: ").strip()
    
    try:
        id_paciente = int(id_paciente)
    except ValueError:
        console.print("[bold red]ID inválido. Digite um número válido.[/bold red]")
        return

    # Buscar o paciente pelo ID
    paciente = buscar_paciente(id_paciente)
    if not paciente:
        console.print("[bold red]Paciente não encontrado.[/bold red]")
        return

    console.print(f"[bold green]Paciente encontrado: {paciente['nome']}[/bold green]")

    # Filtrar os resultados do paciente
    resultados_paciente = [resultado for resultado in dados_resultados if resultado["ID_PACIENTE"] == id_paciente]

    if not resultados_paciente:
        console.print("[bold red]Nenhum resultado de exame encontrado para este paciente.[/bold red]")
        return

    # Exibir os resultados do paciente
    console.print(f"[bold cyan]Resultados de Exames para o Paciente {paciente['nome']}:[/bold cyan]")
    for resultado in resultados_paciente:
        console.print(f"ID do Exame: {resultado['ID']}")
        console.print(f"Exame: {resultado['Exame']}")
        console.print(f"Resultado: {resultado['Resultado']}")
        console.print(f"Médico Responsável: {resultado['Nome_Medico']}")
        console.print("-" * 40)  # Linha separadora

def menu():
    while True:
        opcao = console.input("[bold magenta][1]-Adicionar Exame e Resultado"
                              '\n[2] - Atualizar Resultado do Exame'
                              '\n[3] - Ver Lista de Resultados'
                              '\n[4] - Exibir Resultados de um Paciente'
                              '\n[0] - Sair\n'
                              "[bold cyan]Escolha uma opção: [/bold cyan]")
        if opcao == '1':
            adicionar_exames_resultados()
        elif opcao == '2':
            atualizar_resultado_exame()
        elif opcao == '3':
            exibir_lista_resultados()
        elif opcao == '4':
            exibir_resultado_paciente()
        elif opcao == '0':
            console.print("[bold cyan]Até mais![/bold cyan]")
            break
        else:
            console.print("[bold red]Valor inválido![/bold red]")
