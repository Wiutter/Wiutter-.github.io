import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import openpyxl
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import os

# Lista para armazenar máquinas
maquinas = []

# Constantes para a API do Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'credentials.json'  # Arquivo com suas credenciais (baixe do Google Cloud Console)
TOKEN_FILE = 'token.json' #arquivo para salvar o token

def adicionar_maquina():
    """
    Adiciona uma nova máquina à lista de máquinas com detalhes adicionais.
    Obtém o nome, status, sistema operacional, memória RAM, Office, usuário,
    departamento e setor da máquina das entradas do usuário, verifica se todos os
    campos estão preenchidos, adiciona a máquina à lista, exibe uma mensagem de
    sucesso e limpa os campos de entrada. Se algum campo estiver vazio, exibe
    uma mensagem de aviso.
    """
    nome = entry_nome.get()
    status = entry_status.get()
    sistema_operacional = entry_so.get()
    memoria_ram = entry_ram.get()
    office = entry_office.get()
    usuario = entry_usuario.get()
    departamento = entry_departamento.get()
    setor = entry_setor.get()

    if nome and status and sistema_operacional and memoria_ram and office and usuario and departamento and setor:
        maquinas.append({
            'nome': nome,
            'status': status,
            'sistema_operacional': sistema_operacional,
            'memoria_ram': memoria_ram,
            'office': office,
            'usuario': usuario,
            'departamento': departamento,
            'setor': setor
        })
        messagebox.showinfo("Sucesso", f"Máquina '{nome}' adicionada!")
        entry_nome.delete(0, tk.END)
        entry_status.delete(0, tk.END)
        entry_so.delete(0, tk.END)
        entry_ram.delete(0, tk.END)
        entry_office.delete(0, tk.END)
        entry_usuario.delete(0, tk.END)
        entry_departamento.delete(0, tk.END)
        entry_setor.delete(0, tk.END)
    else:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

def mostrar_dashboard():
    """
    Mostra um gráfico de barras com o status das máquinas cadastradas.
    Verifica se há máquinas cadastradas. Se não houver, exibe uma mensagem de aviso.
    Se houver máquinas, conta a frequência de cada status,
    cria um gráfico de barras com os status e suas frequências,
    define o título e os rótulos dos eixos e exibe o gráfico.
    """
    if not maquinas:
        messagebox.showwarning("Atenção", "Nenhuma máquina cadastrada.")
        return

    status_count = {}
    for maquina in maquinas:
        status = maquina['status']
        if status in status_count:
            status_count[status] += 1
        else:
            status_count[status] = 1

    # Criar gráfico
    plt.bar(status_count.keys(), status_count.values())
    plt.title('Status das Máquinas')
    plt.xlabel('Status')
    plt.ylabel('Quantidade')
    plt.show()

