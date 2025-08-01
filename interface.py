import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkcalendar import DateEntry
from  api import MoedaAPI
from manager import CotacaoManager

class InterfaceCotacoes:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.api = MoedaAPI()
        self.manager = CotacaoManager(self.api)
        self.var_caminho_arquivo = tk.StringVar()
        self._contruir_interface()



    def _contruir_interface(self):
        self.root.title("Cotação Moedas")

        # Widgets - moeda específica
        tk.Label(self.root, text="Cotação moeda específica", borderwidth=2, relief='solid').grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='nswe')

        tk.Label(self.root, text="Selecionar moeda:", anchor='e').grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nswe')
        self.combobox_selecionar_moeda = ttk.Combobox(self.root, values=self.api.moedas)
        self.combobox_selecionar_moeda.grid(row=1, column=2, padx=10, pady=10, sticky='nswe')

        tk.Label(self.root, text="Selecionar dia:", anchor='e').grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nswe')
        self.calendario_moeda_especifica = DateEntry(self.root, year=2025, locale='pt_BR')
        self.calendario_moeda_especifica.grid(row=2, column=2, padx=10, pady=10, sticky='nswe')

        self.label_cotacao_moeda = tk.Label(self.root, text="", anchor='w')
        self.label_cotacao_moeda.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nswe')

        tk.Button(self.root, text="Consultar Cotação", command=self.evento_pegar_cotacao).grid(row=3, column=2, padx=10, pady=10, sticky='nswe')

        # Widgets - múltiplas moedas
        tk.Label(self.root, text="Cotação múltiplas moedas", borderwidth=2, relief='solid').grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky='nswe')

        tk.Label(self.root, text="Selecionar arquivo Excel com moedas (coluna A):").grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='nswe')
        tk.Button(self.root, text="Selecionar Arquivo", command=self.evento_selecionar_arquivo).grid(row=5, column=2, padx=10, pady=10, sticky='nswe')
        self.label_arquivo_selecionado = tk.Label(self.root, text="Nenhum arquivo selecionado")
        self.label_arquivo_selecionado.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky='nswe')

        tk.Label(self.root, text="Data Inicial:").grid(row=7, column=0, padx=10, pady=10, sticky='nswe')
        self.calendario_data_inicial = DateEntry(self.root, year=2025, locale='pt_BR')
        self.calendario_data_inicial.grid(row=7, column=1, padx=10, pady=10, sticky='nswe')

        tk.Label(self.root, text="Data Final:").grid(row=8, column=0, padx=10, pady=10, sticky='nswe')
        self.calendario_data_final = DateEntry(self.root, year=2025, locale='pt_BR')
        self.calendario_data_final.grid(row=8, column=1, padx=10, pady=10, sticky='nswe')

        self.label_atualizar_cotacoes = tk.Label(self.root, text="")
        self.label_atualizar_cotacoes.grid(row=9, column=1, columnspan=2, padx=10, pady=10, sticky='nswe')
        tk.Button(self.root, text="Consultar Cotações e Gerar arquivo Excel", command=self.evento_atualizar_cotacoes).grid(row=9, column=0, padx=10, pady=10, sticky='nswe')

        tk.Button(self.root, text="Fechar", command=self.root.quit).grid(row=10, column=2, padx=10, pady=10, sticky='nswe')

    def evento_pegar_cotacao(self):
        moeda = self.combobox_selecionar_moeda.get()
        data = self.calendario_moeda_especifica.get()
        valor = self.api.get_cotacao_por_dia(moeda, data)
        if valor:
            self.label_cotacao_moeda['text'] = f"Cotação de {moeda} em {data}: R$ {valor:.2f}"
        else:
            self.label_cotacao_moeda["text"] = "Erro ao buscar cotação."

    def evento_selecionar_arquivo(self):
        caminho = askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
        if caminho:
            self.var_caminho_arquivo.set(caminho)
            self.label_arquivo_selecionado['text'] = f"Arquivo Selecionado: {caminho}"

    def evento_atualizar_cotacoes(self):
        moedas = self.manager.carregar_excel_moedas(self.var_caminho_arquivo.get())
        data_inicial = self.calendario_data_inicial.get()
        data_final = self.calendario_data_final.get()
        if moedas:
            nome_arquivo = self.manager.gerar_arquivo_cotacoes(moedas, data_inicial, data_final)
            self.label_atualizar_cotacoes['text'] = f"Arquivo gerado: {nome_arquivo}"
        else:
            self.label_atualizar_cotacoes['text'] = "Erro ao ler moedas. Verifique o arquivo."
