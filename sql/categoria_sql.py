SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        nome TEXT NOT NULL,
        icone TEXT
    )
"""

SQL_INSERIR = """
    INSERT INTO categoria(nome, icone)
    VALUES (?, ?)
"""

SQL_ALTERAR = """
    UPDATE categoria
    SET nome = ?, icone = ?
    WHERE id = ?
"""

SQL_EXCLUIR = """
    DELETE FROM categoria
    WHERE id = ?
"""

SQL_OBTER_TODOS = """
    SELECT id, nome, icone
    FROM categoria
    ORDER BY nome
"""

SQL_OBTER_POR_ID = """
    SELECT id, nome, icone
    FROM categoria
    WHERE id = ?
"""

SQL_OBTER_BUSCA = """
    SELECT id, nome, icone
    FROM categoria
    WHERE nome LIKE ?
    ORDER BY nome
"""