def exportar_para_excel():
    """
    Exporta os dados das máquinas cadastradas para um arquivo Excel e, opcionalmente,
    salva o arquivo no Google Drive do usuário.
    Verifica se há máquinas cadastradas. Se não houver, exibe uma mensagem de aviso.
    Se houver máquinas, cria um novo arquivo Excel, adiciona um cabeçalho com os
    nomes dos campos e adiciona os dados de cada máquina em uma nova linha.
    Salva o arquivo localmente com o nome "dados_maquinas.xlsx" e, se o usuário
    escolher, envia o arquivo para o Google Drive.
    """
    if not maquinas:
        messagebox.showwarning("Atenção", "Nenhuma máquina cadastrada para exportar.")
        return

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Dados das Máquinas"

    # Cabeçalho com todos os campos, incluindo os novos
    cabecalho = ['Nome', 'Status', 'Sistema Operacional', 'Memória RAM', 'Office', 'Usuário', 'Departamento', 'Setor']
    sheet.append(cabecalho)

    # Adiciona os dados de cada máquina
    for maquina in maquinas:
        linha = [
            maquina['nome'],
            maquina['status'],
            maquina['sistema_operacional'],
            maquina['memoria_ram'],
            maquina['office'],
            maquina['usuario'],
            maquina['departamento'],
            maquina['setor']
        ]
        sheet.append(linha)

    nome_arquivo_local = "dados_maquinas.xlsx"
    workbook.save(nome_arquivo_local)
    messagebox.showinfo("Sucesso", f"Dados exportados para '{nome_arquivo_local}'!")

    if messagebox.askyesno("Google Drive", "Deseja salvar uma cópia no Google Drive?"):
        try:
            # Autenticação e conexão com a API do Google Drive
            creds = None
            if os.path.exists(TOKEN_FILE):
                creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            # Se não houver credenciais válidas, faça o login.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        CREDENTIALS_FILE, SCOPES)
                    creds = flow.run_local_server(port=0)
                # Salve as credenciais para a próxima execução
                with open(TOKEN_FILE, 'w') as token:
                    token.write(creds.to_json())

            service = build('drive', 'v3', credentials=creds)

            # Enviar o arquivo para o Google Drive
            file_metadata = {'name': nome_arquivo_local}
            media = MediaFileUpload(nome_arquivo_local, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            file = service.files().create(body=file_metadata, media=media, fields='id').execute()
            print(f"Arquivo enviado para o Google Drive com ID: {file.get('id')}")
            messagebox.showinfo("Google Drive", "Arquivo salvo no Google Drive com sucesso!")

        except HttpError as error:
            # TODO(developer): Handle errors from Drive API.
            print(f"Ocorreu um erro: {error}")
            messagebox.showerror("Erro", f"Erro ao salvar no Google Drive: {error}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            messagebox.showerror("Erro", f"Erro inesperado: {e}")

# Configuração da interface
root = tk.Tk()
root.title("Gerenciamento de Máquinas e Inventário")
root.configure(bg='#f0f0f0')

# Estilo para os widgets
style = ttk.Style()

# Cores mais modernas e agradáveis
cor_principal = '#6a1b9a'
cor_principal_clara = '#9c27b0'
cor_secundaria = '#f50057'
cor_texto = '#fff'
cor_de_fundo = '#f3e5f5'
cor_borda = '#d81b60'

style.configure('TLabel', font=('Arial', 12), foreground=cor_principal)
style.configure('TButton', font=('Arial', 12),
                    background=cor_principal,
                    foreground=cor_texto,
                    relief='flat',
                    borderwidth=0,
                    padding=8)
style.map('TButton',
          background=[('active', cor_principal_clara),
                      ('disabled', '#b8b8b8')],
          foreground=[('disabled', '#777')])
style.configure('TEntry', font=('Arial', 12),
                    relief='inset',
                    borderwidth=1,
                    padding=6,
                    background=cor_de_fundo,
                    fieldbackground=cor_de_fundo,
                    foreground='#000')

# Campos de entrada com labels estilizados e espaçamento
ttk.Label(root, text="Nome da Máquina:", style='TLabel').pack(pady=(10, 2))
entry_nome = ttk.Entry(root, style='TEntry')
entry_nome.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Status da Máquina:", style='TLabel').pack(pady=(10, 2))
entry_status = ttk.Entry(root, style='TEntry')
entry_status.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Sistema Operacional:", style='TLabel').pack(pady=(10, 2))
entry_so = ttk.Entry(root, style='TEntry')
entry_so.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Memória RAM:", style='TLabel').pack(pady=(10, 2))
entry_ram = ttk.Entry(root, style='TEntry')
entry_ram.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Office:", style='TLabel').pack(pady=(10, 2))
entry_office = ttk.Entry(root, style='TEntry')
entry_office.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Usuário:", style='TLabel').pack(pady=(10, 2))
entry_usuario = ttk.Entry(root, style='TEntry')
entry_usuario.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Departamento:", style='TLabel').pack(pady=(10, 2))
entry_departamento = ttk.Entry(root, style='TEntry')
entry_departamento.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Setor:", style='TLabel').pack(pady=(10, 2))
entry_setor = ttk.Entry(root, style='TEntry')
entry_setor.pack(pady=5, padx=20, fill='x')

# Botões estilizados com espaçamento e preenchimento
botao_adicionar = ttk.Button(root, text="Adicionar Máquina", command=adicionar_maquina, style='TButton')
botao_adicionar.pack(pady=10, padx=20, fill='x')
botao_dashboard = ttk.Button(root, text="Mostrar Dashboard", command=mostrar_dashboard, style='TButton')
botao_dashboard.pack(pady=10, padx=20, fill='x')
botao_exportar = ttk.Button(root, text="Exportar para Excel", command=exportar_para_excel, style='TButton')
botao_exportar.pack(pady=10, padx=20, fill='x')

# Iniciar a interface
root.mainloop()
