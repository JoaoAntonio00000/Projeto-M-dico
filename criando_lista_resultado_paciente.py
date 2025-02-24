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
    else:
        console.print("[bold green]Arquivo já existe.[/bold green]")

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

# Exemplo de uso
adicionar_exames_resultados()