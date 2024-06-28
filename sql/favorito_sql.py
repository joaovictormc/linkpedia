SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS favorito (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        url TEXT,
        id_categoria INTEGER,
        id_usuario INTEGER,
        FOREIGN KEY (id_categoria) REFERENCES categoria(id),
        FOREIGN KEY (id_usuario) REFERENCES usuario(id)
    )
"""

SQL_INSERIR = """
    INSERT INTO favorito(nome, url, id_categoria, id_usuario)
    VALUES (?, ?, ?, ?)
"""

SQL_ALTERAR = """
    UPDATE favorito
    SET nome = ?, url = ?, id_categoria = ?, id_usuario = ?
    WHERE id = ?
"""

SQL_EXCLUIR = """
    DELETE FROM favorito
    WHERE id = ?
"""

SQL_OBTER_POR_ID = """
    SELECT id, nome, url, id_categoria, id_usuario
    FROM favorito
    WHERE id = ?
"""

SQL_OBTER_TODOS = """
    SELECT f.id, f.nome, f.url, c.nome as categoria, u.nome as usuario
    FROM favorito f
    INNER JOIN categoria c ON f.id_categoria = c.id
    INNER JOIN usuario u ON f.id_usuario = u.id
    ORDER BY f.nome
"""

SQL_ALTERAR_CATEGORIA = """
    UPDATE favorito
    SET id_categoria = ?
    WHERE id = ?
"""

SQL_ALTERAR_URL = """
    UPDATE favorito
    SET url = ?
    WHERE id = ?
"""

SQL_OBTER_POR_URL = """
    SELECT id, nome, url, id_categoria, id_usuario
    FROM favorito
    WHERE url = ?
"""