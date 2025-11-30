import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_tratte(self, e):
        """
        Funzione che controlla prima se il valore del costo inserito sia valido (es. non deve essere una stringa) e poi
        popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Hub presenti
        * Numero di Tratte
        * Lista di Tratte che superano il costo indicato come soglia
        """
        try:
            guadagno_medio_minimo = float(self._view.guadagno_medio_minimo.value)
        except (ValueError, TypeError) as e:
            self._view.show_alert("Bisogna inserire un valore intero o float come guadagno medio minimo")
            return
        G = self._model.costruisci_grafo(guadagno_medio_minimo)

        self._view.lista_visualizzazione.controls.clear()
        self._view.lista_visualizzazione.controls.append(ft.Text(f"Numero di Hubs: {self._model.get_num_nodes()}"))
        self._view.lista_visualizzazione.controls.append(ft.Text(f"Numero di tratte: {self._model.get_num_edges()}"))

        i=1
        for u, v, d in G.edges(data=True):
            self._view.lista_visualizzazione.controls.append(ft.Text(f"{i}) [{u} -> {v}] -- Guadagno medio per spedizione €{d.get('weight')}"))
            i+=1
        self._view.lista_visualizzazione.update()