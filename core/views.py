
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


def view_vendas(request):
    """View do módulo de vendas."""
    vendas = listar_vendas()

    contexto = {
        "vendas": vendas
    }

    return render(request, "vendas.html", contexto)


def view_pessoas(request):
    """View do módulo de pessoas."""
    clientes = listar_clientes()

    contexto = {
        "clientes": clientes
    }

    return render(request, "pessoas.html", contexto)


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
