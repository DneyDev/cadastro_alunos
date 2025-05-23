# config.py

import os

# --- Configurações do Banco de Dados ---

# Tipo de banco de dados (pode ser expandido para 'mysql' futuramente)
DB_TYPE = "sqlite"

# Nome do arquivo do banco de dados SQLite
SQLITE_DB_FILENAME = "cadastro_escolar.db"

# --- Caminhos do Projeto ---

# Diretório base do projeto (onde este arquivo config.py está)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho completo para o arquivo do banco de dados SQLite
# Garante que o banco seja criado/acessado no mesmo diretório do projeto
DB_PATH = os.path.join(BASE_DIR, SQLITE_DB_FILENAME)

# --- Configurações da Interface (Opcional) ---

APP_TITLE = "Sistema de Cadastro Escolar Modular"
INITIAL_GEOMETRY = "800x600"

# --- Outras Configurações ---

# Exemplo: Nível de log, chaves de API (se aplicável), etc.
LOG_LEVEL = "INFO"

# Bloco para teste (opcional)
if __name__ == '__main__':
    print(f"Tipo de Banco: {DB_TYPE}")
    print(f"Caminho do Banco: {DB_PATH}")
    print(f"Diretório Base: {BASE_DIR}")
    print(f"Título da Aplicação: {APP_TITLE}")

