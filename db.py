import sqlite3
import os
import config # Importa as configurações globais

# Usa o caminho do banco definido em config.py
DB_PATH = config.DB_PATH

def conectar_bd():
    """Conecta ao banco de dados SQLite usando o caminho de config."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.Error as e:
        print(f"Erro de Banco de Dados: Não foi possível conectar ao banco de dados ({DB_PATH}): {e}")
        return None

def criar_tabelas():
    """Cria as tabelas 'turma' e 'aluno' se não existirem."""
    conn = conectar_bd()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS turma (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            ano INTEGER NOT NULL
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS aluno (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE,
            turma_id INTEGER,
            FOREIGN KEY (turma_id) REFERENCES turma (id) ON DELETE SET NULL
        )
        ''')
        conn.commit()
        print(f"Tabelas verificadas/criadas com sucesso em {DB_PATH}.")
        return True
    except sqlite3.Error as e:
        print(f"Erro ao Criar Tabelas: {e}")
        return False
    finally:
        if conn:
            conn.close()

# --- Funções CRUD para Turma ---
def inserir_turma(nome, ano):
    """Insere uma nova turma. Retorna True em sucesso, False em erro."""
    conn = conectar_bd()
    if conn is None: return False
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO turma (nome, ano) VALUES (?, ?)", (nome, ano))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Erro de Integridade: A turma '{nome}' já existe.")
        return False
    except sqlite3.Error as e:
        print(f"Erro ao Inserir Turma: {e}")
        return False
    finally:
        if conn: conn.close()

def listar_turmas():
    """Retorna uma lista de tuplas (id, nome, ano) ou [] em erro."""
    conn = conectar_bd()
    if conn is None: return []
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nome, ano FROM turma ORDER BY nome")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao Listar Turmas: {e}")
        return []
    finally:
        if conn: conn.close()

def listar_turmas_dict():
    """Retorna um dicionário {id: 'nome (ano)'} ou {} em erro."""
    turmas_list = listar_turmas()
    turmas_dict = {0: "(Nenhuma Turma)"} # Opção para desassociar aluno
    for turma in turmas_list:
        turmas_dict[turma[0]] = f"{turma[1]} ({turma[2]})"
    return turmas_dict

def excluir_turma(id_turma):
    """Exclui uma turma pelo ID. Retorna True em sucesso, False em erro."""
    conn = conectar_bd()
    if conn is None: return False
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM turma WHERE id = ?", (id_turma,))
        if cursor.fetchone() is None:
            print("Turma não encontrada para exclusão.")
            return False
        cursor.execute("DELETE FROM turma WHERE id = ?", (id_turma,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao Excluir Turma: {e}")
        return False
    finally:
        if conn: conn.close()

# --- Funções CRUD para Aluno ---
def inserir_aluno(nome, email, turma_id):
    """Insere um novo aluno. Retorna True em sucesso, False em erro."""
    conn = conectar_bd()
    if conn is None: return False
    cursor = conn.cursor()
    db_turma_id = turma_id if turma_id != 0 else None
    try:
        cursor.execute("INSERT INTO aluno (nome, email, turma_id) VALUES (?, ?, ?)", (nome, email, db_turma_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed: aluno.email' in str(e):
             print(f"Erro de Integridade: O email '{email}' já está cadastrado.")
        else:
             print(f"Erro de Integridade não esperado: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Erro ao Inserir Aluno: {e}")
        return False
    finally:
        if conn: conn.close()

def listar_alunos():
    """Retorna lista de tuplas (id, nome, email, nome_turma) ou [] em erro."""
    conn = conectar_bd()
    if conn is None: return []
    cursor = conn.cursor()
    try:
        # Ajustado para incluir o ano da turma na listagem de alunos para clareza
        cursor.execute("""
        SELECT a.id, a.nome, a.email, 
               COALESCE(t.nome || ' (' || t.ano || ')', '(Sem Turma)') as nome_turma
        FROM aluno a
        LEFT JOIN turma t ON a.turma_id = t.id
        ORDER BY a.nome
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao Listar Alunos: {e}")
        return []
    finally:
        if conn: conn.close()

def excluir_aluno(id_aluno):
    """Exclui um aluno pelo ID. Retorna True em sucesso, False em erro."""
    conn = conectar_bd()
    if conn is None: return False
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM aluno WHERE id = ?", (id_aluno,))
        if cursor.fetchone() is None:
            print("Aluno não encontrado para exclusão.")
            return False
        cursor.execute("DELETE FROM aluno WHERE id = ?", (id_aluno,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao Excluir Aluno: {e}")
        return False
    finally:
        if conn: conn.close()

# Bloco para teste direto do módulo (opcional)
if __name__ == '__main__':
    print(f"Verificando/Criando banco de dados em: {DB_PATH}")
    if criar_tabelas():
        print("\nTeste de inserção de turma:")
        inserir_turma("Teste 101", 2025)
        inserir_turma("Teste 102", 2025)
        print("\nListando turmas:")
        print(listar_turmas())
        print("\nListando turmas dict:")
        print(listar_turmas_dict())
    else:
        print("Falha ao inicializar o banco de dados.")

