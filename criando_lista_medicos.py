import json
import os
from rich.console import Console
from validacao_de_dados import validar_email, validar_crm, validar_cpf

console = Console()

caminho_arquivo = "lista_medicos.json"

# Verificar se o arquivo da lista de médicos existe
def verificar_se_arquivo_existe():
    if not os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump([], arquivo, indent=4, ensure_ascii=False)
        console.print("[bold green]Arquivo criado com sucesso![/bold green]")

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

dados_medico = carregar_dados()

# Dando ID para os médicos
if dados_medico:
    medico_id = max(usuario["ID"] for usuario in dados_medico) + 1
else:
    medico_id = 1

# Adicionar médico à lista
def adicionar_medico():
    global medico_id
    while True:
        nome = console.input("[bold yellow]Informe o nome do Médico: [/bold yellow]").strip()
        
        while True:
            cpf = console.input("[bold yellow]Informe o CPF do Médico: ").strip()
            if not validar_cpf(cpf):
                # Verificar se o CPF já existe
                if any(medico["CPF"] == cpf for medico in dados_medico):
                    console.print("[bold red]CPF já cadastrado![/bold red]")
                else:
                    break
            else:
                console.print("[bold red]CPF inválido! Digite novamente.[/bold red]")

        while True:
            email = console.input("[bold yellow]Informe o email do Médico: [/bold yellow]").strip()
            if not validar_email(email):
                break
            else:
                console.print("[bold red]E-mail inválido! Digite novamente.[/bold red]")
        
        while True:
            crm = console.input("[bold yellow]Informe o CRM do médico: (****/Sigla do Estado)[/bold yellow]").strip()
            if not validar_crm(crm):
                # Verificar se o CRM já existe
                if any(medico["CRM"] == crm for medico in dados_medico):
                    console.print("[bold red]CRM já cadastrado![/bold red]")
                else:
                    break
            else:
                console.print("[bold red]CRM inválido! Por favor, tente novamente.[/bold red]")
        
        tipo_de_convenio = console.input("[bold yellow]O médico atende convênio? (s/n): [/bold yellow]").strip().upper()
        if tipo_de_convenio == "S":
            convenio = console.input("[bold blue]Informe quais convênios o médico atende (separados por vírgula): [/bold blue]").strip().split(",")
        else:
            convenio = ['Nenhum']
        
        while True:
            genero = console.input("[bold yellow]Informe o gênero do médico (M/F): [/bold yellow]").strip().upper()
            if genero in ["M", "F"]:
                break
            else:
                console.print("[bold red]Gênero inválido! Use 'M' para masculino ou 'F' para feminino.[/bold red]")
        
        especializacao = console.input("[bold yellow]Informe a especialização do médico: [/bold yellow]").strip()

        novo_usuario = {
            "ID": medico_id,
            "Nome": nome,
            "E-mail": email,
            "CPF": cpf,
            "CRM": crm,
            "Genero": genero,
            "Especializacao": especializacao,
            "Convenio": convenio,
            "Hora do Medico": {
                'Segunda': {"8": True, "9": True, "10": True, "11": True, "13": True, "14": True, "15": True, "16": True, "17": True},
                "Terça": {"8": True, "9": True, "10": True, "11": True, "13": True, "14": True, "15": True, "16": True, "17": True},
                "Quarta": {"8": True, "9": True, "10": True, "11": True, "13": True, "14": True, "15": True, "16": True, "17": True},
                "Quinta": {"8": True, "9": True, "10": True, "11": True, "13": True, "14": True, "15": True, "16": True, "17": True},
                "Sexta": {"8": True, "9": True, "10": True, "11": True, "13": True, "14": True, "15": True, "16": True, "17": True},
            }
        }
        dados_medico.append(novo_usuario)
        medico_id += 1

        continuar = console.input("[bold yellow]Deseja continuar? (S/N): [/bold yellow]").strip().lower()
        if continuar == "n":
            salvar_dados(dados_medico)
            break

def atualizar_contato():
    buscar = console.input("[bold yellow]Informe o ID do Médico que deseja atualizar: [/bold yellow]").strip()

    try:
        buscar = int(buscar)
    except ValueError:
        console.print("[bold red]Erro: O ID deve ser um número válido![/bold red]")
        return

    for usuario in dados_medico:
        if usuario["ID"] == buscar:
            novo_nome = console.input("[bold yellow]Informe o novo nome do médico: [/bold yellow]").strip()
            
            while True:
                novo_email = console.input("[bold yellow]Informe o novo e-mail do médico: [/bold yellow]").strip()
                if not novo_email:  # Se o campo estiver vazio, mantém o atual
                    novo_email = usuario['E-mail']
                    break
                elif validar_email(novo_email):
                    break
                else:
                    console.print("[bold red]E-mail inválido! Digite novamente.[/bold red]")
            
            novo_convenio = console.input("[bold yellow]Informe o novo tipo de convenio do médico: [/bold yellow]").strip().split(",")

            usuario["Nome"] = novo_nome if novo_nome else usuario['Nome']
            usuario["E-mail"] = novo_email if novo_email else usuario['E-mail']
            usuario['Convenio'] = novo_convenio if novo_convenio else usuario['Convenio']
            salvar_dados(dados_medico)
            console.print("[bold green]Contato atualizado com sucesso![/bold green]")
            return

    console.print("[bold red]ID não encontrado![/bold red]")

