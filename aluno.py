import tkinter as tk
from tkinter import ttk, messagebox
import db # Importa o módulo db.py refatorado
import os # Para o teste __main__

class TelaAluno(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.turmas_map = {} # Mapeia nome exibido no combobox para ID da turma

        # --- Frame para Formulário --- 
        form_frame = ttk.LabelFrame(self, text="Cadastrar Novo Aluno")
        form_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(form_frame, text="Nome do Aluno:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome_aluno = ttk.Entry(form_frame, width=40)
        self.entry_nome_aluno.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_email_aluno = ttk.Entry(form_frame, width=40)
        self.entry_email_aluno.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Turma:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.combo_turma_aluno = ttk.Combobox(form_frame, state="readonly", width=37)
        self.combo_turma_aluno.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        # self.atualizar_combobox_turmas() # Carrega as turmas ao iniciar (chamado pelo update_content)

        btn_cadastrar_aluno = ttk.Button(form_frame, text="Cadastrar Aluno", command=self.cadastrar_aluno)
        btn_cadastrar_aluno.grid(row=3, column=0, columnspan=2, pady=10)

        form_frame.columnconfigure(1, weight=1)

        # --- Frame para Lista e Exclusão ---
        list_frame = ttk.LabelFrame(self, text="Alunos Cadastrados")
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para exibir alunos
        self.tree_alunos = ttk.Treeview(list_frame, columns=("id", "nome", "email", "turma"), show="headings")
        self.tree_alunos.heading("id", text="ID")
        self.tree_alunos.heading("nome", text="Nome do Aluno")
        self.tree_alunos.heading("email", text="Email")
        self.tree_alunos.heading("turma", text="Turma")

        self.tree_alunos.column("id", width=50, anchor="center")
        self.tree_alunos.column("nome", width=250)
        self.tree_alunos.column("email", width=250)
        self.tree_alunos.column("turma", width=150)

        scrollbar_alunos = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree_alunos.yview)
        self.tree_alunos.configure(yscrollcommand=scrollbar_alunos.set)

        self.tree_alunos.pack(side="left", fill="both", expand=True)
        scrollbar_alunos.pack(side="right", fill="y")

        btn_excluir_aluno = ttk.Button(self, text="Excluir Aluno Selecionado", command=self.excluir_aluno_selecionado)
        btn_excluir_aluno.pack(pady=5)

        # self.atualizar_lista_alunos() # Carrega alunos ao iniciar (chamado pelo update_content)
        self.update_content() # Carrega dados iniciais

    def atualizar_combobox_turmas(self):
        turmas_dict = db.listar_turmas_dict()
        self.turmas_map = {v: k for k, v in turmas_dict.items()} # Inverte para {nome: id}
        valores_combobox = list(turmas_dict.values())
        self.combo_turma_aluno["values"] = valores_combobox
        
        valor_atual = self.combo_turma_aluno.get()
        
        # Tenta manter a seleção atual se ainda for válida
        if valor_atual in valores_combobox:
            self.combo_turma_aluno.set(valor_atual)
        # Senão, seleciona "(Nenhuma Turma)" se existir
        elif "(Nenhuma Turma)" in valores_combobox:
             self.combo_turma_aluno.set("(Nenhuma Turma)")
        # Senão, seleciona a primeira opção se houver alguma
        elif valores_combobox:
             self.combo_turma_aluno.current(0)
        # Senão, limpa o combobox
        else:
             self.combo_turma_aluno.set("")

    def cadastrar_aluno(self):
        nome = self.entry_nome_aluno.get().strip()
        email = self.entry_email_aluno.get().strip()
        turma_selecionada = self.combo_turma_aluno.get()

        if not nome or not email:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha o nome e o email do aluno.")
            return
        
        if not turma_selecionada:
             messagebox.showwarning("Turma não selecionada", "Por favor, selecione uma turma para o aluno.\nSe não houver turmas, cadastre uma primeiro.")
             return

        turma_id = self.turmas_map.get(turma_selecionada, None)
        if turma_id is None:
             messagebox.showerror("Erro Interno", f"Não foi possível encontrar o ID para a turma selecionada: 	'{turma_selecionada}	'")
             return

        if db.inserir_aluno(nome, email, turma_id):
            messagebox.showinfo("Sucesso", f"Aluno 	'{nome}	' cadastrado com sucesso!")
            self.entry_nome_aluno.delete(0, tk.END)
            self.entry_email_aluno.delete(0, tk.END)
            # Reseta combobox para "(Nenhuma Turma)" se existir, senão para a primeira opção
            if "(Nenhuma Turma)" in self.combo_turma_aluno["values"]:
                self.combo_turma_aluno.set("(Nenhuma Turma)")
            elif self.combo_turma_aluno["values"]:
                 self.combo_turma_aluno.current(0)
            else:
                 self.combo_turma_aluno.set("")
            self.atualizar_lista_alunos()
        else:
            # Mensagens de erro/aviso são tratadas dentro de db.py (via print)
            messagebox.showerror("Erro", f"Não foi possível cadastrar o aluno 	'{nome}	'. Verifique se o email já existe.")

    def atualizar_lista_alunos(self):
        for i in self.tree_alunos.get_children():
            self.tree_alunos.delete(i)
        alunos = db.listar_alunos()
        for aluno in alunos:
            self.tree_alunos.insert("", tk.END, values=aluno)

    def excluir_aluno_selecionado(self):
        selected_item = self.tree_alunos.focus()
        if not selected_item:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione um aluno na lista para excluir.")
            return

        item_values = self.tree_alunos.item(selected_item, "values")
        if not item_values or len(item_values) < 2:
             messagebox.showerror("Erro", "Não foi possível obter os dados do aluno selecionado.")
             return
             
        try:
            id_aluno = int(item_values[0])
            nome_aluno = item_values[1]
        except (ValueError, IndexError):
             messagebox.showerror("Erro", "Dados inválidos para o aluno selecionado.")
             return

        confirm = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o aluno 	'{nome_aluno}	'?")
        
        if confirm:
            if db.excluir_aluno(id_aluno):
                messagebox.showinfo("Sucesso", f"Aluno 	'{nome_aluno}	' excluído com sucesso.")
                self.atualizar_lista_alunos()
            else:
                 messagebox.showerror("Erro", f"Não foi possível excluir o aluno 	'{nome_aluno}	'.")

    def update_content(self):
        """Atualiza o combobox de turmas e a lista de alunos quando o frame é exibido."""
        self.atualizar_combobox_turmas()
        self.atualizar_lista_alunos()

# Exemplo de como usar (para teste direto do módulo, se necessário)
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Teste Tela Aluno")
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
        # Adiciona uma turma para teste do combobox
        db.inserir_turma("Teste 101", 2025)
        
    app_frame = TelaAluno(root, controller)
    app_frame.pack(fill="both", expand=True)
    root.geometry("750x550")
    root.mainloop()

