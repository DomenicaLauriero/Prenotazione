import sqlite3
from datetime import datetime

# Inizializza il database se non esiste già
def init_db():
    """
    Crea la tabella 'prenotazioni' se non esiste.
    La tabella contiene:
    - id: Identificativo unico.
    - nome: Nome e cognome della persona.
    - data: Data della prenotazione.
    - ora: Ora della prenotazione.
    """
    conn = sqlite3.connect('prenotazioni.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS prenotazioni
                      (id INTEGER PRIMARY KEY, 
                      nome TEXT NOT NULL, 
                      data TEXT NOT NULL, 
                      ora TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Aggiunge una prenotazione al database
def add_prenotazione(nome, data, ora):
    """
    Aggiunge una nuova prenotazione al database.
    - nome: Nome e cognome del cliente (stringa).
    - data: Data della prenotazione (formato YYYY-MM-DD).
    - ora: Ora della prenotazione (formato HH:MM).
    """
    # Convalida input
    if not nome.strip() or not data.strip() or not ora.strip():
        raise ValueError("Tutti i campi sono obbligatori.")
    
    # Convalida formato e futuro della data e ora
    datetime_prenotazione = datetime.strptime(f"{data} {ora}", "%Y-%m-%d %H:%M")
    if datetime_prenotazione < datetime.now():
        raise ValueError("Non è possibile prenotare in una data o ora passata.")

    # Inserimento nel database
    conn = sqlite3.connect('prenotazioni.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prenotazioni (nome, data, ora) VALUES (?, ?, ?)", (nome.strip(), data.strip(), ora.strip()))
    conn.commit()
    conn.close()

# Restituisce tutte le prenotazioni
def get_all_prenotazioni():
    """
    Ottiene tutte le prenotazioni presenti nel database.
    Restituisce una lista di tuple con i dettagli delle prenotazioni.
    """
    conn = sqlite3.connect('prenotazioni.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prenotazioni")
    results = cursor.fetchall()
    conn.close()
    return results

# Aggiorna una prenotazione esistente
def update_prenotazione(id, nome, data, ora):
    """
    Aggiorna una prenotazione esistente.
    - id: ID della prenotazione da aggiornare.
    - nome: Nuovo nome del cliente.
    - data: Nuova data della prenotazione.
    - ora: Nuova ora della prenotazione.
    """
    # Convalida input
    if not nome.strip() or not data.strip() or not ora.strip():
        raise ValueError("Tutti i campi sono obbligatori.")
    
    # Convalida formato e futuro della data e ora
    datetime_prenotazione = datetime.strptime(f"{data} {ora}", "%Y-%m-%d %H:%M")
    if datetime_prenotazione < datetime.now():
        raise ValueError("Non è possibile impostare una data o ora passata.")

    # Aggiornamento nel database
    conn = sqlite3.connect('prenotazioni.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE prenotazioni SET nome = ?, data = ?, ora = ? WHERE id = ?", (nome.strip(), data.strip(), ora.strip(), id))
    conn.commit()
    conn.close()

# Cancella una prenotazione esistente
def delete_prenotazione(id):
    """
    Cancella una prenotazione esistente dal database.
    - id: ID della prenotazione da cancellare.
    """
    conn = sqlite3.connect('prenotazioni.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prenotazioni WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# Aggiunge una colonna alla tabella se non esiste
def add_column_if_not_exists():
    """
    Aggiunge la colonna 'ora' alla tabella 'prenotazioni' se non esiste.
    Questa funzione è utile per aggiornamenti futuri dello schema.
    """
    conn = sqlite3.connect('prenotazioni.db')
    cursor = conn.cursor()
    # Controlla se la colonna 'ora' esiste
    cursor.execute("PRAGMA table_info(prenotazioni)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'ora' not in columns:
        cursor.execute("ALTER TABLE prenotazioni ADD COLUMN ora TEXT")
    conn.commit()
    conn.close()
