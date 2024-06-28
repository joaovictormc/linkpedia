import sqlite3
import json
from models.usuario_model import Usuario
from sql.usuario_sql import *
from util.database import obter_conexao
from typing import List, Optional


class UsuarioRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, usuario: Usuario) -> Optional[Usuario]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR, 
                    (
                        usuario.nome, 
                        usuario.data_nascimento, 
                        usuario.email, 
                        usuario.senha,
                    ))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def obter_todos(cls) -> List[Usuario]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS).fetchall()
                usuarios = [Usuario(*t) for t in tuplas]
                return usuarios
            
        except sqlite3.Error as ex:
            print(ex)
            return None
        
    @classmethod
    def alterar(cls, usuario: Usuario) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR,
                    (
                        usuario.nome,
                        usuario.data_nascimento,
                        usuario.email,
                        usuario.id,
                    ))
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
    def alterar_senha(cls, id: int, nova_senha: str) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_ALTERAR_SENHA, (nova_senha, id))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
        

    @classmethod
    def obter_por_id(cls, id: int) -> Optional[Usuario]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_ID, (id, )).fetchone()
                if tupla is None:
                    return None
                return Usuario(*tupla)
        except sqlite3.Error as ex:
            print(ex)
            return None