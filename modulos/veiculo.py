import sys
import os

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


if __name__ == "__main__":
    print("--- Veículos cadastrados ---")

    veiculos = listar_veiculos()

    for veiculo in veiculos:
        print(veiculo)