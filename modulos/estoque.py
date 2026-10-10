import sys
import os
import pyodbc

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
))

from conexao import abrir_conexao


def listar_veiculos():
    """Busca todos os veículos cadastrados no banco."""
    conexao = abrir_conexao()

    if not conexao:
        return []

    try:
        cursor = conexao.cursor()

        query = 'SELECT * FROM "Aura Motors".veiculo;'
        cursor.execute(query)

        veiculos = cursor.fetchall()

        cursor.close()
        conexao.close()

        return veiculos

    except Exception as e:
        print(f"Erro ao buscar veículos: {e}")
        conexao.close()
        return []


def registrar_veiculo(
    modelo, ano, preco, status,
    id_montadora, id_marca, id_categoria
):
    """Registra um veículo no banco de dados."""
    conexao = abrir_conexao()

    if not conexao:
        return False

    try:
        cursor = conexao.cursor()

        query = '''
            INSERT INTO "Aura Motors".veiculo
                (modelo, ano, preco, status,
                 id_montadora, id_marca, id_categoria)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            RETURNING id_veiculo;
        '''

        cursor.execute(query, (
            modelo, ano, preco, status,
            id_montadora, id_marca, id_categoria
        ))

        id_veiculo = cursor.fetchone()[0]

        conexao.commit()

        print(f"Veículo cadastrado! ID: {id_veiculo}")

        cursor.close()
        conexao.close()

        return True

    except Exception as e:
        print(f"Erro ao cadastrar veículo: {e}")
        conexao.rollback()
        conexao.close()
        return False


def atualizar_veiculo(
    id_veiculo, modelo=None, ano=None, preco=None, status=None,
    id_montadora=None, id_marca=None, id_categoria=None
):
    """Atualiza um veículo. Só os campos informados são alterados."""
    campos = {
        "modelo": modelo,
        "ano": ano,
        "preco": preco,
        "status": status,
        "id_montadora": id_montadora,
        "id_marca": id_marca,
        "id_categoria": id_categoria,
    }
    campos = {col: val for col, val in campos.items() if val is not None}

    if not campos:
        print("Aviso: nenhum campo informado para atualizar o veículo.")
        return False

    conexao = abrir_conexao()

    if not conexao:
        return False

    try:
        cursor = conexao.cursor()

        set_clause = ", ".join(f"{col} = ?" for col in campos)
        query = (
            f'UPDATE "Aura Motors".veiculo '
            f'SET {set_clause} WHERE id_veiculo = ?'
        )

        cursor.execute(query, (*campos.values(), id_veiculo))

        if cursor.rowcount == 0:
            print(f"Aviso: nenhum veículo encontrado com ID {id_veiculo}.")
            conexao.rollback()
            cursor.close()
            conexao.close()
            return False

        conexao.commit()

        print(f"Veículo {id_veiculo} atualizado com sucesso!")

        cursor.close()
        conexao.close()

        return True

    except Exception as e:
        print(f"Erro ao atualizar veículo: {e}")
        conexao.rollback()
        conexao.close()
        return False


def remover_veiculo(id_veiculo):
    """Remove um veículo pelo ID."""
    conexao = abrir_conexao()

    if not conexao:
        return False

    try:
        cursor = conexao.cursor()

        query = 'DELETE FROM "Aura Motors".veiculo WHERE id_veiculo = ?'
        cursor.execute(query, (id_veiculo,))

        if cursor.rowcount == 0:
            print(f"Aviso: nenhum veículo encontrado com ID {id_veiculo}.")
            conexao.rollback()
            cursor.close()
            conexao.close()
            return False

        conexao.commit()

        print(f"Veículo {id_veiculo} removido com sucesso!")

        cursor.close()
        conexao.close()

        return True

    except pyodbc.IntegrityError:
        print(
            f"Erro de integridade: não foi possível remover "
            f"o veículo {id_veiculo} devido a registros relacionados."
        )
        conexao.rollback()
        conexao.close()
        return False

    except Exception as e:
        print(f"Erro ao remover veículo: {e}")
        conexao.rollback()
        conexao.close()
        return False


def listar_marcas():
    """Busca todas as marcas cadastradas no banco."""
    conexao = abrir_conexao()

    if not conexao:
        return []

    try:
        cursor = conexao.cursor()

        query = 'SELECT * FROM "Aura Motors".marca;'
        cursor.execute(query)

        marcas = cursor.fetchall()

        cursor.close()
        conexao.close()

        return marcas

    except Exception as e:
        print(f"Erro ao buscar marcas: {e}")
        conexao.close()
        return []


def registrar_marca(nome_marca):
    """Registra uma marca no banco de dados."""
    conexao = abrir_conexao()

    if not conexao:
        return False

    try:
        cursor = conexao.cursor()

        query = '''
            INSERT INTO "Aura Motors".marca
                (nome_marca)
            VALUES (?)
            RETURNING id_marca;
        '''

        cursor.execute(query, (nome_marca,))

        id_marca = cursor.fetchone()[0]

        conexao.commit()

        print(f"Marca registrada! ID: {id_marca}")

        cursor.close()
        conexao.close()

        return True

    except Exception as e:
        print(f"Erro ao cadastrar marca: {e}")
        conexao.rollback()
        conexao.close()
        return False


