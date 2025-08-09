import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkcalendar import DateEntry
from controller.manager import CotacaoManager
from model.moeda_api import MoedaAPI

class InterfaceCotacoes:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Cotação de Moedas")

        self.api = MoedaAPI()
        self.manager = CotacaoManager(self.api)
        self.moedas_disponiveis = self.api.get_lista_moedas()
        self.var_arquivo = tk.StringVar()

        self._montar_interface()

    def _montar_interface(self):
        # Seção: Cotacao individual
        ttk.Label(self.root, text="Cotacao Individual", relief="ridge").grid(row=0, column=0, columnspan=3, sticky='ew', pady=5)
        ttk.Label(self.root, text="Moeda:").grid(row=1, column=0)
        self.combo_moeda = ttk.Combobox(self.root, values=self.moedas_disponiveis)
        self.combo_moeda.grid(row=1, column=1, columnspan=2, sticky='ew')

        ttk.Label(self.root, text="Data:").grid(row=2, column=0)
        self.data_unica = DateEntry(self.root, locale='pt_BR')
        self.data_unica.grid(row=2, column=1, sticky='ew')
        ttk.Button(self.root, text="Buscar", command=self.pegar_cotacao).grid(row=2, column=2, padx=5)

        self.resultado_cotacao = ttk.Label(self.root, text="")
        self.resultado_cotacao.grid(row=3, column=0, columnspan=3, sticky='w', pady=5)

        # Seção: Arquivo
        ttk.Label(self.root, text="Excel de Moedas (Coluna A)", relief="ridge").grid(row=4, column=0, columnspan=3, sticky='ew', pady=5)
        ttk.Button(self.root, text="Selecionar Arquivo", command=self.selecionar_arquivo).grid(row=5, column=0, sticky='w')
        self.label_arquivo = ttk.Label(self.root, text="Nenhum arquivo")
        self.label_arquivo.grid(row=5, column=1, columnspan=2, sticky='w')

        ttk.Label(self.root, text="Data Inicial:").grid(row=6, column=0)
        self.data_inicio = DateEntry(self.root, locale='pt_BR')
        self.data_inicio.grid(row=6, column=1)

        ttk.Label(self.root, text="Data Final:").grid(row=7, column=0)
        self.data_fim = DateEntry(self.root, locale='pt_BR')
        self.data_fim.grid(row=7, column=1)

        ttk.Button(self.root, text="Cotar Moedas do arquivo e Gerar Novo Excel", command=self.gerar_excel).grid(row=8, column=0, columnspan=3, sticky='ew')
        self.resultado_excel = ttk.Label(self.root, text="")
        self.resultado_excel.grid(row=9, column=0, columnspan=3, sticky='w')

    def pegar_cotacao(self):
        moeda = self.combo_moeda.get()
        data = self.data_unica.get()
        valor = self.manager.obter_cotacao_individual(moeda, data)
        self.resultado_cotacao['text'] = f"R$ {valor:.2f}" if valor else "Erro na consulta."

    def selecionar_arquivo(self):
        caminho = askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if caminho:
            self.var_arquivo.set(caminho)
            self.label_arquivo['text'] = caminho

    def gerar_excel(self):
        moedas = self.manager.carregar_moedas_do_excel(self.var_arquivo.get())
        if not moedas:
            self.resultado_excel['text'] = "Erro: Arquivo inválido ou vazio."
            return
        try:
            arquivo = self.manager.gerar_excel_cotacoes(moedas, self.data_inicio.get(), self.data_fim.get())
            self.resultado_excel['text'] = f"Arquivo gerado com sucesso: {arquivo}"
        except Exception as e:
            self.resultado_excel['text'] = f"Erro ao gerar Excel: {str(e)}"

