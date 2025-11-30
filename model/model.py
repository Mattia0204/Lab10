from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None  # memorizza il numero di nodi del grafo
        self._edges = None  # memorizza il numero di archi del grafo
        self.G = nx.Graph()  # inizializza il grafo vuoto

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
        guadagno medio per spedizione >= threshold (euro)
        """
        self.G = nx.Graph()  # ricrea un grafo vuoto
        lista_hub = DAO.get_hub()  # recupera tutti gli hub dal database
        nome_1 = ""  # variabile temporanea per nome del nodo origine
        nome_2 = ""  # variabile temporanea per nome del nodo destinazione
        acr_1 = ""   # variabile temporanea per acronimo (es. TO per Torino) del nodo origine
        acr_2 = ""   # variabile temporanea per acronimo (es. TO per Torino) del nodo origine
        edges_valore = self.get_all_edges()  # calcola tutte le tratte con valore medio
        for edge, valore in edges_valore.items():  # scorre tutte le tratte
            valore = float(valore)  # converte il valore medio a float
            if valore >= threshold:  # filtra solo le tratte sopra la soglia
                nodo_1, nodo_2 = edge  # prende gli id degli hub dalla tupla
                for hub in lista_hub.values():  # cerca i nomi degli hub
                    if nodo_1 == hub.id:
                        nome_1 = hub.nome  # salva il nome del nodo origine
                        acr_1 = hub.stato  # salva lo stato del nodo origine
                    if nodo_2 == hub.id:
                        nome_2 = hub.nome  # salva il nome del nodo destinazione
                        acr_2 = hub.stato   # salva lo stato del nodo destinazione
                self.G.add_edge((nome_1, acr_1), (nome_2, acr_2), weight=valore)  # aggiunge l'arco al grafo con peso
        return self.G  # restituisce il grafo costruito

    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """
        n=0  # contatore degli archi
        for elements in self.G.edges():  # scorre tutti gli archi nel grafo
            n+=1  # incrementa il contatore
        self._edges = n  # salva il numero totale di archi
        return self._edges  # restituisce il numero di archi

    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """
        lista_hub=DAO.get_hub()  # recupera tutti gli hub dal database
        lista_hub_distinte = []  # lista per memorizzare hub unici
        for hub in lista_hub.values():  # scorre tutti gli hub
            if hub.id not in lista_hub_distinte:  # verifica se l'hub è già aggiunto
                lista_hub_distinte.append(hub.id)  # aggiunge l'hub alla lista unica
        self._nodes = len(lista_hub_distinte)  # calcola il numero totale di nodi
        return self._nodes  # restituisce il numero di nodi

    def get_all_edges(self):
        """
        Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        lista_spedizioni = DAO.get_spedizione()  # recupera tutte le spedizioni dal database
        lista_spedizioni_distinte = []  # lista per tracciare tratte già considerate
        id_edges = {}  # dizionario per contare quante volte appare ogni tratta
        risultato = {}  # dizionario per sommare il valore totale di ciascuna tratta
        lista_spedizioni_finale = {}  # dizionario finale con valore medio per tratta
        for spedizione in lista_spedizioni.values():  # scorre tutte le spedizioni
            tratta = tuple(sorted((spedizione.id_hub_origine, spedizione.id_hub_destinazione)))  # tratta indifferente alla direzione
            valore_corrente = float(spedizione.valore_merce)  # converte il valore a float
            if tratta not in lista_spedizioni_distinte:  # se la tratta non è ancora stata aggiunta
                lista_spedizioni_distinte.append(tratta)  # aggiunge la tratta alla lista
                risultato[tratta] = valore_corrente  # inizializza il valore totale della tratta
                id_edges[tratta] = 1  # inizializza il contatore della tratta
            else:  # se la tratta è già presente
                valore_parziale = risultato[tratta]  # recupera il valore accumulato
                num_edges = id_edges[tratta] + 1  # incrementa il contatore
                valore_parziale = valore_parziale + valore_corrente  # somma il nuovo valore
                risultato[tratta] = valore_parziale  # aggiorna il valore totale
                id_edges[tratta] = num_edges  # aggiorna il contatore
        for tratta, valore in risultato.items():  # calcola il valore medio per ogni tratta
            num_edges = id_edges[tratta]  # recupera il numero di spedizioni per quella tratta
            valore_finale = valore / num_edges  # calcola il valore medio
            lista_spedizioni_finale[tratta] = valore_finale  # salva il valore medio finale

        return lista_spedizioni_finale  # restituisce il dizionario delle tratte con valori medi