def atualizar_marca(id_marca, nome_marca):
    """Atualiza o nome de uma marca."""
    conexao = abrir_conexao()

    if not conexao:
        return False

    try:
        cursor = conexao.cursor()

        query = '''
            UPDATE "Aura Motors".marca
            SET nome_marca = ?
            WHERE id_marca = ?
        '''

        cursor.execute(query, (nome_marca, id_marca))

        if cursor.rowcount == 0:
            print(f"Aviso: nenhuma marca encontrada com ID {id_marca}.")
            conexao.rollback()
            cursor.close()
            conexao.close()
            return False

        conexao.commit()

        print(f"Marca {id_marca} atualizada com sucesso!")

        cursor.close()
        conexao.close()

        return True

    except Exception as e:
        print(f"Erro ao atualizar marca: {e}")
        conexao.rollback()
        conexao.close()
        return False


def remover_marca(id_marca):
    """Remove uma marca pelo ID."""
    conexao = abrir_conexao()

    if not conexao:
        return False

    try:
        cursor = conexao.cursor()

        query = 'DELETE FROM "Aura Motors".marca WHERE id_marca = ?'
        cursor.execute(query, (id_marca,))

        if cursor.rowcount == 0:
            print(f"Aviso: nenhuma marca encontrada com ID {id_marca}.")
            conexao.rollback()
            cursor.close()
            conexao.close()
            return False

        conexao.commit()

        print(f"Marca {id_marca} removida com sucesso!")

        cursor.close()
        conexao.close()

        return True

    except pyodbc.IntegrityError:
        print(
            f"Erro de integridade: não foi possível remover "
            f"a marca {id_marca} devido a registros relacionados."
        )
        conexao.rollback()
        conexao.close()
        return False

    except Exception as e:
        print(f"Erro ao remover marca: {e}")
        conexao.rollback()
        conexao.close()
        return False


def listar_montadoras():
    """Busca todas as montadoras cadastradas no banco."""
    conexao = abrir_conexao()

    if not conexao:
        return []

    try:
        cursor = conexao.cursor()

        query = 'SELECT * FROM "Aura Motors".montadora;'
        cursor.execute(query)

        montadoras = cursor.fetchall()

        cursor.close()
        conexao.close()

        return montadoras

    except Exception as e:
        print(f"Erro ao buscar montadoras: {e}")
        conexao.close()
        return []


def registrar_montadora(nome_montadora):
    """Registra uma montadora no banco de dados."""
    conexao = abrir_conexao()

    if not conexao:
        return False

    try:
        cursor = conexao.cursor()

        query = '''
            INSERT INTO "Aura Motors".montadora
                (nome_montadora)
            VALUES (?)
            RETURNING id_montadora;
        '''

        cursor.execute(query, (nome_montadora,))

        id_montadora = cursor.fetchone()[0]

        conexao.commit()

        print(f"Montadora registrada! ID: {id_montadora}")

        cursor.close()
        conexao.close()

        return True

    except Exception as e:
        print(f"Erro ao cadastrar montadora: {e}")
        conexao.rollback()
        conexao.close()
        return False


def atualizar_montadora(id_montadora, nome_montadora):
    """Atualiza o nome de uma montadora."""
    conexao = abrir_conexao()

    if not conexao:
        return False

    try:
        cursor = conexao.cursor()

        query = '''
            UPDATE "Aura Motors".montadora
            SET nome_montadora = ?
            WHERE id_montadora = ?
        '''

        cursor.execute(query, (nome_montadora, id_montadora))

        if cursor.rowcount == 0:
            print(f"Aviso: nenhuma montadora encontrada com ID {id_montadora}.")
            conexao.rollback()
            cursor.close()
            conexao.close()
            return False

        conexao.commit()

        print(f"Montadora {id_montadora} atualizada com sucesso!")

        cursor.close()
        conexao.close()

        return True

    except Exception as e:
        print(f"Erro ao atualizar montadora: {e}")
        conexao.rollback()
        conexao.close()
        return False


def remover_montadora(id_montadora):
    """Remove uma montadora pelo ID."""
    conexao = abrir_conexao()

    if not conexao:
        return False

    try:
        cursor = conexao.cursor()

        query = 'DELETE FROM "Aura Motors".montadora WHERE id_montadora = ?'
        cursor.execute(query, (id_montadora,))

        if cursor.rowcount == 0:
            print(f"Aviso: nenhuma montadora encontrada com ID {id_montadora}.")
            conexao.rollback()
            cursor.close()
            conexao.close()
            return False

        conexao.commit()

        print(f"Montadora {id_montadora} removida com sucesso!")

        cursor.close()
        conexao.close()

        return True

    except pyodbc.IntegrityError:
        print(
            f"Erro de integridade: não foi possível remover "
            f"a montadora {id_montadora} devido a registros relacionados."
        )
        conexao.rollback()
        conexao.close()
        return False

    except Exception as e:
        print(f"Erro ao remover montadora: {e}")
        conexao.rollback()
        conexao.close()
        return False


if __name__ == "__main__":
    print("--- Veículos cadastrados ---")
    for veiculo in listar_veiculos():
        print(veiculo)

    print("\n--- Marcas registradas ---")
    for marca in listar_marcas():
        print(marca)

    print("\n--- Montadoras registradas ---")
    for montadora in listar_montadoras():
        print(montadora)