import pytest
import pandas as pd
from model.moeda_api import MoedaAPI
from controller.manager import CotacaoManager
from unittest.mock import patch
from tests.mocks.fake_cotacoes import fake_cotacoes_intervalo_response

@pytest.fixture
def manager():
    api = MoedaAPI()
    return CotacaoManager(api)

def test_carregar_excel_moedas(manager, tmp_path):
    # cria Excel temporário
    file_path = tmp_path / "moedas.xlsx"
    df = pd.DataFrame({"Moeda": ["USD", "EUR"]})
    df.to_excel(file_path, index=False)

    moedas = manager.carregar_moedas_do_excel(str(file_path))
    assert moedas == ["USD", "EUR"]

@patch("model.moeda_api.requests.get")
def test_gerar_arquivo_cotacoes(mock_get, manager, tmp_path):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = fake_cotacoes_intervalo_response()

    moedas = ["USD"]
    arquivo_saida = tmp_path / "cotacoes.xlsx"
    path = manager.gerar_excel_cotacoes(moedas, "31/07/2025", "02/08/2025", str(arquivo_saida))

    df = pd.read_excel(path)
    assert not df.empty
    assert "Moedas" in df.columns or "01/08/2025" in df.columns