def verificar_e_cancelar_consultas_medico(medico_id):

    try:
        with open("agenda.json", "r") as arquivo:
            agenda = json.load(arquivo)
        
        consultas_canceladas = False

        # Percorre todos os dias da semana na agenda
        for dia_semana in agenda:
            # Filtra as consultas que são do médico e estão pendentes ou confirmadas
            for consulta in agenda[dia_semana]:
                if consulta["id_medico"] == medico_id and consulta["confirmacao_paciente"] in ["pendente", "confirmado"]:
                    consulta["confirmacao_paciente"] = "cancelado"
                    consultas_canceladas = True
        
        # Se houver consultas canceladas, salva a agenda atualizada
        if consultas_canceladas:
            with open("agenda.json", "w") as arquivo:
                json.dump(agenda, arquivo, indent=4, ensure_ascii=False)
            console.print(f"[bold yellow]Consultas do médico ID {medico_id} canceladas com sucesso![/bold yellow]")
            return True
        else:
            console.print(f"[bold green]Nenhuma consulta pendente encontrada para o médico ID {medico_id}.[/bold green]")
            return False

    except FileNotFoundError:
        console.print("[bold red]Arquivo de agenda não encontrado.[/bold red]")
        return False
    except json.JSONDecodeError:
        console.print("[bold red]Erro ao ler o arquivo JSON. Verifique a formatação.[/bold red]")
        return False
    except Exception as e:
        console.print(f"[bold red]Ocorreu um erro inesperado: {e}[/bold red]")
        return False
    
def excluir_medico():
    buscar = console.input("[bold yellow]Informe o ID do Médico que deseja excluir: [/bold yellow]").strip()

    try:
        buscar = int(buscar)
    except ValueError:
        console.print("[bold red]Erro: O ID deve ser um número válido![/bold red]")
        return

    for usuario in dados_medico:
        if usuario["ID"] == buscar:
            console.print(f"[bold red]Tem certeza que deseja excluir o Médico {usuario['Nome']}? (S/N)[/bold red]")
            confirmar = console.input().strip().lower()

            if confirmar == "s":
                # Verifica e cancela as consultas do médico
                if verificar_e_cancelar_consultas_medico(buscar):
                    console.print(f"[bold yellow]Consultas do médico {usuario['Nome']} canceladas.[/bold yellow]")
                
                # Remove o médico da lista de médicos
                dados_medico.remove(usuario)
                salvar_dados(dados_medico)
                console.print("[bold green]Médico excluído com sucesso![/bold green]")
            else:
                console.print("[bold yellow]Operação cancelada.[/bold yellow]")
            return

    console.print("[bold red]ID não encontrado![/bold red]")


def exibir_lista_medico():
    from rich.table import Table
    if not dados_medico:
        console.print("[bold red]Nenhum Médico encontrado![/bold red]")
        return

    tabela = Table(title="Lista de Médicos", show_lines=True)
    tabela.add_column("ID", justify="center", style="bold cyan")
    tabela.add_column("Nome", justify="left", style="bold yellow")
    tabela.add_column("E-mail", justify="left", style="bold green")
    tabela.add_column("Convenio", justify="left", style="bold green")
    tabela.add_column("Genero", justify="left", style="bold green")
    tabela.add_column("Especialização", justify="left", style="bold green")
    tabela.add_column("CRM", justify="left", style="bold blue")
    tabela.add_column("CPF", justify='left', style='bold magenta')
    for usuario in dados_medico:
        tabela.add_row(
            str(usuario["ID"]),
            usuario["Nome"],
            usuario["E-mail"],
            ", ".join(usuario['Convenio']),
            usuario['Genero'],
            usuario['Especializacao'],
            usuario['CRM'],
            usuario['CPF']
        )

    console.print(tabela)

def menu():
    while True:
        opcao = console.input("[bold magenta][1]-Adicionar médico"
                              '\n[2] - Ver lista de médicos'
                              '\n[3] - Excluir médico'
                              '\n[4] - Atualizar médico'
                              '\n[0] - Sair\n'
                              "[bold cyan]Escolha uma opção: [/bold cyan]")
        if opcao == '1':
            adicionar_medico()
        elif opcao == '2':
            exibir_lista_medico()
        elif opcao == '3':
            exibir_lista_medico()
            excluir_medico()
        elif opcao == '4':
            atualizar_contato()
        elif opcao == '0':
            console.print("[bold cyan]Até mais![/bold cyan]")
            break
        else:
            console.print("[bold red]Valor inválido![/bold red]")

if __name__ == "__main__":
    menu()