import pandas as pd
import numpy as np
from datetime import datetime

class CotacaoManager:

    def __init__(self, api):
        self.api = api

    def carregar_moedas_do_excel(self, caminho):
        try:
            df = pd.read_excel(caminho)
            if 'Moedas' in df.columns:
                return df['Moedas'].dropna().tolist()
            # Caso não tenha cabeçalho:
            return df.iloc[:, 0].dropna().tolist()
        except Exception as e:
            print(f"[ERRO] Falha ao carregar Excel: {e}")
            return []

    def gerar_excel_cotacoes(self, moedas, data_inicial, data_final, arquivo_saida=None):
        df = pd.DataFrame({"Moedas": moedas})
        for moeda in moedas:
            cotacoes = self.api.get_cotacoes_intervalo(moeda, data_inicial, data_final)
            for cotacao in cotacoes:
                data = datetime.fromtimestamp(int(cotacao['timestamp'])).strftime('%d/%m/%Y')
                bid = float(cotacao['bid'])
                if data not in df.columns:
                    df[data] = np.nan
                df.loc[df['Moedas'] == moeda, data] = bid

        nome_arquivo = arquivo_saida or f"Cotacoes_{data_inicial.replace('/', '-')}_a_{data_final.replace('/', '-')}.xlsx"
        df.to_excel(nome_arquivo, index=False)
        return nome_arquivo

    def obter_cotacao_individual(self, moeda, data):
        return self.api.get_cotacao_por_dia(moeda, data)

