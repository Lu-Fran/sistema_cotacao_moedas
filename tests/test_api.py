import pytest
from unittest.mock import patch
from model.moeda_api import MoedaAPI
from tests.mocks.fake_cotacoes import fake_cotacao_por_dia_response, fake_cotacoes_intervalo_response
from tests.mocks.fake_lista_moedas import fake_lista_moedas

@pytest.fixture
def api():
    return MoedaAPI()

@patch('model.moeda_api.requests.get')
def test_lista_moedas(mock_get, api):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {moeda: {} for moeda in fake_lista_moedas()}

    moedas = api.get_lista_moedas()
    assert isinstance(moedas, list)
    assert "USD" in moedas

@patch("model.moeda_api.requests.get")
def test_cotacao_por_dia(mock_get, api):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = fake_cotacao_por_dia_response()

    data = "31/07/2025"
    valor = api.get_cotacao_por_dia("USD", data)
    assert  valor == 5.60

@patch("model.moeda_api.requests.get")
def test_cotacoes_intervalo(mock_get, api):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = fake_cotacoes_intervalo_response()

    dados = api.get_cotacoes_intervalo("USD", "31/07/2025", "02/08/2025")
    assert  isinstance(dados, list)
    assert  len(dados) == 3

