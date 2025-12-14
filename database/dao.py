from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    def getRifugio(self):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM rifugio"
        cursor.execute(query)
        for row in cursor:
            rifugio = Rifugio(row["id"], row["nome"], row["localita"],
                              row["altitudine"], row["capienza"], row["aperto"])
            result.append(rifugio)
        cursor.close()
        conn.close()
        return result

    def getConnessione(self):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione"
        cursor.execute(query)
        for row in cursor:
            connessione = Connessione(row["id"], row["id_rifugio1"], row["id_rifugio2"], row["distanza"],
                                      row["difficolta"], row["durata"], row["anno"])
            result.append(connessione)
        cursor.close()
        conn.close()
        return result


    def getGrafo(self, year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT id_rifugio1, id_rifugio2, distanza, difficolta
                    FROM connessione
                    WHERE anno <= %s"""
        cursor.execute(query, (year,))
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result

