import pyodbc
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conexao import conectar # Corrigido para conectar() que é o nome da tua função no conexao.py

def listar_clientes():
    conexao = conectar()
    if not conexao: return []
    try:
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM "Aura Motors".cliente;')
        resultados = cursor.fetchall()
        return resultados
    except Exception as erro:
        print(f"Erro ao buscar clientes: {erro}")
        return []
    finally:
        if 'cursor' in locals() and cursor is not None: cursor.close()
        if 'conexao' in locals() and conexao is not None: conexao.close()

def adicionar_cliente(nome, email, cpf, telefone):
    conexao = conectar()
    if not conexao: return False
    try:
        cursor = conexao.cursor()
        query = 'INSERT INTO "Aura Motors".cliente (nome, cpf, email, telefone) VALUES (?, ?, ?, ?)'
        cursor.execute(query, (nome, cpf, email, telefone))
        conexao.commit()
        return True
    except Exception as erro:
        print(f"Erro ao inserir cliente: {erro}")
        conexao.rollback()
        return False
    finally:
        if 'cursor' in locals() and cursor is not None: cursor.close()
        conexao.close()

def atualizar_cliente(cpf, nome=None, email=None, telefone=None):
    campos = {"nome": nome, "email": email, "telefone": telefone}
    campos = {col: val for col, val in campos.items() if val is not None}
    if not campos: return False
    
    conexao = conectar()
    if not conexao: return False
    try:
        cursor = conexao.cursor()
        set_clause = ", ".join(f"{col} = ?" for col in campos)
        query = f'UPDATE "Aura Motors".cliente SET {set_clause} WHERE cpf = ?'
        cursor.execute(query, (*campos.values(), cpf))
        
        if cursor.rowcount == 0:
            conexao.rollback()
            return False
            
        conexao.commit()
        return True
    except Exception as erro:
        print(f"Erro ao atualizar cliente: {erro}")
        conexao.rollback()
        return False
    finally:
        if 'cursor' in locals() and cursor is not None: cursor.close()
        conexao.close()

def remover_cliente(cpf):
    conexao = conectar()
    if not conexao: return False
    try:
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM "Aura Motors".cliente WHERE cpf = ?', (cpf,))
        if cursor.rowcount == 0:
            return False
        conexao.commit()
        return True
    except Exception as erro:
        print(f"Erro ao remover cliente: {erro}")
        conexao.rollback()
        return False
    finally:
        if 'cursor' in locals() and cursor is not None: cursor.close()
        conexao.close()

def listar_colaboradores():
    conexao = conectar()
    if not conexao: return []
    try:
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM "Aura Motors".colaborador;')
        return cursor.fetchall()
    except Exception as erro:
        print(f"Erro ao buscar colaboradores: {erro}")
        return []
    finally:
        if 'cursor' in locals() and cursor is not None: cursor.close()
        if 'conexao' in locals() and conexao is not None: conexao.close()

def adicionar_colaborador(nome, cpf, cargo):
    conexao = conectar()
    if not conexao: return False
    try:
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO "Aura Motors".colaborador (nome, cpf, cargo) VALUES (?, ?, ?)', (nome, cpf, cargo))
        conexao.commit()
        return True
    except Exception as erro:
        print(f"Erro ao registrar colaborador: {erro}")
        conexao.rollback()
        return False
    finally:
        if 'cursor' in locals() and cursor is not None: cursor.close()
        conexao.close()

def atualizar_colaborador(cpf, nome=None, cargo=None):
    campos = {"nome": nome, "cargo": cargo}
    campos = {col: val for col, val in campos.items() if val is not None}
    if not campos: return False
    
    conexao = conectar()
    if not conexao: return False
    try:
        cursor = conexao.cursor()
        set_clause = ", ".join(f"{col} = ?" for col in campos)
        query = f'UPDATE "Aura Motors".colaborador SET {set_clause} WHERE cpf = ?'
        cursor.execute(query, (*campos.values(), cpf))
        
        if cursor.rowcount == 0:
            conexao.rollback()
            return False
            
        conexao.commit()
        return True
    except Exception as erro:
        print(f"Erro ao atualizar colaborador: {erro}")
        conexao.rollback()
        return False
    finally:
        if 'cursor' in locals() and cursor is not None: cursor.close()
        conexao.close()

def remover_colaborador(cpf):
    conexao = conectar()
    if not conexao: return False
    try:
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM "Aura Motors".colaborador WHERE cpf = ?', (cpf,))
        if cursor.rowcount == 0:
            return False
        conexao.commit()
        return True
    except Exception as erro:
        print(f"Erro ao remover o colaborador: {erro}")
        conexao.rollback()
        return False
    finally:
        if 'cursor' in locals() and cursor is not None: cursor.close()
        conexao.close()