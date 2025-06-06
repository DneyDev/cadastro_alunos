# Aplicação de Cadastro Escolar Modular (Tkinter + SQLite)

Esta aplicação permite o cadastro e visualização de turmas e alunos utilizando uma interface gráfica desenvolvida com Tkinter e um banco de dados SQLite, agora com uma estrutura de projeto modular.

## Requisitos

*   Python 3.x
*   Tkinter (geralmente incluído na instalação padrão do Python, mas pode precisar ser instalado separadamente em alguns sistemas Linux: `sudo apt-get install python3-tk` ou similar)

## Estrutura do Projeto

```
projeto_escola/
│
├── main.py                  # Ponto de entrada da aplicação, orquestra as telas
├── db.py                    # Funções de interação com o banco de dados (SQLite)
├── aluno.py                 # Classe da tela de cadastro e listagem de Alunos (TelaAluno)
├── turma.py                 # Classe da tela de cadastro e listagem de Turmas (TelaTurma)
├── menu.py                  # Função para criar o menu principal e classe da tela de Ajuda (TelaAjuda)
├── config.py                # Configurações globais (caminho do banco, título da app, etc.)
└── cadastro_escolar.db      # Arquivo do banco de dados SQLite (será criado automaticamente)
└── README.md                # Este arquivo
```

## Como Executar

1.  **Certifique-se de ter o Python 3 e o Tkinter instalados.**
2.  **Descompacte o arquivo .zip** fornecido.
3.  **Navegue até o diretório `projeto_escola`** pelo terminal:
    ```bash
    cd caminho/para/projeto_escola
    ```
4.  **Execute o arquivo principal**:
    ```bash
    python main.py
    ```
    *(Use `python3` se `python` estiver associado ao Python 2 no seu sistema)*

5.  A janela da aplicação será aberta.

## Funcionalidades

*   **Navegação:** Utilize o menu superior ("Navegação") para acessar as telas de Início, Cadastro de Turmas e Cadastro de Alunos.
*   **Cadastro de Turmas:**
    *   Acesse "Navegação" > "Cadastro de Turmas".
    *   Preencha o nome e o ano da turma.
    *   Clique em "Cadastrar Turma".
    *   Visualize as turmas cadastradas na tabela.
    *   Selecione uma turma na tabela e clique em "Excluir Turma Selecionada" para removê-la.
*   **Cadastro de Alunos:**
    *   Acesse "Navegação" > "Cadastro de Alunos".
    *   Preencha o nome e o email do aluno.
    *   Selecione uma turma no menu dropdown (é necessário cadastrar turmas primeiro).
    *   Clique em "Cadastrar Aluno".
    *   Visualize os alunos cadastrados na tabela, incluindo a turma associada.
    *   Selecione um aluno na tabela e clique em "Excluir Aluno Selecionado" para removê-lo.
*   **Ajuda:** Acesse o menu "Ajuda" > "Sobre" para ver os créditos e a descrição do projeto.

## Validação Final (Sugestão)

Como não foi possível testar a interface gráfica no ambiente de desenvolvimento, por favor, execute a aplicação em seu ambiente local e teste as seguintes funcionalidades para garantir que tudo está conforme o esperado após a refatoração:

1.  Abrir a aplicação executando `python main.py`.
2.  Navegar entre todas as telas (Início, Turmas, Alunos, Ajuda) usando o menu.
3.  Cadastrar turmas.
4.  Verificar se as turmas aparecem na lista.
5.  Cadastrar alunos, associando-os às turmas criadas.
6.  Verificar se os alunos aparecem na lista com as turmas corretas.
7.  Verificar se o combobox de turmas na tela de Alunos é atualizado automaticamente ao cadastrar/excluir turmas.
8.  Excluir uma turma com alunos e verificar se os alunos ficam "(Sem Turma)".
9.  Excluir alunos.
10. Verificar a tela de Ajuda/Sobre.

Se encontrar qualquer problema ou tiver dúvidas, por favor, me informe.
#   c a d a s t r o _ a l u n o s  
 