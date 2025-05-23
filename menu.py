import tkinter as tk
from tkinter import ttk

# --- Tela de Ajuda ---
class TelaAjuda(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # --- Conteúdo da Ajuda ---
        self.label_titulo = ttk.Label(self, text="Ajuda e Créditos", font=("Arial", 16))
        self.label_titulo.pack(pady=10)

        # Usando Text widget para permitir seleção e cópia, mas desabilitado para edição
        self.text_info = tk.Text(self, wrap="word", height=15, width=70, 
                                 borderwidth=0, relief="flat", # Aparência mais limpa
                                 background=self.cget("background")) # Cor de fundo igual ao frame
        self.text_info.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Scrollbar para o Text widget, caso o conteúdo seja muito grande
        # scrollbar_ajuda = ttk.Scrollbar(self.text_info, orient="vertical", command=self.text_info.yview)
        # self.text_info.configure(yscrollcommand=scrollbar_ajuda.set)
        # scrollbar_ajuda.pack(side="right", fill="y") # Empacotar ao lado se necessário

        self.update_content() # Carrega o conteúdo inicial

     def update_content(self):
         """Atualiza o conteúdo da tela de Ajuda."""
         # Informações do projeto
         nomes_integrantes = "Sidney Rodrigues - Aluno de Ciência da Computação (3º Período)"
         titulo_projeto = "Sistema de Cadastro Escolar"
         descricao = ("Aplicação para gerenciamento de alunos e turmas.\n"
                      "Permite cadastrar, visualizar e excluir turmas.\n"
                      "Permite cadastrar, visualizar e excluir alunos, associando-os a turmas existentes.\n"
                      "Utiliza Tkinter para a interface gráfica e SQLite para o banco de dados.")

         conteudo = f"""
Título do Projeto: {titulo_projeto}

Integrantes do Grupo:
{nomes_integrantes}

Descrição da Aplicação:
{descricao}
         """

         # Atualiza o widget Text
         self.text_info.config(state="normal") # Habilita escrita temporariamente
         self.text_info.delete("1.0", tk.END) # Limpa conteúdo anterior
         self.text_info.insert("1.0", conteudo.strip()) # Insere novo conteúdo (strip para remover espaços extras)
         self.text_info.config(state="disabled") # Desabilita escrita novamente

# --- Função para criar o Menu Principal ---
def criar_menu_principal(app_controller):
    """Cria e configura a barra de menus principal da aplicação."""
    menubar = tk.Menu(app_controller) # app_controller é a instância Tk (root window)

    # Menu Navegação
    menu_navegacao = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Navegação", menu=menu_navegacao)
    # Os nomes dos frames ('TelaInicio', 'TelaTurma', etc.) serão definidos no main.py
    menu_navegacao.add_command(label="Início",
                               command=lambda: app_controller.show_frame("TelaInicio"))
    menu_navegacao.add_command(label="Cadastro de Turmas",
                               command=lambda: app_controller.show_frame("TelaTurma"))
    menu_navegacao.add_command(label="Cadastro de Alunos",
                               command=lambda: app_controller.show_frame("TelaAluno"))
    menu_navegacao.add_separator()
    menu_navegacao.add_command(label="Sair", command=app_controller.quit)

    # Menu Ajuda
    menu_ajuda = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
    menu_ajuda.add_command(label="Sobre",
                           command=lambda: app_controller.show_frame("TelaAjuda"))

    # Configura a janela principal para usar este menubar
    app_controller.config(menu=menubar)

# Exemplo de como usar (para teste direto do módulo, se necessário)
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Teste Menu e Ajuda")

    # Mock controller para teste
    class MockController(tk.Tk): # Herda de Tk para ter o método config e quit
        def __init__(self):
            super().__init__()
            self.frames = {}
            # Adiciona um frame de ajuda mock para teste
            container = tk.Frame(self)
            container.pack(fill="both", expand=True)
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)
            
            ajuda_frame = TelaAjuda(container, self)
            ajuda_frame.grid(row=0, column=0, sticky="nsew")
            self.frames["TelaAjuda"] = ajuda_frame
            
            # Adiciona outros frames mock se necessário para testar navegação
            inicio_frame = tk.Frame(container); ttk.Label(inicio_frame, text="Tela Início Mock").pack()
            inicio_frame.grid(row=0, column=0, sticky="nsew")
            self.frames["TelaInicio"] = inicio_frame
            
            turma_frame = tk.Frame(container); ttk.Label(turma_frame, text="Tela Turma Mock").pack()
            turma_frame.grid(row=0, column=0, sticky="nsew")
            self.frames["TelaTurma"] = turma_frame
            
            aluno_frame = tk.Frame(container); ttk.Label(aluno_frame, text="Tela Aluno Mock").pack()
            aluno_frame.grid(row=0, column=0, sticky="nsew")
            self.frames["TelaAluno"] = aluno_frame

            self.show_frame("TelaInicio") # Mostra frame inicial

        def show_frame(self, page_name):
            print(f"Show frame: {page_name}")
            frame = self.frames.get(page_name)
            if frame:
                if hasattr(frame, "update_content"):
                    frame.update_content()
                frame.tkraise()
            else:
                print(f"Erro: Frame '{page_name}' não encontrado.")
        
        # Método quit já existe em tk.Tk

    controller = MockController()
    criar_menu_principal(controller) # Cria o menu na janela mock
    controller.geometry("600x400")
    controller.mainloop()

