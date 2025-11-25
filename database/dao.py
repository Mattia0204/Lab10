from database.DB_connect import DBConnect
from model.spedizione import Spedizione
from model.hub import Hub
from model.compagnia import Compagnia

class DAO:

    @staticmethod
    def get_spedizione() -> dict[str, Spedizione] | None:

        cnx = DBConnect.get_connection()
        result = {}

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM spedizione"
        try:
            cursor.execute(query)
            for row in cursor:
                spedizione = Spedizione(
                    id=row["id"],
                    id_compagnia=row["id_compagnia"],
                    numero_tracking=row["numero_tracking"],
                    id_hub_origine=row["id_hub_origine"],
                    id_hub_destinazione=row["id_hub_destinazione"],
                    data_ritiro_programmata=row["data_ritiro_programmata"],
                    distanza=row["distanza"],
                    data_consegna=row["data_consegna"],
                    valore_merce=row["valore_merce"]
                )
                result[spedizione.id] = spedizione
        except Exception as e:
            print(f"Errore durante la query get_spedizione: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def get_hub() -> dict[str, Hub] | None:

        cnx = DBConnect.get_connection()
        result = {}

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM hub"
        try:
            cursor.execute(query)
            for row in cursor:
                hub = Hub(
                    id=row["id"],
                    codice=row["codice"],
                    nome=row["nome"],
                    citta=row["citta"],
                    stato=row["stato"],
                    latitudine=row["latitudine"],
                    longitudine=row["longitudine"]
                )
                result[hub.id] = hub
        except Exception as e:
            print(f"Errore durante la query get_hub: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def get_compagnia() -> dict[str, Compagnia] | None:

        cnx = DBConnect.get_connection()
        result = {}

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM compagnia"
        try:
            cursor.execute(query)
            for row in cursor:
                compagnia = Compagnia(
                    id=row["id"],
                    codice=row["codice"],
                    nome=row["nome"],
                )
                result[compagnia.id] = compagnia
        except Exception as e:
            print(f"Errore durante la query get_compagnia: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result