#!/usr/bin/env python3
import socket
import os
import datetime
import threading
import mimetypes

# Configurazione del server
HOST = 'localhost'
PORT = 8080
DOCUMENT_ROOT = 'www'

# Configurazione del logger
LOG_FILE = 'server.log'

# Dizionario dei codici di stato HTTP
HTTP_STATUS = {
    200: 'OK',
    404: 'Not Found',
    500: 'Internal Server Error'
}

def log_request(client_address, request_line, status_code):
    """Registra le richieste in un file di log"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {client_address[0]}:{client_address[1]} - {request_line} - {status_code}\n"
    
    # Stampa a console
    print(log_entry.strip())
    
    # Scrivi nel file di log
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)

def get_mime_type(file_path):
    """Determina il MIME type del file richiesto"""
    return mimetypes.guess_type(file_path)[0] or 'application/octet-stream'

def handle_client(client_socket, client_address):
    """Gestisce una singola connessione client"""
    try:
        # Ricevi i dati della richiesta
        request_data = client_socket.recv(1024).decode('utf-8')
        if not request_data:
            return
            
        # Estrai la prima riga della richiesta
        request_line = request_data.splitlines()[0]
        
        # Analizza la richiesta
        method, path, _ = request_line.split(' ', 2)
        
        # Gestisci solo le richieste GET
        if method != 'GET':
            response = build_response(501, b'Metodo non supportato', 'text/plain')
            client_socket.sendall(response)
            log_request(client_address, request_line, 501)
            return
            
        # Gestisci il percorso della richiesta
        if path == '/':
            path = '/index.html'  # Pagina predefinita
        
        # Costruisci il percorso del file sul filesystem
        file_path = os.path.join(DOCUMENT_ROOT, path.lstrip('/'))
        
        try:
            # Assicurati che il file esista e sia all'interno della directory www
            if not os.path.normpath(file_path).startswith(os.path.normpath(DOCUMENT_ROOT)):
                raise FileNotFoundError("Tentativo di directory traversal")
                
            # Apri e leggi il file
            with open(file_path, 'rb') as f:
                content = f.read()
                
            # Ottieni il MIME type del file
            mime_type = get_mime_type(file_path)
            
            # Costruisci e invia la risposta HTTP
            response = build_response(200, content, mime_type)
            client_socket.sendall(response)
            log_request(client_address, request_line, 200)
            
        except FileNotFoundError:
            # Gestione file non trovato (404)
            content = b'<html><body><h1>404 - File non trovato</h1><p>La risorsa richiesta non esiste sul server.</p></body></html>'
            response = build_response(404, content, 'text/html')
            client_socket.sendall(response)
            log_request(client_address, request_line, 404)
            
    except Exception as e:
        # Gestione errore interno del server (500)
        content = f'<html><body><h1>500 - Errore Interno del Server</h1><p>{str(e)}</p></body></html>'.encode('utf-8')
        response = build_response(500, content, 'text/html')
        client_socket.sendall(response)
        log_request(client_address, request_line if 'request_line' in locals() else "ERRORE", 500)
        
    finally:
        # Chiudi la connessione
        client_socket.close()

def build_response(status_code, content, content_type):
    """Costruisce una risposta HTTP con lo status code e il contenuto forniti"""
    status_message = HTTP_STATUS.get(status_code, 'Unknown')
    headers = [
        f'HTTP/1.1 {status_code} {status_message}',
        f'Content-Type: {content_type}',
        f'Content-Length: {len(content)}',
        'Connection: close',
        'Server: PythonMinimalHTTP/1.0',
        '\r\n'  # Linea vuota per separare gli header dal body
    ]
    header_bytes = '\r\n'.join(headers).encode('utf-8')
    
    # Combina headers e content
    return header_bytes + content

def main():
    """Funzione principale del server"""
    # Inizializza l'elenco dei MIME types conosciuti
    mimetypes.init()
    
    # Assicurati che la directory radice dei documenti esista
    if not os.path.exists(DOCUMENT_ROOT):
        os.makedirs(DOCUMENT_ROOT)
        
    # Crea il file di log se non esiste
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.write(f"# Server log avviato il {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Crea il socket del server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Associa il socket all'indirizzo e porta specificati
        server_socket.bind((HOST, PORT))
        
        # Metti il socket in ascolto
        server_socket.listen(5)  # 5 connessioni in coda
        
        print(f"Server in ascolto su http://{HOST}:{PORT}")
        print(f"Documenti serviti dalla directory: {os.path.abspath(DOCUMENT_ROOT)}")
        print("Premi Ctrl+C per terminare il server")
        
        # Loop principale del server
        while True:
            client_socket, client_address = server_socket.accept()
            # Gestisci ogni connessione in un thread separato
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\nServer terminato dall'utente")
        
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
