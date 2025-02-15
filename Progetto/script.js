document.getElementById('prenotazione-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const nome = document.getElementById('nome').value.trim();
    const data = document.getElementById('data').value;
    const ora = document.getElementById('ora').value;

    // Validazione del nome: deve contenere solo caratteri alfabetici e spazi
    const nomeRegex = /^[a-zA-Z\s]+$/;
    if (!nomeRegex.test(nome)) {
        alert("Il nome può contenere solo lettere e spazi.");
        return;
    }

    // Validazione della data e dell'ora
    const dataOraInserita = new Date(`${data}T${ora}`);
    const dataOraCorrente = new Date();
    if (dataOraInserita <= dataOraCorrente) {
        alert("La prenotazione non può essere in una data o orario passati.");
        return;
    }

    // Invio dei dati al server
    fetch('http://localhost:5000/prenotazioni', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nome: nome, data: data, ora: ora })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('risultato').innerText = `Prenotazione confermata per ${data.nome} il ${data.data} alle ${data.ora}`;
        caricaPrenotazioni();
    })
    .catch(error => {
        console.error("Errore nella prenotazione:", error);
        alert("Si è verificato un errore durante la prenotazione.");
    });
});

// Funzione per caricare le prenotazioni dal server
// function caricaPrenotazioni() {
//     fetch('http://localhost:5000/prenotazioni')
//     .then(response => response.json())
//     .then(data => {
//         const listaPrenotazioni = document.getElementById('prenotazioni-lista');
//         listaPrenotazioni.innerHTML = '';
//         data.forEach(prenotazione => {
//             const div = document.createElement('div');
//             div.innerHTML = `Prenotazione ID ${prenotazione[0]}: ${prenotazione[1]} il ${prenotazione[2]} alle ${prenotazione[3]}
//                               <button onclick="modificaPrenotazione(${prenotazione[0]}, '${prenotazione[1]}', '${prenotazione[2]}', '${prenotazione[3]}')">Modifica</button>
//                               <button onclick="cancellaPrenotazione(${prenotazione[0]})">Cancella</button>`;
//             listaPrenotazioni.appendChild(div);
//         });
//     })
//     .catch(error => {
//         console.error("Errore nel caricamento delle prenotazioni:", error);
//         alert("Si è verificato un errore durante il caricamento delle prenotazioni.");
//     });
// }


function caricaPrenotazioni() {
    fetch('http://localhost:5000/prenotazioni')
        .then(response => response.json())
        .then(data => {
            const listaPrenotazioni = document.getElementById('prenotazioni-lista');
            listaPrenotazioni.innerHTML = ''; // Svuota la tabella prima di ricaricarla

            data.forEach(prenotazione => {
                const row = document.createElement('tr'); // Crea una nuova riga

                // Colonna ID
                const idCell = document.createElement('td');
                idCell.textContent = prenotazione[0];
                row.appendChild(idCell);

                // Colonna Nome
                const nomeCell = document.createElement('td');
                nomeCell.textContent = prenotazione[1];
                row.appendChild(nomeCell);

                // Colonna Data
                const dataCell = document.createElement('td');
                dataCell.textContent = prenotazione[2];
                row.appendChild(dataCell);

                // Colonna Ora
                const oraCell = document.createElement('td');
                oraCell.textContent = prenotazione[3];
                row.appendChild(oraCell);

                // Colonna Azioni
                const azioniCell = document.createElement('td');
                const modificaButton = document.createElement('button');
                modificaButton.textContent = 'Modifica';
                modificaButton.onclick = () => modificaPrenotazione(
                    prenotazione[0],
                    prenotazione[1],
                    prenotazione[2],
                    prenotazione[3]
                );

                const cancellaButton = document.createElement('button');
                cancellaButton.textContent = 'Cancella';
                cancellaButton.onclick = () => cancellaPrenotazione(prenotazione[0]);

                azioniCell.appendChild(modificaButton);
                azioniCell.appendChild(cancellaButton);
                row.appendChild(azioniCell);

                listaPrenotazioni.appendChild(row); // Aggiungi la riga alla tabella
            });
        });
}


// Funzione per modificare una prenotazione
function modificaPrenotazione(id, nome, data, ora) {
    const nuovoNome = prompt("Inserisci il nuovo nome:", nome)?.trim();
    const nuovaData = prompt("Inserisci la nuova data (AAAA-MM-GG):", data);
    const nuovaOra = prompt("Inserisci la nuova ora (HH:MM):", ora);

    // Validazione del nome
    const nomeRegex = /^[a-zA-Z\s]+$/;
    if (!nomeRegex.test(nuovoNome)) {
        alert("Il nome può contenere solo lettere e spazi.");
        return;
    }

    // Validazione della data e dell'ora
    const dataOraInserita = new Date(`${nuovaData}T${nuovaOra}`);
    const dataOraCorrente = new Date();
    if (dataOraInserita <= dataOraCorrente) {
        alert("La prenotazione non può essere in una data o orario passati.");
        return;
    }

    fetch(`http://localhost:5000/prenotazioni/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nome: nuovoNome, data: nuovaData, ora: nuovaOra })
    })
    .then(response => response.json())
    .then(data => {
        caricaPrenotazioni();
    })
    .catch(error => {
        console.error("Errore nella modifica della prenotazione:", error);
        alert("Si è verificato un errore durante la modifica della prenotazione.");
    });
}

// Funzione per cancellare una prenotazione
function cancellaPrenotazione(id) {
    if (!confirm("Sei sicuro di voler cancellare questa prenotazione?")) {
        return;
    }

    fetch(`http://localhost:5000/prenotazioni/${id}`, {
        method: 'DELETE'
    })
    .then(() => {
        caricaPrenotazioni();
    })
    .catch(error => {
        console.error("Errore nella cancellazione della prenotazione:", error);
        alert("Si è verificato un errore durante la cancellazione della prenotazione.");
    });
}

// Carica inizialmente tutte le prenotazioni
caricaPrenotazioni();
