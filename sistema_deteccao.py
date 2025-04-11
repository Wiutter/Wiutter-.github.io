import socket
import threading
import json
import time
from datetime import datetime
import hashlib
import hmac
import random

# Configuração
HOST = '0.0.0.0'  # Escuta em todos os interfaces
PORT = 12345
BUFFER_SIZE = 1024
SECRET_KEY = b'super_seguro_123'  # Chave secreta para HMAC

# Estruturas de Dados
alertas = []
logs = []
amenacas_conhecidas = {
    "ataques_port_scan": [80, 443, 22, 21, 23, 3389],
    "ip_maliciosos": ["192.168.1.100", "10.0.0.5"],
    "assinaturas_ataques": ["SYN Flood", "DDoS", "SQL Injection"],
    "comportamentos_anomalos": ["login_falhado_excesso", "transferencia_grande_ficheiro_incomum"]
}

# Funções Auxiliares
def registar_log(tipo, mensagem, detalhes=None):
    """
    Regista um log de evento com timestamp.
    """
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "tipo": tipo,
        "mensagem": mensagem,
        "detalhes": detalhes
    }
    logs.append(log_entry)
    print(f"LOG: {log_entry}")  # Para debugging

def gerar_alerta(tipo, mensagem, gravidade, detalhes=None):
    """
    Gera um alerta de segurança com timestamp e gravidade.
    """
    timestamp = datetime.now().isoformat()
    alerta = {
        "timestamp": timestamp,
        "tipo": tipo,
        "mensagem": mensagem,
        "gravidade": gravidade,  # "info", "aviso", "critico"
        "detalhes": detalhes
    }
    alertas.append(alerta)
    print(f"ALERTA: {alerta}")  # Para debugging
    # TODO: Adicionar envio de alerta (email, Slack, etc.)

def verificar_hmac(mensagem_recebida, assinatura_recebida):
    """
    Verifica a integridade da mensagem usando HMAC-SHA256.
    """
    hmac_gerado = hmac.new(SECRET_KEY, mensagem_recebida.encode('utf-8'), hashlib.sha256).digest()
    return hmac.compare_digest(hmac_gerado, assinatura_recebida)

def simular_evento(tipo_evento, sock, addr):
    """
    Simula um evento de segurança para testes.
    """
    if tipo_evento == "porta_scan":
        porta = random.choice(amenacas_conhecidas["ataques_port_scan"])
        mensagem = f"SCAN: Port Scan detetado em porta {porta}"
        gravidade = "aviso"
        detalhes = {"porta": porta, "ip_origem": addr[0]}
        return mensagem, gravidade, detalhes
    elif tipo_evento == "ip_malicioso":
        mensagem = f"MALICIOSO: IP {addr[0]} detetado na lista negra"
        gravidade = "critico"
        detalhes = {"ip_origem": addr[0]}
        return mensagem, gravidade, detalhes
    elif tipo_evento == "assinatura_ataque":
        assinatura = random.choice(amenacas_conhecidas["assinaturas_ataques"])
        mensagem = f"ATAQUE: Assinatura de ataque detetada - {assinatura}"
        gravidade = "critico"
        detalhes = {"assinatura": assinatura}
        return mensagem, gravidade, detalhes
    elif tipo_evento == "comportamento_anomalo":
        comportamento = random.choice(amenacas_conhecidas["comportamentos_anomalos"])
        mensagem = f"ANOMALIA: Comportamento anómalo detetado - {comportamento}"
        gravidade = "aviso"
        detalhes = {"comportamento": comportamento}
        return mensagem, gravidade, detalhes
    else:
        return "Evento desconhecido", "info", {}

# Função para lidar com a ligação de cada cliente
def lidar_cliente(sock, addr):
    """
    Lida com a comunicação com um cliente.
    """
    registar_log("info", f"Ligação estabelecida com {addr}")
    try:
        while True:
            # Recebe dados com um timeout
            sock.settimeout(5)  # Timeout de 5 segundos
            try:
                dados_recebidos = sock.recv(BUFFER_SIZE)
            except socket.timeout:
                continue  # Volta para o início do loop para verificar se o socket foi fechado

            if not dados_recebidos:
                registar_log("info", f"Ligação encerrada por {addr}")
                break

            # Verifica o HMAC
            try:
                assinatura_recebida = dados_recebidos[-32:]  # Últimos 32 bytes são a assinatura
                mensagem_recebida = dados_recebidos[:-32].decode('utf-8')
                if not verificar_hmac(mensagem_recebida, assinatura_recebida):
                    registar_log("aviso", "Falha na verificação do HMAC. Ligação encerrada.")
                    sock.send(b"ERRO: HMAC verification failed")
                    break
                mensagem_recebida = mensagem_recebida
            except Exception as e:
                registar_log("erro", f"Erro ao verificar HMAC: {e}")
                sock.send(b"ERRO: HMAC error")
                break

            # Processa a mensagem recebida
            if mensagem_recebida.lower() == "simular ataque":
                tipo_evento = random.choice(["porta_scan", "ip_malicioso", "assinatura_ataque", "comportamento_anomalo"])
                mensagem, gravidade, detalhes = simular_evento(tipo_evento, sock, addr)
                gerar_alerta(mensagem, gravidade, detalhes)
                sock.send(b"OK: Ataque simulado")  # Envia confirmação
            elif mensagem_recebida.lower() == "listar alertas":
                sock.send(json.dumps(alertas).encode('utf-8'))
            elif mensagem_recebida.lower() == "listar logs":
                sock.send(json.dumps(logs).encode('utf-8'))
            elif mensagem_recebida.lower() == "terminar":
                sock.send(b"OK: Ligação terminada")
                break
            else:
                mensagem = f"Recebido: {mensagem_recebida}"
                gravidade = "info"
                detalhes = {"mensagem_recebida": mensagem_recebida}
                registar_log("info", mensagem, detalhes)
                sock.send(b"OK: Comando recebido") # Envia OK para o cliente

    except Exception as e:
        registar_log("erro", f"Erro ao lidar com cliente {addr}: {e}")
    finally:
        sock.close()

def iniciar_servidor():
    """
    Inicia o servidor de escuta.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reutilizar o endereço
    sock.bind((HOST, PORT))
    sock.listen(5)  # Aceita até 5 ligações em espera
    registar_log("info", f"Servidor a escutar em {HOST}:{PORT}")

    try:
        while True:
            cliente_sock, addr = sock.accept()
            # Cria uma thread para lidar com cada cliente
            cliente_thread = threading.Thread(target=lidar_cliente, args=(cliente_sock, addr))
            cliente_thread.start()
    except KeyboardInterrupt:
        registar_log("info", "Servidor encerrado por interrupção do utilizador.")
    finally:
        sock.close()

if __name__ == "__main__":
    iniciar_servidor()

