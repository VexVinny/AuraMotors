
from django.shortcuts import render, redirect
from django.contrib import messages

# Importa as funções de cada módulo da equipe
from modulos.vendas import listar_vendas
from modulos.pessoas import listar_clientes

from modulos.estoque import (
    listar_veiculos,
    registrar_veiculo,
    atualizar_veiculo,
    remover_veiculo,
    listar_marcas,
    registrar_marca,
    atualizar_marca,
    remover_marca,
    listar_montadoras,
    registrar_montadora,
    atualizar_montadora,
    remover_montadora,
)
from modulos.vendas import (
    listar_vendas,
    buscar_venda_por_id,
    registrar_venda,
    atualizar_venda,
    remover_venda,
    listar_itens_da_venda,
    adicionar_item_venda,
    remover_item_venda
)

def view_vendas(request):
    mensagem = None
    erro = None
    venda_para_editar = None
    venda_selecionada_id = request.GET.get('venda_id')

    if request.method == 'POST':
        acao = request.POST.get('acao')

        if acao == 'cadastrar':
            id_cliente = request.POST.get('id_cliente')
            id_colaborador = request.POST.get('id_colaborador')
            valor_total = request.POST.get('valor_total')

            if id_cliente and id_colaborador and valor_total:
                if registrar_venda(valor_total, id_cliente, id_colaborador):
                    mensagem = "Venda cadastrada com sucesso!"
                else:
                    erro = "Erro ao registrar a venda no banco de dados."
            else:
                erro = "Preencha todos os campos."

        elif acao == 'atualizar':
            id_venda = request.POST.get('id_venda')
            id_cliente = request.POST.get('id_cliente')
            id_colaborador = request.POST.get('id_colaborador')
            valor_total = request.POST.get('valor_total')

            if id_venda and id_cliente and id_colaborador and valor_total:
                if atualizar_venda(id_venda, valor_total, id_cliente, id_colaborador):
                    mensagem = f"Venda ID #{id_venda} atualizada com sucesso!"
                else:
                    erro = "Erro ao atualizar a venda no banco de dados."
            else:
                erro = "Preencha todos os campos para atualizar."

        elif acao == 'excluir':
            id_venda = request.POST.get('id_venda')
            if id_venda:
                if remover_venda(id_venda):
                    mensagem = f"Venda ID #{id_venda} (e seus itens) cancelada com sucesso!"
                else:
                    erro = "Erro ao remover a venda do banco de dados."

        elif acao == 'adicionar_item':
            id_venda = request.POST.get('id_venda')
            id_veiculo = request.POST.get('id_veiculo')
            valor_unitario = request.POST.get('valor_unitario')

            if id_venda and id_veiculo and valor_unitario:
                if adicionar_item_venda(id_venda, id_veiculo, valor_unitario):
                    mensagem = "Item adicionado à venda com sucesso!"
                    venda_selecionada_id = id_venda
                else:
                    erro = "Erro ao adicionar o item na venda."

        elif acao == 'remover_item':
            id_item_venda = request.POST.get('id_item_venda')
            id_venda = request.POST.get('id_venda')
            if id_item_venda:
                if remover_item_venda(id_item_venda):
                    mensagem = "Item removido da venda com sucesso!"
                    venda_selecionada_id = id_venda
                else:
                    erro = "Erro ao remover o item da venda."

    editar_id = request.GET.get('editar_id')
    if editar_id:
        venda_para_editar = buscar_venda_por_id(editar_id)

    vendas = listar_vendas()

    itens_venda = []
    if venda_selecionada_id:
        itens_venda = listar_itens_da_venda(venda_selecionada_id)

    contexto = {
        'vendas': vendas,
        'venda_para_editar': venda_para_editar,
        'venda_selecionada_id': venda_selecionada_id,
        'itens_venda': itens_venda,
        'mensagem': mensagem,
        'erro': erro
    }
    return render(request, 'vendas.html', contexto)


def view_estoque(request):
    """View do módulo de estoque, veículos, marcas e montadoras."""

    if request.method == "POST":
        acao = request.POST.get("acao")

        try:
            sucesso = False

            # VEÍCULOS
            if acao == "inserir_veiculo":
                sucesso = registrar_veiculo(
                    request.POST["modelo"],
                    int(request.POST["ano"]),
                    float(request.POST["preco"]),
                    request.POST["status"],
                    int(request.POST["id_montadora"]),
                    int(request.POST["id_marca"]),
                    int(request.POST["id_categoria"]),
                )

            elif acao == "atualizar_veiculo":
                sucesso = atualizar_veiculo(
                    int(request.POST["id_veiculo"]),
                    modelo=request.POST["modelo"],
                    ano=int(request.POST["ano"]),
                    preco=float(request.POST["preco"]),
                    status=request.POST["status"],
                    id_montadora=int(request.POST["id_montadora"]),
                    id_marca=int(request.POST["id_marca"]),
                    id_categoria=int(request.POST["id_categoria"]),
                )

            elif acao == "remover_veiculo":
                sucesso = remover_veiculo(
                    int(request.POST["id_veiculo"])
                )

            # MARCAS
            elif acao == "inserir_marca":
                sucesso = registrar_marca(
                    request.POST["nome_marca"].strip()
                )

            elif acao == "atualizar_marca":
                sucesso = atualizar_marca(
                    int(request.POST["id_marca"]),
                    request.POST["nome_marca"].strip()
                )

            elif acao == "remover_marca":
                sucesso = remover_marca(
                    int(request.POST["id_marca"])
                )

            # MONTADORAS
            elif acao == "inserir_montadora":
                sucesso = registrar_montadora(
                    request.POST["nome_montadora"].strip()
                )

            elif acao == "atualizar_montadora":
                sucesso = atualizar_montadora(
                    int(request.POST["id_montadora"]),
                    request.POST["nome_montadora"].strip()
                )

            elif acao == "remover_montadora":
                sucesso = remover_montadora(
                    int(request.POST["id_montadora"])
                )

            # MENSAGENS DO RESULTADO
            if sucesso:
                messages.success(
                    request,
                    "Operação realizada com sucesso!"
                )
            else:
                messages.error(
                    request,
                    "Não foi possível realizar a operação. "
                    "Verifique os dados ou os registros relacionados."
                )

        except (ValueError, KeyError):
            messages.error(
                request,
                "Dados inválidos. Confira os campos preenchidos."
            )

        return redirect("estoque")

    # CARREGA OS DADOS PARA A PÁGINA
    contexto = {
        "veiculos": listar_veiculos(),
        "marcas": listar_marcas(),
        "montadoras": listar_montadoras(),
    }

    return render(request, "estoque.html", contexto)


def view_pessoas(request):
    """View do módulo de pessoas."""
    clientes = listar_clientes()

    contexto = {
        "clientes": clientes
    }

    return render(request, "pessoas.html", contexto)
