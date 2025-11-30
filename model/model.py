from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.G = nx.Graph()

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
        guadagno medio per spedizione >= threshold (euro)
        """
        self.G = nx.Graph()
        edges_valore = self.get_all_edges()
        for edge, valore in edges_valore.items():
            valore = float(valore)
            if valore >= threshold:
                nodo_1, nodo_2 = edge
                self.G.add_edge(nodo_1, nodo_2, weight=valore)
        return self.G

    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """
        n=0
        for elements in self.G.edges():
            n+=1
        self._edges = n
        return self._edges

    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """
        lista_hub=DAO.get_hub()
        lista_hub_distinte = []
        for hub in lista_hub.values():
            if hub.id not in lista_hub_distinte:
                lista_hub_distinte.append(hub.id)
        self._nodes = len(lista_hub_distinte)
        return self._nodes

    def get_all_edges(self):
        """
        Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        lista_spedizioni = DAO.get_spedizione()
        lista_spedizioni_distinte = []
        id_edges = {}
        risultato = {}
        lista_spedizioni_finale = {}
        for spedizione in lista_spedizioni.values():
            tratta = (spedizione.id_hub_origine, spedizione.id_hub_destinazione)
            valore_corrente = float(spedizione.valore_merce)
            if tratta not in lista_spedizioni_distinte:
                lista_spedizioni_distinte.append(tratta)
                risultato[tratta] = valore_corrente
                id_edges[tratta] = 1
            else:
                valore_parziale = risultato[tratta]
                num_edges = id_edges[tratta] + 1
                valore_parziale = valore_parziale + valore_corrente
                risultato[tratta] = valore_parziale
                id_edges[tratta] = num_edges
        for tratta, valore in risultato.items():
            num_edges = id_edges[tratta]
            valore_finale = valore / num_edges
            lista_spedizioni_finale[tratta] = valore_finale

        return lista_spedizioni_finale
