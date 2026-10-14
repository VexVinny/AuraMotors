import sys
import os
from datetime import date

STATUS_DISPONIVEL = 'disponivel'
STATUS_VENDIDO = 'vendido'

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexao import abrir_conexao

def _veiculo_ja_vendido(cursor, id_veiculo):
    """Retorna True se o veículo já está vinculado a algum item de venda."""
    cursor.execute(
        'SELECT 1 FROM "Aura Motors".item_venda WHERE id_veiculo = ?;',
        (int(id_veiculo),)
    )
    return cursor.fetchone() is not None

def listar_vendas():
    """[SELECT com INNER JOIN] Busca todas as vendas trazendo o Nome do Cliente e do Colaborador."""
    conexao = abrir_conexao()
    if not conexao:
        return []

    try:
        cursor = conexao.cursor()
        query = '''
            SELECT 
                v.id_venda, 
                v.data_venda, 
                v.valor_total, 
                c.nome AS nome_cliente, 
                col.nome AS nome_colaborador
            FROM "Aura Motors".venda v
            JOIN "Aura Motors".cliente c ON v.id_cliente = c.id_cliente
            JOIN "Aura Motors".colaborador col ON v.id_colaborador = col.id_colaborador
            ORDER BY v.id_venda DESC;
        '''
        cursor.execute(query)
        vendas = cursor.fetchall()
        cursor.close()
        return vendas
    except Exception as e:
        print(f"Erro ao buscar vendas com JOIN: {e}")
        return []
    finally:
        if conexao:
            conexao.close()


def buscar_venda_por_id(id_venda):
    """[SELECT] Busca os dados de uma venda específica pelo ID para preencher o formulário de edição."""
    conexao = abrir_conexao()
    if not conexao:
        return None

    try:
        cursor = conexao.cursor()
        query = '''
            SELECT id_venda, data_venda, valor_total, id_cliente, id_colaborador 
            FROM "Aura Motors".venda 
            WHERE id_venda = ?;
        '''
        cursor.execute(query, (id_venda,))
        venda = cursor.fetchone()
        cursor.close()
        return venda
    except Exception as e:
        print(f"Erro ao buscar venda por ID: {e}")
        return None
    finally:
        if conexao:
            conexao.close()


def registrar_venda(id_cliente, id_colaborador, id_veiculo):
    """[INSERT + UPDATE] Cadastra a venda, cria o item e marca o veículo como vendido."""
    conexao = abrir_conexao()
    if not conexao:
        return False

    try:
        cursor = conexao.cursor()

        cursor.execute(
            'SELECT preco FROM "Aura Motors".veiculo WHERE id_veiculo = ?;',
            (int(id_veiculo),)
        )
        resultado = cursor.fetchone()
        if not resultado:
            print(f"Veículo {id_veiculo} não encontrado.")
            return False
        preco = resultado[0]

        if _veiculo_ja_vendido(cursor, id_veiculo):
            print(f"Veículo {id_veiculo} já foi vendido.")
            return False

        cursor.execute('''
            INSERT INTO "Aura Motors".venda (data_venda, valor_total, id_cliente, id_colaborador)
            VALUES (?, ?, ?, ?)
            RETURNING id_venda;
        ''', (date.today(), preco, int(id_cliente), int(id_colaborador)))
        id_venda = cursor.fetchone()[0]

        cursor.execute('''
            INSERT INTO "Aura Motors".item_venda (id_venda, id_veiculo, preco_praticado)
            VALUES (?, ?, ?);
        ''', (id_venda, int(id_veiculo), preco))

        # Marca o veículo como vendido
        cursor.execute(
            'UPDATE "Aura Motors".veiculo SET status = ? WHERE id_veiculo = ?;',
            (STATUS_VENDIDO, int(id_veiculo))
        )

        conexao.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Erro ao registrar venda: {e}")
        if conexao:
            conexao.rollback()
        return False
    finally:
        if conexao:
            conexao.close()


def atualizar_venda(id_venda, id_cliente, id_colaborador):
    """[UPDATE] Atualiza cliente e colaborador de uma venda.
    O valor_total não é editado aqui: ele vem da soma dos itens."""
    conexao = abrir_conexao()
    if not conexao:
        return False

    try:
        cursor = conexao.cursor()
        cursor.execute('''
            UPDATE "Aura Motors".venda
            SET id_cliente = ?, id_colaborador = ?
            WHERE id_venda = ?;
        ''', (int(id_cliente), int(id_colaborador), int(id_venda)))
        conexao.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Erro ao atualizar venda: {e}")
        if conexao:
            conexao.rollback()
        return False
    finally:
        if conexao:
            conexao.close()


