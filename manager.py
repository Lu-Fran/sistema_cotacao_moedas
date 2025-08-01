import pandas as pd
import numpy as np
from datetime import datetime

class CotacaoManager:

    def __init__(self, api):
        self.api = api

    def carregar_excel_moedas(self, caminho: str):
        try:
            df = pd.read_excel(caminho)
            return df.iloc[:, 0].tolist()
        except Exception:
            return []

    def gerar_arquivo_cotacoes(self, moedas, data_inicial: str, data_final: str, arquivo_saida: str=None):
        df = pd.DataFrame({'Moeda': moedas})

        for moeda in moedas:
            cotacoes = self.api.get_cotacoes_intervalo(moeda, data_inicial, data_final)
            for cotacao in cotacoes:
                data = datetime.fromtimestamp(int(cotacao['timestamp'])).strftime('%d/%m/%Y')
                bid = float(cotacao['bid'])
                if data not in df.columns:
                    df[data] = np.nan
                df.loc[df['Moeda'] == moeda, data] = bid

        nome_arquivo = arquivo_saida or f'Cotações_{data_inicial.replace("/", "-")}_a_{data_final.replace("/", "-")}.xlsx'
        df.to_excel(nome_arquivo, index=False)
        return nome_arquivo
