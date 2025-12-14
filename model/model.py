import networkx as nx

from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.peso_min = 10000
        self.peso_max  = 0
        self.G = nx.Graph()

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        self.G.clear()
        lista_nodi = DAO().getRifugio()
        lista_archi = DAO().getGrafo(year)
        lista_rifugi = []
        for arco in lista_archi:
            id_rifugio1 = arco['id_rifugio1']
            id_rifugio2 = arco['id_rifugio2']
            lista_rifugi.append(id_rifugio1)
            lista_rifugi.append(id_rifugio2)
            distanza = float(arco['distanza'])
            difficolta = arco['difficolta']
            if difficolta=="facile":
                difficolta = 1
            elif difficolta =="media":
                difficolta = 1.5
            elif difficolta =="difficile":
                difficolta = 2
            peso = distanza*difficolta
            self.G.add_edge(id_rifugio1, id_rifugio2, weight=peso)
        for nodo in lista_nodi:
            if nodo in lista_rifugi:
                self.G.add_node(nodo)



    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        for u, v, data in self.G.edges(data=True):
            peso = data['weight']
            if peso < self.peso_min:
                self.peso_min = peso
            elif peso > self.peso_max:
                self.peso_max = peso
        return self.peso_min, self.peso_max

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        minori = 0
        maggiori = 0
        try:
            if soglia <= self.peso_max and soglia >= self.peso_min:
                for u, v, data in self.G.edges(data=True):
                    peso = data['weight']
                    if peso < soglia:
                        minori += 1
                    elif peso > soglia:
                        maggiori += 1
            return minori, maggiori
        except TypeError:
            return soglia


    """Implementare la parte di ricerca del cammino minimo"""
    # TODO

    def trova_cammino_minimo(self, soglia):
        grafo = nx.Graph()
        cammino_minimo = []
        peso = float('inf')
        for u, v, data in self.G.edges(data=True):
            peso = data['weight']
            if peso > soglia:
                grafo.add_edge(u, v, weight=peso)
        for nodo in grafo.nodes():
            visitati = set()
            cammino_attuale, peso_attuale = self.ricorsione(grafo, nodo, visitati, peso, cammino_minimo, [nodo], 0)
            if len(cammino_attuale) >= 3 and peso_attuale < peso:
                peso = peso_attuale
                cammino_minimo = cammino_attuale
        if peso == float('inf'):
            peso = None
        sentieri = []
        for i in range(len(cammino_minimo) - 1):
            nodo_iniziale = cammino_minimo[i]
            nodo_fine = cammino_minimo[i + 1]
            peso_arco = grafo[nodo_iniziale][nodo_fine]['weight']
            sentieri.append({"inizio": nodo_iniziale, "fine": nodo_fine, "peso": peso_arco})
        return sentieri


    def ricorsione(self, grafo, nodo, visitati, peso, cammino_minimo, cammino_attuale, peso_attuale):
        visitati.add(nodo)
        if len(cammino_attuale)>=3 and peso_attuale < peso:
            peso = peso_attuale
            cammino_minimo = list(cammino_attuale)

        for vicino in grafo.neighbors(nodo):
            if vicino not in visitati:
                peso_arco = grafo[nodo][vicino]['weight']
                peso_attuale += peso_arco
                if peso_attuale < peso:
                    cammino_attuale.append(vicino)
                    cammino_minimo, peso = self.ricorsione(grafo, vicino, visitati, peso, cammino_minimo, cammino_attuale, peso_attuale)
                    cammino_attuale.pop()
        visitati.remove(nodo)
        return cammino_minimo, peso