def remover_venda(id_venda):
    """[DELETE + UPDATE] Remove a venda e seus itens e devolve os veículos para disponível."""
    conexao = abrir_conexao()
    if not conexao:
        return False

    try:
        cursor = conexao.cursor()

        cursor.execute('''
            UPDATE "Aura Motors".veiculo
            SET status = ?
            WHERE id_veiculo IN (
                SELECT id_veiculo FROM "Aura Motors".item_venda WHERE id_venda = ?
            );
        ''', (STATUS_DISPONIVEL, int(id_venda)))

        cursor.execute('DELETE FROM "Aura Motors".item_venda WHERE id_venda = ?;', (int(id_venda),))
        cursor.execute('DELETE FROM "Aura Motors".venda WHERE id_venda = ?;', (int(id_venda),))

        conexao.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Erro ao remover venda: {e}")
        if conexao:
            conexao.rollback()
        return False
    finally:
        if conexao:
            conexao.close()


def listar_itens_da_venda(id_venda):
    """[SELECT] Lista todos os itens/veículos associados a uma venda específica."""
    conexao = abrir_conexao()
    if not conexao:
        return []

    try:
        cursor = conexao.cursor()
        query = '''
            SELECT id_item, id_venda, id_veiculo, preco_praticado 
            FROM "Aura Motors".item_venda 
            WHERE id_venda = ?;
        '''
        cursor.execute(query, (id_venda,))
        itens = cursor.fetchall()
        cursor.close()
        return itens
    except Exception as e:
        print(f"Erro ao listar itens da venda: {e}")
        return []
    finally:
        if conexao:
            conexao.close()


def adicionar_item_venda(id_venda, id_veiculo):
    """[INSERT + UPDATE] Adiciona o veículo à venda, recalcula o total e marca como vendido."""
    conexao = abrir_conexao()
    if not conexao:
        return False

    try:
        cursor = conexao.cursor()

        cursor.execute(
            'SELECT preco FROM "Aura Motors".veiculo WHERE id_veiculo = ?;',
            (int(id_veiculo),)
        )
        resultado = cursor.fetchone()
        if not resultado:
            print(f"Veículo {id_veiculo} não encontrado.")
            return False
        preco = resultado[0]

        if _veiculo_ja_vendido(cursor, id_veiculo):
            print(f"Veículo {id_veiculo} já foi vendido.")
            return False

        cursor.execute('''
            INSERT INTO "Aura Motors".item_venda (id_venda, id_veiculo, preco_praticado)
            VALUES (?, ?, ?);
        ''', (int(id_venda), int(id_veiculo), preco))

        cursor.execute('''
            UPDATE "Aura Motors".venda
            SET valor_total = (
                SELECT COALESCE(SUM(preco_praticado), 0)
                FROM "Aura Motors".item_venda
                WHERE id_venda = ?
            )
            WHERE id_venda = ?;
        ''', (int(id_venda), int(id_venda)))

        cursor.execute(
            'UPDATE "Aura Motors".veiculo SET status = ? WHERE id_veiculo = ?;',
            (STATUS_VENDIDO, int(id_veiculo))
        )

        conexao.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"\n[ERRO SQL - ITEM VENDA]: {e}\n")
        if conexao:
            conexao.rollback()
        return False
    finally:
        if conexao:
            conexao.close()


def remover_item_venda(id_item, id_venda):
    """[DELETE + UPDATE] Remove o item, recalcula o total e devolve o veículo para disponível."""
    conexao = abrir_conexao()
    if not conexao:
        return False

    try:
        cursor = conexao.cursor()

        cursor.execute(
            'SELECT id_veiculo FROM "Aura Motors".item_venda WHERE id_item = ?;',
            (int(id_item),)
        )
        resultado = cursor.fetchone()
        if not resultado:
            print(f"Item {id_item} não encontrado.")
            return False
        id_veiculo = resultado[0]

        cursor.execute('DELETE FROM "Aura Motors".item_venda WHERE id_item = ?;', (int(id_item),))

        cursor.execute('''
            UPDATE "Aura Motors".venda
            SET valor_total = (
                SELECT COALESCE(SUM(preco_praticado), 0)
                FROM "Aura Motors".item_venda
                WHERE id_venda = ?
            )
            WHERE id_venda = ?;
        ''', (int(id_venda), int(id_venda)))

        cursor.execute(
            'UPDATE "Aura Motors".veiculo SET status = ? WHERE id_veiculo = ?;',
            (STATUS_DISPONIVEL, id_veiculo)
        )

        conexao.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Erro ao remover item da venda: {e}")
        if conexao:
            conexao.rollback()
        return False
    finally:
        if conexao:
            conexao.close()


def listar_veiculos_nunca_vendidos():
    """[EXCEPT] Retorna os veículos do estoque que NUNCA foram vendidos."""
    conexao = abrir_conexao()
    if not conexao:
        return []

    try:
        cursor = conexao.cursor()
        query = '''
            SELECT id_veiculo, modelo, preco 
            FROM "Aura Motors".veiculo
            EXCEPT
            SELECT v.id_veiculo, v.modelo, v.preco 
            FROM "Aura Motors".veiculo v
            JOIN "Aura Motors".item_venda iv ON v.id_veiculo = iv.id_veiculo;
        '''
        cursor.execute(query)
        veiculos = cursor.fetchall()
        cursor.close()
        return veiculos
    except Exception as e:
        print(f"Erro ao buscar veículos nunca vendidos (EXCEPT): {e}")
        return []
    finally:
        if conexao:
            conexao.close()