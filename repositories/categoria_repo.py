import sqlite3
import json
from typing import List, Optional
from models.categoria_model import Categoria
from sql.categoria_sql import *
from util.database import obter_conexao


class CategoriaRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)


    @classmethod
    def inserir(cls, categoria: Categoria) -> Optional[Categoria]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (
                        categoria.nome,
                        categoria.data_nascimento,
                        categoria.email,
                        categoria.senha,
                    ),
                )
                if cursor.rowcount > 0:
                    categoria.id = cursor.lastrowid
                    return categoria
        except sqlite3.Error as ex:
            print(ex)
            return None
        

    @classmethod
    def alterar(cls, categoria: Categoria) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR,
                    (
                        categoria.nome,
                        categoria.data_nascimento,
                        categoria.email,
                        categoria.id,
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
        

    @classmethod
    def excluir(cls, id: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
        

    @classmethod
    def obter_busca(cls, termo: str, pagina: int, tamanho_pagina: int) -> List[Categoria]:
        termo = "%" + termo + "%"
        offset = (pagina - 1) * tamanho_pagina
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(
                    SQL_OBTER_BUSCA, (termo, termo, tamanho_pagina, offset)
                ).fetchall()
                categoria = [Categoria(*t) for t in tuplas]
                return categoria
        except sqlite3.Error as ex:
            print(ex)
            return None
        

    @classmethod
    def obter_todos(cls) -> List[Categoria]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS).fetchall()
                categoria = [Categoria(*t) for t in tuplas]
                return categoria
        except sqlite3.Error as ex:
            print(ex)
            return None
        

    @classmethod
    def obter_por_id(cls, id: int) -> Optional[Categoria]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_ID, (id, )).fetchone()
                if tupla:
                    return Categoria(*tupla)
                else:
                    return None
        except sqlite3.Error as ex:
            print(ex)
            return None