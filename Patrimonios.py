import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Importa o módulo ttk para widgets estilizados
import matplotlib.pyplot as plt
import openpyxl  # Importa a biblioteca openpyxl para trabalhar com arquivos Excel

# Lista para armazenar máquinas
maquinas = []

def adicionar_maquina():
    """
    Adiciona uma nova máquina à lista de máquinas com todos os detalhes fornecidos.
    Obtém os dados das entradas do usuário, verifica se todos os campos estão preenchidos,
    adiciona a máquina à lista e limpa os campos de entrada.
    """
    num_status_registro = entry_num_status_registro.get()
    win_registro = entry_win_registro.get()
    office_patrimonio = entry_office_patrimonio.get()
    nota_fiscal = entry_nota_fiscal.get()
    setor = entry_setor.get()
    usuario = entry_usuario.get()
    host_name = entry_host_name.get()
    tipo = entry_tipo.get()
    modelo = entry_modelo.get()
    fabricante = entry_fabricante.get()
    service_tag = entry_service_tag.get()
    cadastrado_dell = entry_cadastrado_dell.get()
    conexao = entry_conexao.get()
    sistema_operacional = entry_sistema_operacional.get()
    memoria_ram = entry_memoria_ram.get()
    tipo_memoria = entry_tipo_memoria.get()
    frequencia = entry_frequencia.get()
    processador = entry_processador.get()
    tipo_hd1 = entry_tipo_hd1.get()
    ativo = entry_ativo.get()

    if (num_status_registro and win_registro and office_patrimonio and nota_fiscal and
            setor and usuario and host_name and tipo and modelo and fabricante and
            service_tag and cadastrado_dell and conexao and sistema_operacional and
            memoria_ram and tipo_memoria and frequencia and processador and
            tipo_hd1 and ativo):
        maquinas.append({
            'NUMSTATUSREGISTRO': num_status_registro,
            'WINREGISTRO': win_registro,
            'OFFICEPATRIMONIO': office_patrimonio,
            'NOTAFISCAL': nota_fiscal,
            'SETOR': setor,
            'USUARIO': usuario,
            'HOSTNAME': host_name,
            'TIPO': tipo,
            'MODELO': modelo,
            'FABRICANTE': fabricante,
            'SERVICETAG': service_tag,
            'CADASTRADELL': cadastrado_dell,
            'CONEXAO': conexao,
            'SISTEMAOPERACIONAL': sistema_operacional,
            'MEMORIARAM': memoria_ram,
            'TIPOMEMORIA': tipo_memoria,
            'FREQUENCIA': frequencia,
            'PROCESSADOR': processador,
            'TIPOHD1': tipo_hd1,
            'ATIVO': ativo
        })
        messagebox.showinfo("Sucesso", "Máquina adicionada com sucesso!")
        entry_num_status_registro.delete(0, tk.END)
        entry_win_registro.delete(0, tk.END)
        entry_office_patrimonio.delete(0, tk.END)
        entry_nota_fiscal.delete(0, tk.END)
        entry_setor.delete(0, tk.END)
        entry_usuario.delete(0, tk.END)
        entry_host_name.delete(0, tk.END)
        entry_tipo.delete(0, tk.END)
        entry_modelo.delete(0, tk.END)
        entry_fabricante.delete(0, tk.END)
        entry_service_tag.delete(0, tk.END)
        entry_cadastrado_dell.delete(0, tk.END)
        entry_conexao.delete(0, tk.END)
        entry_sistema_operacional.delete(0, tk.END)
        entry_memoria_ram.delete(0, tk.END)
        entry_tipo_memoria.delete(0, tk.END)
        entry_frequencia.delete(0, tk.END)
        entry_processador.delete(0, tk.END)
        entry_tipo_hd1.delete(0, tk.END)
        entry_ativo.delete(0, tk.END)
    else:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

def mostrar_dashboard():
    """
    Mostra um gráfico de barras com a contagem de máquinas por status (ATIVO).
    """
    if not maquinas:
        messagebox.showwarning("Atenção", "Nenhuma máquina cadastrada.")
        return

    status_count = {}
    for maquina in maquinas:
        status = maquina['ATIVO']
        if status in status_count:
            status_count[status] += 1
        else:
            status_count[status] = 1

    plt.bar(status_count.keys(), status_count.values())
    plt.title('Status das Máquinas (Ativo)')
    plt.xlabel('Status')
    plt.ylabel('Quantidade')
    plt.show()

def exportar_para_excel():
    """
    Exporta os dados das máquinas para um arquivo Excel.
    """
    if not maquinas:
        messagebox.showwarning("Atenção", "Nenhuma máquina cadastrada para exportar.")
        return

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Dados das Máquinas"

    # Cabeçalho com todos os campos
    cabecalho = ['NUMSTATUSREGISTRO', 'WINREGISTRO', 'OFFICEPATRIMONIO', 'NOTAFISCAL', 'SETOR', 'USUARIO',
                 'HOSTNAME', 'TIPO', 'MODELO', 'FABRICANTE', 'SERVICETAG', 'CADASTRADELL', 'CONEXAO',
                 'SISTEMAOPERACIONAL', 'MEMORIARAM', 'TIPOMEMORIA', 'FREQUENCIA', 'PROCESSADOR',
                 'TIPOHD1', 'ATIVO']
    sheet.append(cabecalho)

    # Adiciona os dados de cada máquina
    for maquina in maquinas:
        linha = [
            maquina['NUMSTATUSREGISTRO'], maquina['WINREGISTRO'], maquina['OFFICEPATRIMONIO'],
            maquina['NOTAFISCAL'], maquina['SETOR'], maquina['USUARIO'], maquina['HOSTNAME'],
            maquina['TIPO'], maquina['MODELO'], maquina['FABRICANTE'], maquina['SERVICETAG'],
            maquina['CADASTRADELL'], maquina['CONEXAO'], maquina['SISTEMAOPERACIONAL'],
            maquina['MEMORIARAM'], maquina['TIPOMEMORIA'], maquina['FREQUENCIA'],
            maquina['PROCESSADOR'], maquina['TIPOHD1'], maquina['ATIVO']
        ]
        sheet.append(linha)

    workbook.save("dados_maquinas.xlsx")
    messagebox.showinfo("Sucesso", "Dados exportados para 'dados_maquinas.xlsx'!")

