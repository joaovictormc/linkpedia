import sqlite3
import json
from typing import List, Optional
from models.favorito_model import Favorito
from sql.favorito_sql import *
from util.database import obter_conexao



class FavoritoRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)


    @classmethod
    def inserir(cls, favorito: Favorito) -> Optional[Favorito]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (
                        favorito.id,
                        favorito.id_usuario,
                        favorito.id_link,
                    ),
                )
                conexao.commit()
                return favorito
        except sqlite3.Error as ex:
            print(ex)
            return None
        

    @classmethod
    def alterar(cls, favorito: Favorito) -> Optional[Favorito]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR,
                    (
                        favorito.id_usuario,
                        favorito.id_link,
                        favorito.id,
                    ),
                )
                conexao.commit()
                return favorito
        except sqlite3.Error as ex:
            print(ex)
            return None
        

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
    def alterar_categoria(cls, id_categoria: int, url: str) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_ALTERAR_CATEGORIA, (id_categoria, url))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
        

    @classmethod
    def alterar_url(cls, id: int, url: str) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_ALTERAR_URL, (url, id))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
        
    @classmethod
    def obter_por_id(cls, id: int) -> Optional[Favorito]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_ID, (id,)).fetchone()
                favorito = Favorito(*tupla)
                return favorito
        except sqlite3.Error as ex:
            print(ex)
            return None
        

    @classmethod
    def obter_por_url(cls, url: str) -> Optional[Favorito]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_URL, (url, )).fetchone()
                favorito = Favorito(*tupla)
                return favorito
        except sqlite3.Error as ex:
            print(ex)
            return None
        

    @classmethod
    def obter_todos(cls) -> List[Favorito]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS).fetchall()
                favoritos = [Favorito(*tupla) for tupla in tuplas]
                return favoritos
        except sqlite3.Error as ex:
            print(ex)
            return []