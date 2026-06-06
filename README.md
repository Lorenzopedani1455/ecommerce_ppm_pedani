# Back-end PPM 2026 - E-commerce API

**Studente:** Lorenzo Pedani  
**Project Type:** REST API  
**Framework Usato:** Django & Django REST Framework  

## 1. Descrizione del Progetto
Questa applicazione back-end implementa un'API RESTful per un sistema di E-commerce (Track 2). Gestisce l'autenticazione tramite token JWT e divide la logica in app modulari (`users` e `shop`). Offre funzionalità di gestione catalogo (categorie e prodotti), gestione del carrello e completamento ordini con simulazione di controllo stock in tempo reale. Include anche un client frontend in vanilla JavaScript.

## 2. Funzionalità e Ruoli Utente
Il sistema implementa permessi basati sui ruoli tramite classi di permission custom in DRF:

* **Ospite (Non Autenticato):**
    * Può visualizzare il catalogo prodotti e le categorie (sola lettura).
    * Può registrarsi come nuovo utente.
* **Customer (Utente Autenticato):**
    * Tutti i permessi dell'ospite.
    * Gestione del proprio profilo e carrello personale.
    * Creazione di ordini (checkout) con scalamento automatico dello stock.
    * Visualizzazione dello storico dei propri ordini.
* **Store Manager (Ruolo Avanzato):**
    * Tutti i permessi del Customer.
    * Gestione completa CRUD su Prodotti e Categorie.
    * Visualizzazione di tutti gli ordini effettuati sulla piattaforma.
    * Modifica dello stato degli ordini (es. da "pending" a "shipped") o cancellazione degli stessi.

## 3. Istruzioni per l'Installazione Locale
Per avviare il progetto localmente, eseguire i seguenti comandi nel terminale:

1. Clonare la repository e accedere alla cartella.
2. Creare e attivare l'ambiente virtuale:
   ```bash
   python3 -m venv venv
   source venv/bin/activate