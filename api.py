import requests
from datetime import datetime, date

class MoedaAPI:

    def __init__(self):
        self.url_base = "https://economia.awesomeapi.com.br/json"
        self.moedas = self.get_lista_moedas()

    def get_lista_moedas(self):
        try:
            response = requests.get(f'{self.url_base}/all')
            response.raise_for_status()
            data = response.json()
            return list(data.keys())
        except requests.RequestException:
            return []

    def get_cotacao_por_dia(self, moeda: str, data: str):
        dia, mes, ano = data[:2], data[3:5], data[6:]
        url = f'{self.url_base}/daily/{moeda}-BRL/?start_date={ano}{mes}{dia}&end_date={ano}{mes}{dia}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            dados = response.json()
            if dados:
                return float(dados[0]['bid'])
        except requests.RequestException:
            pass
        return None

    def get_cotacoes_intervalo(self, moeda: str, data_inicio: str, data_fim: str):
        di = datetime.strptime(data_inicio, "%d/%m/%Y").date()
        df = datetime.strptime(data_fim, "%d/%m/%Y").date()
        dias = abs((df - di).days)

        url = f"{self.url_base}/daily/{moeda}-BRL/{dias}?start_date={di.strftime('%Y%m%d')}&end_date={df.strftime('%Y%m%d')}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return []
