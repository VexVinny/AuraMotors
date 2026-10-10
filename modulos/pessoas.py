import pyodbc
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conexao import abrir_conexao



def listar_clientes():
    conexao = abrir_conexao()
    
    if not conexao: 
        return []

    try:
        cursor = conexao.cursor()
        
        query = 'SELECT * FROM "Aura Motors".cliente;'
        cursor.execute(query)
        
        resultados = cursor.fetchall()
        return resultados

    except Exception as erro:
        print(f"Erro ao buscar clientes: {erro}")
        return []
        
    finally:
        # Fecha as conexões de forma segura
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conexao' in locals() and conexao is not None:
            conexao.close()

def adicionar_cliente(nome, email, cpf, telefone):
    conexao = abrir_conexao()

    if not conexao:
        return

    cursor = None

    try:
        cursor = conexao.cursor()

        query = '''
            INSERT INTO "Aura Motors".cliente
            (nome, cpf, email, telefone)
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


def atualizar_cliente(cpf, nome=None, email=None, telefone=None):
    """Atualiza os dados de um cliente identificado pelo CPF.

    Só os campos informados (diferentes de None) são alterados.
    """
    campos = {"nome": nome, "email": email, "telefone": telefone}
    campos = {col: val for col, val in campos.items() if val is not None}

    if not campos:
        print("\nAviso: nenhum campo informado para atualizar.")
        return

    conexao = abrir_conexao()

    if not conexao:
        return

    cursor = None

    try:
        cursor = conexao.cursor()

        set_clause = ", ".join(f"{col} = ?" for col in campos)
        query = f'UPDATE "Aura Motors".cliente SET {set_clause} WHERE cpf = ?'

        cursor.execute(query, (*campos.values(), cpf))

        if cursor.rowcount == 0:
            conexao.rollback()
            print(f"\nAviso: Nenhum cliente encontrado com CPF {cpf}.")
            return

        conexao.commit()
        print(f"\nSucesso: cliente com CPF {cpf} atualizado!")

    except Exception as erro:
        conexao.rollback()
        print(f"\nErro ao atualizar cliente: {erro}")

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



def listar_colaboradores():
    """Busca todos os colaboradores cadastrados no banco."""
    conexao = abrir_conexao()
    
    if not conexao: 
        return []

    try:
        cursor = conexao.cursor()
        
        query = 'SELECT * FROM "Aura Motors".colaborador;'
        cursor.execute(query)
        
        resultados = cursor.fetchall()
        return resultados

    except Exception as erro:
        print(f"Erro ao buscar colaboradores: {erro}")
        return []
        
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conexao' in locals() and conexao is not None:
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


def atualizar_colaborador(cpf, nome=None, cargo=None):
    """Atualiza os dados de um colaborador identificado pelo CPF.

    Só os campos informados (diferentes de None) são alterados.
    """
    campos = {"nome": nome, "cargo": cargo}
    campos = {col: val for col, val in campos.items() if val is not None}

    if not campos:
        print("\nAviso: nenhum campo informado para atualizar.")
        return

    conexao = abrir_conexao()

    if not conexao:
        return

    cursor = None

    try:
        cursor = conexao.cursor()

        set_clause = ", ".join(f"{col} = ?" for col in campos)
        query = (
            f'UPDATE "Aura Motors".colaborador '
            f'SET {set_clause} WHERE cpf = ?'
        )

        cursor.execute(query, (*campos.values(), cpf))

        if cursor.rowcount == 0:
            conexao.rollback()
            print(f"\nAviso: Nenhum colaborador encontrado com CPF {cpf}.")
            return

        conexao.commit()
        print(f"\nSucesso: colaborador com CPF {cpf} atualizado!")

    except Exception as erro:
        conexao.rollback()
        print(f"\nErro ao atualizar colaborador: {erro}")

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