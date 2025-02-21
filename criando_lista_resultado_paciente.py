import json
import os
from rich.console import Console

console = Console()

# Verificar se o arquivo da lista de médicos existe
caminho_arquivo = "resultado_pacientes.json"

def verificar_se_arquivo_existe():
    if not os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump([], arquivo, indent=4, ensure_ascii=False)
        console.print("[bold green]Arquivo criado com sucesso![/bold green]")
    else:
        console.print("[bold green]Arquivo já existe.[/bold green]")

verificar_se_arquivo_existe()

# Carregar os dados da lista de médicos
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

# Dando ID para os médicos
if dados_resultados:
    resultados_id = max(usuario["ID"] for usuario in dados_resultados) + 1
else:
    resultados_id = 1

def buscar_paciente(id_paciente):
    for paciente in dados_resultados:
        if paciente["ID"] == id_paciente:
            return paciente
    return None

def adicionar_exame_resultado():
    id_paciente = int(input("Digite o ID do paciente: "))
    paciente = buscar_paciente(id_paciente)
    
    if paciente:
        console.print(f"[bold green]Paciente encontrado: {paciente['Nome']}[/bold green]")
        nome_exame = input("Digite o nome do exame: ")
        resultado_exame = input("Digite o resultado do exame: ")
        
        if "resultados" not in paciente:
            paciente["resultados"] = []
        
        paciente["resultados"].append({
            "exame": nome_exame,
            "resultado": resultado_exame
        })
        
        salvar_dados(dados_resultados)
        console.print("[bold green]Exame e resultado adicionados com sucesso![/bold green]")
    else:
        console.print("[bold red]Paciente não encontrado.[/bold red]")

# Exemplo de uso
adicionar_exame_resultado()