from django.shortcuts import render

# Importa as funções de cada módulo da equipe
from modulos.vendas import listar_vendas
from modulos.pessoas import listar_clientes
from modulos.estoque import listar_veiculos


def view_vendas(request):
    """View do Módulo de Vendas (Sua responsabilidade)"""
    vendas = listar_vendas()
    contexto = {
        'vendas': vendas
    }
    return render(request, 'vendas.html', contexto)


def view_pessoas(request):
    """View do Módulo de Pessoas (Responsabilidade do Colega 1)"""
    clientes = listar_clientes()
    contexto = {
        'clientes': clientes
    }
    return render(request, 'pessoas.html', contexto)


def view_estoque(request):
    """View do Módulo de Estoque/Veículos (Responsabilidade do Colega 2)"""
    veiculos = listar_veiculos()
    contexto = {
        'veiculos': veiculos
    }
    return render(request, 'estoque.html', contexto)