# main.py
import tkinter as tk
from gerenciador_contas_app import GerenciadorContasApp

if __name__ == "__main__":
    root = tk.Tk()
    app = GerenciadorContasApp(root)
    root.mainloop()
