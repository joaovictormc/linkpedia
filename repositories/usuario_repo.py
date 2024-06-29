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
                if cursor.rowcount > 0:
                    Usuario.id = cursor.lastrowid
                    return Usuario
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
        
    @classmethod
    def obter_por_email(cls, email: str) -> Optional[Usuario]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_EMAIL, (email,)).fetchone()
                if tupla:
                    usuario = Usuario(*tupla)
                    return usuario
                else:
                    return None
        except sqlite3.Error as ex:
            print(ex)
            return None
        

    @classmethod
    def obter_por_token(cls, token: str) -> Optional[Usuario]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(
                    SQL_OBTER_POR_TOKEN, (token,)).fetchone()
                if tupla is None:
                    return None
                return Usuario(*tupla)
        except sqlite3.Error as ex:
            print(ex)
            return None
        
    @classmethod
    def alterar_token(cls, id: int, token: str) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_ALTERAR_TOKEN, (token, id))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
        
    @classmethod
    def obter_busca(cls) -> List[Usuario]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_BUSCA).fetchall()
                usuarios = [Usuario(*t) for t in tuplas]
                return usuarios
        except sqlite3.Error as ex:
            print(ex)
            return None
    
    @classmethod
    def obter_quantidade(cls) -> int:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_QUANTIDADE).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return None
        

    @classmethod
    def inserir_usuarios_json(cls, arquivo_json: str):
        if UsuarioRepo.obter_quantidade() == 0:
            with open(arquivo_json, "r", encoding="utf-8") as arquivo:
                usuarios = json.load(arquivo)
                for usuario in usuarios:
                    UsuarioRepo.inserir(Usuario(**usuario))