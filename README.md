# 💱 Sistema de Cotação de Moedas — RPA em Python

Sistema **RPA em Python** para consulta automática de cotações de moedas via API, com histórico, interface gráfica e geração de relatórios.
O projeto é uma **evolução arquitetural**: partiu de um nível inicial de POO (Nível 2) para um design **MVC** completo (Nível 4), com **testes automatizados e mocks**.

---

## 📜 Linha do Tempo da Evolução

| Data        | Versão     | Nível Arquitetural | Principais Características                                                                                      |
| ----------- | ---------- | ------------------ | --------------------------------------------------------------------------------------------------------------- |
| **2025-08-01** | `versao-2` | **Nível 2** — POO  | Classes e métodos organizados, interface simples, sem testes automatizados.                                     |
| **2025-08-09** | `main`     | **Nível 4** — MVC  | Separação Model-View-Controller, testes automatizados com `pytest`, mocks, código mais escalável e manutenível. |

---

## 🛠 Tecnologias Utilizadas

* **Linguagem**: Python 3.13
* **Bibliotecas**:

  * Requests (consumo da API de cotações)
  * Pandas & OpenPyXL (manipulação de planilhas)
  * Tkinter & TkCalendar (interface gráfica)
  * Pytest & Mocks (testes automatizados)
* **Arquitetura**: MVC (Model, View, Controller)

---

## 📂 Estrutura da Versão Atual (`main` - Nível 4)
sistema_cotacao_moedas_MVC/
├── main.py
├── model/
│ └── moeda_api.py
├── controller/
│ └── manager.py
├── view/
│ └── interface.py
├── tests/
│ ├── init.py
│ ├── mocks/
│ │ ├── init.py
│ │ ├── fake_cotacoes.py
│ │ └── fake_lista_moedas.py
│ ├── test_api.py
│ └── test_manager.py

---

## 📌 Como Executar
```bash
# Clonar o repositório
git clone https://github.com/Lu-Fran/sistema_cotacao_moedas.git

# Entrar no diretório
cd sistema_cotacao_moedas

# Criar e ativar o ambiente virtual (opcional, mas recomendado)
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar
python main.py

✅ Testes Automatizados
pytest -v

