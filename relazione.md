# Relazione Tecnica: Web Server Minimale in Python

## 1. Introduzione

Questo documento descrive l'implementazione di un server HTTP minimale sviluppato interamente in Python, utilizzando solo il modulo `socket` della libreria standard. Il server è in grado di gestire richieste HTTP di base e di servire un sito web statico composto da file HTML, CSS e JavaScript.

## 2. Architettura del Server

### 2.1 Panoramica

Il server è stato progettato con un'architettura multi-thread per gestire più connessioni contemporaneamente. È costituito dai seguenti componenti principali:

- **Socket Server**: Gestisce le connessioni TCP a livello di rete
- **HTTP Request Handler**: Analizza le richieste HTTP e genera risposte appropriate
- **File System Handler**: Recupera i file dal filesystem e li serve al client
- **Logger**: Registra le attività e le richieste del server

### 2.2 Flusso di Esecuzione

1. Il server inizializza un socket TCP e si mette in ascolto sulla porta specificata (8080)
2. Quando un client si connette, viene creato un nuovo thread per gestire la connessione
3. Il thread analizza la richiesta HTTP ricevuta dal client
4. Se la richiesta è valida, il server tenta di recuperare il file richiesto dalla directory `www/`
5. Il server invia una risposta HTTP appropriata insieme al contenuto del file (se trovato) o un errore 404
6. La connessione viene chiusa e il thread termina

## 3. Implementazione

### 3.1 Inizializzazione del Server

Il server viene inizializzato nella funzione `main()`, che svolge le seguenti operazioni:

- Inizializza i tipi MIME riconosciuti
- Verifica l'esistenza della directory dei documenti
- Crea un file di log se non esiste
- Crea e configura il socket del server
- Avvia il loop principale del server che accetta connessioni

### 3.2 Gestione delle Connessioni

La funzione `handle_client()` gestisce ogni singola connessione client:

- Riceve e decodifica i dati della richiesta HTTP
- Estrae la prima riga della richiesta per identificare metodo, percorso e versione del protocollo
- Gestisce solo le richieste GET (requisito minimo)
- Reindirizza automaticamente le richieste alla radice (`/`) verso `index.html`
- Verifica che il file richiesto esista ed è all'interno della directory consentita
- Legge il contenuto del file e identifica il tipo MIME
- Costruisce e invia la risposta HTTP appropriata

### 3.3 Gestione degli Errori

Il server implementa una robusta gestione degli errori:

- **Errore 404 (Not Found)**: Viene restituito quando il file richiesto non viene trovato
- **Errore 500 (Internal Server Error)**: Viene restituito in caso di errori interni del server
- **Validazione del percorso**: Impedisce tentativi di directory traversal per motivi di sicurezza

### 3.4 Logging

Il server registra tutte le richieste in un file di log (`server.log`), memorizzando:

- Timestamp della richiesta
- Indirizzo IP e porta del client
- Riga della richiesta originale
- Codice di stato HTTP della risposta

### 3.5 Supporto MIME Types

Il server identifica automaticamente il tipo di contenuto (MIME type) dei file richiesti utilizzando il modulo `mimetypes` di Python. Questo permette di inviare l'header `Content-Type` corretto nelle risposte HTTP.

## 4. Il Sito Web Demo

### 4.1 Struttura del Sito

Il sito web dimostrativo è composto da:

- **index.html**: Homepage con introduzione
- **chi-siamo.html**: Pagina informativa sul progetto
- **contatti.html**: Pagina con contatti e FAQ
- **style.css**: Foglio di stile condiviso tra tutte le pagine

### 4.2 Caratteristiche dell'Interfaccia

- **Design Responsive**: Il layout si adatta a diverse dimensioni di schermo
- **Navigazione**: Menu di navigazione funzionale e intuitivo
- **Animazioni CSS**: Effetti di transizione e animazione per migliorare l'esperienza utente
- **Interattività JavaScript**: Script per gestire le funzionalità interattive come FAQ e form

### 4.3 Best Practices Implementate

- **CSS Modulare**: Stili organizzati per componenti
- **Markup Semantico**: Utilizzo appropriato di tag HTML5
- **Progressive Enhancement**: Funzionalità base accessibili anche senza JavaScript
- **Compatibilità Cross-Browser**: Stile e funzionalità consistenti su diversi browser

## 5. Estensioni Implementate

### 5.1 Supporto MIME Types

Il server è in grado di riconoscere e servire correttamente diversi tipi di file:

- HTML (text/html)
- CSS (text/css)
- JavaScript (text/javascript)
- Immagini (image/jpeg, image/png, ecc.)
- Altri tipi comuni di file

### 5.2 Sistema di Logging

Il server implementa un sistema di logging completo che registra:

- Tutte le richieste ricevute
- Tempo di elaborazione
- Codici di stato delle risposte
- Eventuali errori

### 5.3 Design Responsivo e Animazioni

Il sito web dimostrativo include:

- Layout che si adatta a dispositivi mobili e desktop
- Animazioni CSS per migliorare l'esperienza utente
- Transizioni fluide tra gli elementi dell'interfaccia

## 6. Sicurezza

### 6.1 Misure Implementate

- **Validazione dei percorsi**: Prevenzione di attacchi di tipo directory traversal
- **Limitazione dei metodi HTTP**: Supporto solo per richieste GET
- **Controllo degli accessi**: I file possono essere serviti solo dalla directory `www/`

### 6.2 Limitazioni

Essendo un server dimostrativo, sono presenti alcune limitazioni:

- Nessun supporto per HTTPS
- Nessuna autenticazione o autorizzazione
- Nessuna protezione avanzata contro attacchi DDoS o altri tipi di attacchi web

## 7. Istruzioni per l'Uso

### 7.1 Requisiti

- Python 3.6 o superiore

### 7.2 Esecuzione del Server

1. Posiziona il file `server.py` e la directory `www/` nella stessa cartella
2. Esegui il comando: `python server.py`
3. Accedi al sito tramite un browser all'indirizzo: `http://localhost:8080`

### 7.3 Personalizzazione

Per modificare le impostazioni del server, è possibile modificare le variabili all'inizio del file `server.py`:

- `HOST`: L'indirizzo su cui il server risponde (default: localhost)
- `PORT`: La porta su cui il server è in ascolto (default: 8080)
- `DOCUMENT_ROOT`: La directory da cui servire i file (default: www)

## 8. Conclusioni

Questo progetto dimostra come sia possibile implementare un server HTTP funzionale utilizzando solo la libreria standard di Python. Sebbene minimale, il server include tutte le funzionalità di base necessarie per servire un sito web statico.

Il server è stato progettato principalmente a scopo didattico e dimostrativo, per comprendere i principi fondamentali del protocollo HTTP e dell'implementazione di un server web. Per ambienti di produzione, si raccomanda l'utilizzo di server web più robusti e completi come Nginx, Apache o framework web come Flask o Django con server WSGI.

