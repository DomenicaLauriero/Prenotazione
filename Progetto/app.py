from flask import Flask, request, jsonify
from flask_cors import CORS
import db_config
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Inizializzazione del database
db_config.init_db()

# Aggiorna il database per aggiungere la colonna "ora" se non esiste
try:
    db_config.add_column_if_not_exists()
except sqlite3.OperationalError:
    # Ignora l'errore se la colonna esiste già
    pass

@app.route('/prenotazioni', methods=['POST'])
def aggiungi_prenotazione():
    """
    Endpoint per aggiungere una nuova prenotazione.
    Esegue controlli di validazione sul nome, la data e l'ora.
    """
    nuova_prenotazione = request.get_json()
    # Validazione del nome: deve essere una stringa alfabetica con spazi
    if not isinstance(nuova_prenotazione['nome'], str) or not nuova_prenotazione['nome'].replace(" ", "").isalpha():
        return jsonify({"errore": "Il nome è invalido. Deve contenere solo lettere e spazi."}), 400
    # Validazione di data e ora
    try:
        # Combinazione di data e ora per creare un oggetto datetime
        data_ora = datetime.strptime(f"{nuova_prenotazione['data']} {nuova_prenotazione['ora']}", "%Y-%m-%d %H:%M")
        if data_ora <= datetime.now():
            return jsonify({"errore": "Data e ora non possono essere nel passato."}), 400
    except ValueError:
        return jsonify({"errore": "Formato di data o ora non valido."}), 400
    # Se tutto è valido, aggiungi la prenotazione al database
    db_config.add_prenotazione(nuova_prenotazione['nome'], nuova_prenotazione['data'], nuova_prenotazione['ora'])
    return jsonify(nuova_prenotazione), 201

@app.route('/prenotazioni', methods=['GET'])
def ottieni_prenotazioni():
    """
    Endpoint per ottenere tutte le prenotazioni esistenti.
    """
    prenotazioni = db_config.get_all_prenotazioni()
    return jsonify(prenotazioni), 200

@app.route('/prenotazioni/<int:id>', methods=['PUT'])
def aggiorna_prenotazione(id):
    """
    Endpoint per aggiornare una prenotazione esistente.
    Esegue controlli di validazione prima di salvare i dati.
    """
    dati_prenotazione = request.get_json()
    # Validazione del nome
    if not isinstance(dati_prenotazione['nome'], str) or not dati_prenotazione['nome'].replace(" ", "").isalpha():
        return jsonify({"errore": "Il nome è invalido. Deve contenere solo lettere e spazi."}), 400
    # Validazione di data e ora
    try:
        # Combinazione di data e ora per creare un oggetto datetime
        data_ora = datetime.strptime(f"{dati_prenotazione['data']} {dati_prenotazione['ora']}", "%Y-%m-%d %H:%M")
        if data_ora <= datetime.now():
            return jsonify({"errore": "Data e ora non possono essere nel passato."}), 400
    except ValueError:
        return jsonify({"errore": "Formato di data o ora non valido."}), 400
    # Se tutto è valido, aggiorna la prenotazione nel database
    db_config.update_prenotazione(id, dati_prenotazione['nome'], dati_prenotazione['data'], dati_prenotazione['ora'])
    return jsonify(dati_prenotazione), 200

@app.route('/prenotazioni/<int:id>', methods=['DELETE'])
def cancella_prenotazione(id):
    """
    Endpoint per cancellare una prenotazione esistente.
    """
    db_config.delete_prenotazione(id)
    return '', 204

if __name__ == '__main__':
    # Avvia l'applicazione Flask in modalità di debug
    app.run(debug=True)
