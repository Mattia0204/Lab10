import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view  # memorizza il riferimento alla view
        self._model = model  # memorizza il riferimento al modello

    def mostra_tratte(self, e):
        """
        Funzione che controlla prima se il valore del costo inserito sia valido (es. non deve essere una stringa) e poi
        popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Hub presenti
        * Numero di Tratte
        * Lista di Tratte che superano il costo indicato come soglia
        """
        try:
            guadagno_medio_minimo = float(self._view.guadagno_medio_minimo.value)  # legge il valore inserito dall'utente e lo converte in float
        except (ValueError, TypeError) as e:  # intercetta errori di conversione (es. input non numerico)
            self._view.show_alert("Bisogna inserire un valore intero o float come guadagno medio minimo")  # mostra alert se il valore non è valido
            return  # esce dalla funzione se c'è un errore
        G = self._model.costruisci_grafo(guadagno_medio_minimo)  # costruisce il grafo filtrando le tratte sopra la soglia

        self._view.lista_visualizzazione.controls.clear()  # pulisce la lista attuale nella ListView
        self._view.lista_visualizzazione.controls.append(ft.Text(f"Numero di Hubs: {self._model.get_num_nodes()}"))  # aggiunge il numero di hub alla lista
        self._view.lista_visualizzazione.controls.append(ft.Text(f"Numero di tratte: {self._model.get_num_edges()}"))  # aggiunge il numero di tratte alla lista

        i=1  # contatore per numerare le tratte
        for u, v, d in G.edges(data=True):  # scorre tutti gli archi del grafo con i dati associati
            self._view.lista_visualizzazione.controls.append(ft.Text(f"{i}) [{u} -> {v}] -- Guadagno medio per spedizione €{d.get('weight')}"))  # aggiunge ogni tratta con il suo guadagno medio
            i+=1  # incrementa il contatore
        self._view.lista_visualizzazione.update()  # aggiorna la ListView per riflettere i cambiamenti
