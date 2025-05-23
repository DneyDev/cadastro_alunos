import tkinter as tk
from tkinter import ttk, messagebox
import db # Importa o módulo db.py refatorado

class TelaTurma(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # --- Frame para Formulário --- 
        form_frame = ttk.LabelFrame(self, text="Cadastrar Nova Turma")
        form_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(form_frame, text="Nome da Turma:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome_turma = ttk.Entry(form_frame, width=40)
        self.entry_nome_turma.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Ano:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_ano_turma = ttk.Entry(form_frame, width=10)
        self.entry_ano_turma.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        btn_cadastrar = ttk.Button(form_frame, text="Cadastrar Turma", command=self.cadastrar_turma)
        btn_cadastrar.grid(row=2, column=0, columnspan=2, pady=10)

        form_frame.columnconfigure(1, weight=1) # Faz a coluna do entry expandir

        # --- Frame para Lista e Exclusão ---
        list_frame = ttk.LabelFrame(self, text="Turmas Cadastradas")
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para exibir turmas
        self.tree_turmas = ttk.Treeview(list_frame, columns=("id", "nome", "ano"), show="headings")
        self.tree_turmas.heading("id", text="ID")
        self.tree_turmas.heading("nome", text="Nome da Turma")
        self.tree_turmas.heading("ano", text="Ano")
        
        self.tree_turmas.column("id", width=50, anchor="center")
        self.tree_turmas.column("nome", width=300)
        self.tree_turmas.column("ano", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree_turmas.yview)
        self.tree_turmas.configure(yscrollcommand=scrollbar.set)

        self.tree_turmas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        btn_excluir = ttk.Button(self, text="Excluir Turma Selecionada", command=self.excluir_turma_selecionada)
        btn_excluir.pack(pady=5)

        self.atualizar_lista_turmas()

    def cadastrar_turma(self):
        nome = self.entry_nome_turma.get().strip()
        ano_str = self.entry_ano_turma.get().strip()

        if not nome or not ano_str:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha o nome e o ano da turma.")
            return
        try:
            ano = int(ano_str)
        except ValueError:
            messagebox.showerror("Erro de Formato", "O ano deve ser um número inteiro.")
            return

        if db.inserir_turma(nome, ano):
            messagebox.showinfo("Sucesso", f"Turma 	'{nome}' cadastrada com sucesso!")
            self.entry_nome_turma.delete(0, tk.END)
            self.entry_ano_turma.delete(0, tk.END)
            self.atualizar_lista_turmas()
            # Notifica o controller para atualizar outras telas se necessário
            self.controller.atualizar_telas_dependentes("turma")
        else:
            # Mensagens de erro/aviso são tratadas dentro de db.py (via print)
            # Poderia adicionar um messagebox aqui se db.py retornasse o tipo de erro
            messagebox.showerror("Erro", f"Não foi possível cadastrar a turma 	'{nome}'. Verifique se já existe.")

    def atualizar_lista_turmas(self):
        for i in self.tree_turmas.get_children():
            self.tree_turmas.delete(i)
        turmas = db.listar_turmas()
        for turma in turmas:
            self.tree_turmas.insert("", tk.END, values=turma)

    def excluir_turma_selecionada(self):
        selected_item = self.tree_turmas.focus()
        if not selected_item:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma turma na lista para excluir.")
            return

        item_values = self.tree_turmas.item(selected_item, "values")
        # Validação extra para garantir que item_values não está vazio ou malformado
        if not item_values or len(item_values) < 2:
             messagebox.showerror("Erro", "Não foi possível obter os dados da turma selecionada.")
             return
             
        try:
            id_turma = int(item_values[0])
            nome_turma = item_values[1]
        except (ValueError, IndexError):
             messagebox.showerror("Erro", "Dados inválidos para a turma selecionada.")
             return

        confirm = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a turma 	'{nome_turma}'?\nAlunos associados a esta turma terão sua turma removida (definida como NULA).")
        
        if confirm:
            if db.excluir_turma(id_turma):
                messagebox.showinfo("Sucesso", f"Turma 	'{nome_turma}' excluída com sucesso.")
                self.atualizar_lista_turmas()
                # Notifica o controller para atualizar outras telas
                self.controller.atualizar_telas_dependentes("turma")
            else:
                 messagebox.showerror("Erro", f"Não foi possível excluir a turma 	'{nome_turma}'.")

    def update_content(self):
        """Atualiza a lista de turmas quando o frame é exibido."""
        self.atualizar_lista_turmas()

# Exemplo de como usar (para teste direto do módulo, se necessário)
if __name__ == '__main__':
    # Este código só será executado se turma.py for rodado diretamente
    # Normalmente, ele será importado e usado por main.py
    root = tk.Tk()
    root.title("Teste Tela Turma")
    # Mock controller para teste
    class MockController:
        def show_frame(self, page_name):
            print(f"Show frame: {page_name}")
        def atualizar_telas_dependentes(self, origem):
             print(f"Atualizando telas dependentes de: {origem}")

    controller = MockController()
    # Garante que o DB exista para o teste
    if not os.path.exists(db.DB_PATH):
        print("Criando banco de dados para teste...")
        db.criar_tabelas()
        
    app_frame = TelaTurma(root, controller)
    app_frame.pack(fill="both", expand=True)
    root.geometry("700x500")
    root.mainloop()

