import tkinter as tk
from tkinter import ttk

# Importa módulos refatorados
import config
import db
import menu
from turma import TelaTurma
from aluno import TelaAluno
# A TelaAjuda está agora dentro do módulo menu
from menu import TelaAjuda

# --- Tela Inicial Simples ---
class TelaInicio(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Bem-vindo ao Sistema de Cadastro Escolar!", 
                          font=("Arial", 18))
        label.pack(pady=20, padx=20)
        ttk.Label(self, text="Utilize o menu superior para navegar entre os módulos.").pack(pady=10)

# --- Classe Principal da Aplicação ---
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configurações da janela principal (do config.py)
        self.title(config.APP_TITLE)
        self.geometry(config.INITIAL_GEOMETRY)

        # Garante que o banco de dados e tabelas existam
        if not db.criar_tabelas():
            # Poderia mostrar um erro fatal aqui e fechar, mas db.py já imprime o erro
            print("Erro crítico: Não foi possível inicializar o banco de dados. Saindo.")
            self.destroy() # Fecha a aplicação se o DB falhar
            return

        # Cria o menu principal usando a função do módulo menu
        menu.criar_menu_principal(self)

        # Container principal para os frames (telas)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Define as telas que serão gerenciadas
        # Usando os nomes das classes como chave para consistência
        telas_para_criar = (TelaInicio, TelaTurma, TelaAluno, TelaAjuda)

        for F in telas_para_criar:
            page_name = F.__name__ # Ex: "TelaTurma"
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Mostra a tela inicial
        self.show_frame("TelaInicio")

    def show_frame(self, page_name):
        """Mostra um frame (tela) específico."""
        frame = self.frames.get(page_name)
        if frame:
            # Chama o método update_content se existir, para atualizar dados
            if hasattr(frame, "update_content") and callable(frame.update_content):
                try:
                    frame.update_content()
                except Exception as e:
                    print(f"Erro ao chamar update_content em {page_name}: {e}")
            frame.tkraise()
        else:
            print(f"Erro: Frame 	'{page_name}	' não encontrado.")

    def atualizar_telas_dependentes(self, origem):
        """Chamado por uma tela (ex: Turma) para notificar outras (ex: Aluno) sobre mudanças."""
        print(f"Atualização solicitada por: {origem}")
        if origem == "turma":
            # Se a tela de Aluno já foi criada e está no dicionário
            if "TelaAluno" in self.frames:
                aluno_frame = self.frames["TelaAluno"]
                # Verifica se o método existe antes de chamar
                if hasattr(aluno_frame, "atualizar_combobox_turmas") and callable(aluno_frame.atualizar_combobox_turmas):
                    print("Atualizando combobox de turmas na tela de Alunos...")
                    aluno_frame.atualizar_combobox_turmas()
                # Pode ser necessário atualizar a lista de alunos também, se a exibição da turma mudou
                if hasattr(aluno_frame, "atualizar_lista_alunos") and callable(aluno_frame.atualizar_lista_alunos):
                     print("Atualizando lista de alunos...")
                     aluno_frame.atualizar_lista_alunos()
        # Adicionar outras lógicas de dependência se necessário

# --- Ponto de Entrada Principal ---
if __name__ == "__main__":
    app = App()
    # Verifica se a inicialização falhou (ex: erro no DB)
    if app.winfo_exists(): # Checa se a janela foi criada
        app.mainloop()

