import requests
from  datetime import datetime

class MoedaAPI:

    def __init__(self, url_base="https://economia.awesomeapi.com.br/json"):
        self.url_base = url_base

    def get_lista_moedas(self):
        try:
            response = requests.get(f'{self.url_base}/all')
            response.raise_for_status()
            return  list(response.json().keys())
        except requests.RequestException:
            return []

    def get_cotacao_por_dia(self, moeda: str, data: str):
        dia, mes, ano = data[:2], data[3:5], data[6:]
        url = f'{self.url_base}/daily/{moeda}-BRL/?start_date={ano}{mes}{dia}&end_date={ano}{mes}{dia}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            dados = response.json()
            return float(dados[0]['bid']) if dados else None
        except requests.RequestException:
            return None

    def get_cotacoes_intervalo(self, moeda: str, data_inicio: str, data_fim: str):
        try:
            di = datetime.strptime(data_inicio, "%d/%m/%Y").date()
            df = datetime.strptime(data_fim, "%d/%m/%Y").date()
            dias = (df - di).days + 1
            if dias <= 0:
                return []
            url = f"{self.url_base}/daily/{moeda}-BRL/{dias}?start_date={di.strftime('%Y%m%d')}&end_date={df.strftime('%Y%m%d')}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError):
            return []