# Configuração da interface
root = tk.Tk()
root.title("Gerenciamento de Máquinas e Inventário")
root.configure(bg='#f0f0f0')

# Estilo para os widgets
style = ttk.Style()
style.configure('TLabel', font=('Arial', 12), foreground='#555')
style.configure('TButton', font=('Arial', 12),
                background='#6a1b9a',
                foreground='white',
                relief='flat',
                borderwidth=0,
                padding=8)
style.map('TButton',
          background=[('active', '#9c27b0'),
                      ('disabled', '#b8b8b8')],
          foreground=[('disabled', '#777')])
style.configure('TEntry', font=('Arial', 12),
                relief='inset',
                borderwidth=1,
                padding=6,
                background='#f3e5f5',
                fieldbackground='#f3e5f5',
                foreground='#000')

# Campos de entrada com labels estilizados e espaçamento
ttk.Label(root, text="Número Status Registro:", style='TLabel').pack(pady=(10, 2))
entry_num_status_registro = ttk.Entry(root, style='TEntry')
entry_num_status_registro.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Win Registro:", style='TLabel').pack(pady=(10, 2))
entry_win_registro = ttk.Entry(root, style='TEntry')
entry_win_registro.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Office Patrimônio:", style='TLabel').pack(pady=(10, 2))
entry_office_patrimonio = ttk.Entry(root, style='TEntry')
entry_office_patrimonio.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Nota Fiscal:", style='TLabel').pack(pady=(10, 2))
entry_nota_fiscal = ttk.Entry(root, style='TEntry')
entry_nota_fiscal.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Setor:", style='TLabel').pack(pady=(10, 2))
entry_setor = ttk.Entry(root, style='TEntry')
entry_setor.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Usuário:", style='TLabel').pack(pady=(10, 2))
entry_usuario = ttk.Entry(root, style='TEntry')
entry_usuario.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Host Name:", style='TLabel').pack(pady=(10, 2))
entry_host_name = ttk.Entry(root, style='TEntry')
entry_host_name.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Tipo:", style='TLabel').pack(pady=(10, 2))
entry_tipo = ttk.Entry(root, style='TEntry')
entry_tipo.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Modelo:", style='TLabel').pack(pady=(10, 2))
entry_modelo = ttk.Entry(root, style='TEntry')
entry_modelo.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Fabricante:", style='TLabel').pack(pady=(10, 2))
entry_fabricante = ttk.Entry(root, style='TEntry')
entry_fabricante.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Service Tag:", style='TLabel').pack(pady=(10, 2))
entry_service_tag = ttk.Entry(root, style='TEntry')
entry_service_tag.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Cadastrado Dell:", style='TLabel').pack(pady=(10, 2))
entry_cadastrado_dell = ttk.Entry(root, style='TEntry')
entry_cadastrado_dell.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Conexão:", style='TLabel').pack(pady=(10, 2))
entry_conexao = ttk.Entry(root, style='TEntry')
entry_conexao.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Sistema Operacional:", style='TLabel').pack(pady=(10, 2))
entry_sistema_operacional = ttk.Entry(root, style='TEntry')
entry_sistema_operacional.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Memória RAM:", style='TLabel').pack(pady=(10, 2))
entry_memoria_ram = ttk.Entry(root, style='TEntry')
entry_memoria_ram.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Tipo de Memória:", style='TLabel').pack(pady=(10, 2))
entry_tipo_memoria = ttk.Entry(root, style='TEntry')
entry_tipo_memoria.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Frequência:", style='TLabel').pack(pady=(10, 2))
entry_frequencia = ttk.Entry(root, style='TEntry')
entry_frequencia.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Processador:", style='TLabel').pack(pady=(10, 2))
entry_processador = ttk.Entry(root, style='TEntry')
entry_processador.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Tipo de HD1:", style='TLabel').pack(pady=(10, 2))
entry_tipo_hd1 = ttk.Entry(root, style='TEntry')
entry_tipo_hd1.pack(pady=5, padx=20, fill='x')

ttk.Label(root, text="Ativo (Sim/Não):", style='TLabel').pack(pady=(10, 2))
entry_ativo = ttk.Entry(root, style='TEntry')
entry_ativo.pack(pady=5, padx=20, fill='x')

# Botões
botao_adicionar = ttk.Button(root, text="Adicionar Máquina", command=adicionar_maquina, style='TButton')
botao_adicionar.pack(pady=10, padx=20, fill='x')
botao_dashboard = ttk.Button(root, text="Mostrar Dashboard", command=mostrar_dashboard, style='TButton')
botao_dashboard.pack(pady=10, padx=20, fill='x')
botao_exportar = ttk.Button(root, text="Exportar para Excel", command=exportar_para_excel, style='TButton')
botao_exportar.pack(pady=10, padx=20, fill='x')

# Iniciar a interface
root.mainloop()
