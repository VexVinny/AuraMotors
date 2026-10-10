import pyodbc
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conexao import abrir_conexao

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexao import abrir_conexao

def listar_clientes():
    """Busca e retorna todos os clientes cadastrados no banco."""
    conexao = abrir_conexao()
    if not conexao:
        return []

    try:
        cursor = conexao.cursor()
        query = 'SELECT * FROM "Aura Motors".cliente;'
        cursor.execute(query)
        clientes = cursor.fetchall()
        
        cursor.close()
        conexao.close()
        return clientes

    except Exception as e:
        print(f"Erro ao listar clientes: {e}")
        return []
        
        
def adicionar_cliente(nome, email, cpf, telefone):
    conexao = abrir_conexao()

    if not conexao:
        return

    cursor = None

    try:
        cursor = conexao.cursor()

        query = '''
            INSERT INTO "Aura Motors".cliente
            (nome, email, cpf, telefone)
            VALUES (?, ?, ?, ?)
        '''

        cursor.execute(query, (nome, email, cpf, telefone))
        conexao.commit()

        print(f"\nCliente '{nome}' inserido com sucesso!")

    except Exception as erro:
        conexao.rollback()
        print(f"\nErro ao inserir cliente: {erro}")

    finally:
        if cursor is not None:
            cursor.close()
        conexao.close() 
        
        
def remover_cliente(cpf):
    conexao = abrir_conexao()

    if not conexao:
        return

    cursor = None
    nome_cliente = "desconhecido"

    try:
        cursor = conexao.cursor()

        cursor.execute(
            'SELECT nome FROM "Aura Motors".cliente WHERE cpf = ?',
            (cpf,)
        )
        cliente = cursor.fetchone()

        if not cliente:
            print(f"\nAviso: Nenhum cliente encontrado com CPF {cpf}.")
            return

        nome_cliente = cliente[0]

        cursor.execute(
            'DELETE FROM "Aura Motors".cliente WHERE cpf = ?',
            (cpf,)
        )

        conexao.commit()
        print(f"\nSucesso: O cliente '{nome_cliente}' foi removido do sistema!")

    except pyodbc.IntegrityError:
        conexao.rollback()
        print(
            f"\nErro de integridade: não foi possível remover "
            f"o cliente '{nome_cliente}' devido a registros relacionados."
        )

    except Exception as erro:
        conexao.rollback()
        print(f"\nErro inesperado ao remover o cliente: {erro}")

    finally:
        if cursor is not None:
            cursor.close()
        conexao.close()
        
        
def listar_desempenho_colaboradores():
    conexao = abrir_conexao()

    if not conexao:
        return

    cursor = None

    try:
        cursor = conexao.cursor()

        cursor.execute(
            'SELECT * FROM "Aura Motors".mv_12_desempenho_colaboradores;'
        )

        colunas = [column[0] for column in cursor.description]
        resultado = cursor.fetchall()

        print("\n--- DESEMPENHO DOS COLABORADORES ---")
        print(" | ".join(colunas))
        print("-" * 70)

        for linha in resultado:
            print(" | ".join(
                str(valor) if valor is not None else "N/A"
                for valor in linha
            ))

    except Exception as erro:
        print(f"\nErro ao listar colaboradores: {erro}")

    finally:
        if cursor is not None:
            cursor.close()
        conexao.close()
        

def adicionar_colaborador(nome, cpf, cargo):
    conexao = abrir_conexao()

    if not conexao:
        return

    cursor = None

    try:
        cursor = conexao.cursor()

        cursor.execute(
            '''
            INSERT INTO "Aura Motors".colaborador
            (nome, cpf, cargo)
            VALUES (?, ?, ?)
            ''',
            (nome, cpf, cargo)
        )

        conexao.commit()

        print(
            f"\nSucesso: O colaborador '{nome}', "
            f"com cargo '{cargo}', foi adicionado ao sistema!"
        )

    except Exception as erro:
        conexao.rollback()
        print(f"\nErro ao registrar colaborador: {erro}")

    finally:
        if cursor is not None:
            cursor.close()
        conexao.close()
        
        
def remover_colaborador(cpf):
    conexao = abrir_conexao()

    if not conexao:
        return

    cursor = None
    nome_colaborador = "desconhecido"

    try:
        cursor = conexao.cursor()

        cursor.execute(
            'SELECT nome FROM "Aura Motors".colaborador WHERE cpf = ?',
            (cpf,)
        )
        colaborador = cursor.fetchone()

        if not colaborador:
            print(
                f"\nAviso: Nenhum colaborador encontrado com CPF {cpf}."
            )
            return

        nome_colaborador = colaborador[0]

        cursor.execute(
            'DELETE FROM "Aura Motors".colaborador WHERE cpf = ?',
            (cpf,)
        )

        conexao.commit()

        print(
            f"\nSucesso: O colaborador '{nome_colaborador}' "
            f"foi removido do sistema!"
        )

    except pyodbc.IntegrityError:
        conexao.rollback()
        print(
            f"\nErro de integridade: não foi possível remover "
            f"o colaborador '{nome_colaborador}' devido a registros relacionados."
        )

    except Exception as erro:
        conexao.rollback()
        print(f"\nErro inesperado ao remover o colaborador: {erro}")

    finally:
        if cursor is not None:
            cursor.close()
        conexao.close()

    
                
