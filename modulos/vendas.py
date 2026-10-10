import sys
import os
from datetime import date

# Garante a importação do conexao.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexao import abrir_conexao

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


def registrar_venda(valor_total, id_cliente, id_colaborador):
    """[INSERT] Cadastra uma nova venda com a data atual."""
    conexao = abrir_conexao()
    if not conexao:
        return False

    try:
        cursor = conexao.cursor()
        query = '''
            INSERT INTO "Aura Motors".venda (data_venda, valor_total, id_cliente, id_colaborador)
            VALUES (?, ?, ?, ?);
        '''
        data_hoje = date.today()
        cursor.execute(query, (data_hoje, valor_total, id_cliente, id_colaborador))
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


def atualizar_venda(id_venda, valor_total, id_cliente, id_colaborador):
    """[UPDATE] Atualiza as informações de uma venda existente."""
    conexao = abrir_conexao()
    if not conexao:
        return False

    try:
        cursor = conexao.cursor()
        query = '''
            UPDATE "Aura Motors".venda
            SET valor_total = ?, id_cliente = ?, id_colaborador = ?
            WHERE id_venda = ?;
        '''
        cursor.execute(query, (valor_total, id_cliente, id_colaborador, id_venda))
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
    """[DELETE] Remove uma venda e seus itens vinculados na tabela item_venda."""
    conexao = abrir_conexao()
    if not conexao:
        return False

    try:
        cursor = conexao.cursor()
        
        # 1. Remove primeiro os itens vinculados na tabela item_venda (evita erro de Chave Estrangeira)
        query_itens = 'DELETE FROM "Aura Motors".item_venda WHERE id_venda = ?;'
        cursor.execute(query_itens, (id_venda,))

        # 2. Remove o registro principal da venda
        query_venda = 'DELETE FROM "Aura Motors".venda WHERE id_venda = ?;'
        cursor.execute(query_venda, (id_venda,))

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
    """[SELECT] Lista todos os veículos/itens associados a uma venda específica."""
    conexao = abrir_conexao()
    if not conexao:
        return []

    try:
        cursor = conexao.cursor()
        query = '''
            SELECT id_item_venda, id_venda, id_veiculo, valor_unitario 
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


def adicionar_item_venda(id_venda, id_veiculo, valor_unitario):
    """[INSERT] Adiciona um veículo como item de uma venda."""
    conexao = abrir_conexao()
    if not conexao:
        return False

    try:
        cursor = conexao.cursor()
        query = '''
            INSERT INTO "Aura Motors".item_venda (id_venda, id_veiculo, valor_unitario)
            VALUES (?, ?, ?);
        '''
        cursor.execute(query, (id_venda, id_veiculo, valor_unitario))
        conexao.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Erro ao adicionar item na venda: {e}")
        if conexao:
            conexao.rollback()
        return False
    finally:
        if conexao:
            conexao.close()


def atualizar_item_venda(id_item_venda, valor_unitario):
    """[UPDATE] Atualiza o valor unitário de um item da venda."""
    conexao = abrir_conexao()
    if not conexao:
        return False

    try:
        cursor = conexao.cursor()
        query = '''
            UPDATE "Aura Motors".item_venda
            SET valor_unitario = ?
            WHERE id_item_venda = ?;
        '''
        cursor.execute(query, (valor_unitario, id_item_venda))
        conexao.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Erro ao atualizar item da venda: {e}")
        if conexao:
            conexao.rollback()
        return False
    finally:
        if conexao:
            conexao.close()


def remover_item_venda(id_item_venda):
    """[DELETE] Remove um item específico da venda."""
    conexao = abrir_conexao()
    if not conexao:
        return False

    try:
        cursor = conexao.cursor()
        query = 'DELETE FROM "Aura Motors".item_venda WHERE id_item_venda = ?;'
        cursor.execute(query, (id_item_venda,))
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