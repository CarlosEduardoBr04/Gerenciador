# gerenciador_contas_app.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import sqlite3
from conta import Conta

class GerenciadorContasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Contas")
        self.root.geometry("800x300")  # Ajustei a resolução

        self.conn = sqlite3.connect('contas.db')
        self.c = self.conn.cursor()

        self.c.execute('''
            CREATE TABLE IF NOT EXISTS contas (
                user_id INTEGER PRIMARY KEY,
                email TEXT,
                senha TEXT,
                observacao TEXT
            )
        ''')
        self.conn.commit()

        self.style = ttk.Style()
        self.style.configure("Treeview", font=('Arial', 10))
        self.style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))

        self.tree = ttk.Treeview(root, columns=("ID", "Email", "Senha", "Observação"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Senha", text="Senha")
        self.tree.heading("Observação", text="Observação")

        # Ajustando o alinhamento das colunas para o centro
        for col in ("ID", "Email", "Senha", "Observação"):
            self.tree.column(col, anchor="center")

        self.tree.pack(pady=10)

        self.frame_botoes = tk.Frame(root)
        self.frame_botoes.pack(pady=10)

        self.btn_adicionar = ttk.Button(self.frame_botoes, text="Adicionar Conta", command=self.adicionar_conta)
        self.btn_adicionar.pack(side="left", padx=5)

        self.btn_editar = ttk.Button(self.frame_botoes, text="Editar Conta", command=self.editar_conta)
        self.btn_editar.pack(side="left", padx=5)

        self.btn_remover = ttk.Button(self.frame_botoes, text="Remover Conta(s)", command=self.remover_contas)
        self.btn_remover.pack(side="left", padx=5)

        self.btn_selecionar_todas = ttk.Button(self.frame_botoes, text="Selecionar Todas", command=self.selecionar_todas)
        self.btn_selecionar_todas.pack(side="left", padx=5)

        self.btn_exportar_txt = ttk.Button(self.frame_botoes, text="Exportar para TXT", command=self.exportar_para_txt)
        self.btn_exportar_txt.pack(side="left", padx=5)

        self.btn_importar_txt = ttk.Button(self.frame_botoes, text="Importar do TXT", command=self.importar_do_txt)
        self.btn_importar_txt.pack(side="left", padx=5)

        self.atualizar_lista_contas()

    def adicionar_conta(self):
        novo_email = simpledialog.askstring("Adicionar Conta", "Digite o e-mail:")
        nova_senha = simpledialog.askstring("Adicionar Conta", "Digite a senha:")
        observacao = simpledialog.askstring("Adicionar Conta", "Digite a observação:")

        if novo_email and nova_senha:
            self.c.execute('''
                INSERT INTO contas (email, senha, observacao) VALUES (?, ?, ?)
            ''', (novo_email, nova_senha, observacao))
            self.conn.commit()
            self.atualizar_lista_contas()
            messagebox.showinfo("Sucesso", "Conta adicionada com sucesso.")

    def editar_conta(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Nenhuma Conta Selecionada", "Selecione uma conta para editar.")
            return

        user_id = self.tree.item(item_selecionado, "values")[0]

        novo_email = simpledialog.askstring("Editar Conta", "Digite o novo e-mail:")
        nova_senha = simpledialog.askstring("Editar Conta", "Digite a nova senha:")
        observacao = simpledialog.askstring("Editar Conta", "Digite a nova observação:")

        if novo_email and nova_senha:
            self.c.execute('''
                UPDATE contas SET email=?, senha=?, observacao=? WHERE user_id=?
            ''', (novo_email, nova_senha, observacao, user_id))
            self.conn.commit()
            self.atualizar_lista_contas()
            messagebox.showinfo("Sucesso", "Conta editada com sucesso.")

    def remover_contas(self):
        items_selecionados = self.tree.selection()
        if not items_selecionados:
            messagebox.showwarning("Nenhuma Conta Selecionada", "Selecione uma conta para remover.")
            return

        for item_selecionado in items_selecionados:
            user_id = self.tree.item(item_selecionado, "values")[0]
            self.c.execute('''
                DELETE FROM contas WHERE user_id=?
            ''', (user_id,))
        
        self.conn.commit()
        self.atualizar_lista_contas()
        messagebox.showinfo("Sucesso", "Conta(s) removida(s) com sucesso.")

    def selecionar_todas(self):
        self.tree.selection_set(self.tree.get_children())

    def exportar_para_txt(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt")])

        if file_path:
            with open(file_path, "w") as file:
                # Escrever cabeçalho
                file.write("ID, Email, Senha, Observação\n")

                for row in self.c.execute('SELECT * FROM contas'):
                    # Escrever dados no formato CSV
                    file.write(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}\n")

    def importar_do_txt(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt")])

        if file_path:
            with open(file_path, "r") as file:
                # Ignorar cabeçalho
                next(file)

                for line in file:
                    data = line.strip().split(", ")
                    if len(data) == 4:
                        self.c.execute('''
                            INSERT INTO contas (email, senha, observacao) VALUES (?, ?, ?)
                        ''', (data[1], data[2], data[3]))
        
            self.conn.commit()
            self.atualizar_lista_contas()
            messagebox.showinfo("Sucesso", "Dados importados com sucesso.")

    def atualizar_lista_contas(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.c.execute('SELECT * FROM contas'):
            conta = Conta(*row)
            self.tree.insert("", "end", values=(conta.user_id, conta.email, conta.senha, conta.observacao))

if __name__ == "__main__":
    root = tk.Tk()
    app = GerenciadorContasApp(root)
    root.mainloop()
