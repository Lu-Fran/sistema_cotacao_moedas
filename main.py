import tkinter as tk
from view.interface import InterfaceCotacoes

def main():
    root = tk.Tk()
    app = InterfaceCotacoes(root)
    root.mainloop()

if __name__ == '__main__':
    main()

