from django.shortcuts import render
from pypro.rango.models import Categoria, Pagina


def index(request):
    category_list = Categoria.objects.order_by('-likes')[:5]
    context_dict = {'categorias': category_list}

    page_list = Pagina.objects.order_by('-views')[:5]
    context_dict['paginas'] = page_list

    return render(request, 'rango/index.html', context_dict)


def about(request):
    return render(request, 'rango/about.html')



def all_categories(request):
    category_list = Categoria.objects.order_by('-likes')[:100000]
    context_dict = {'categorias': category_list}

    return render(request, 'rango/categorias.html', context_dict)


def all_paginas(request):
    page_list = Pagina.objects.order_by('-likes')[:100000]
    context_dict = {'paginas': page_list}

    return render(request, 'rango/paginas.html', context_dict)


def show_category(request, category_name_slug):

    context_dict = {}
    try:
        categoria = Categoria.objects.get(slug=category_name_slug)
        paginas = Pagina.objects.filter(category=categoria)

        context_dict['paginas'] = paginas
        context_dict['categoria'] = categoria

    except Categoria.DoesNotExist:
        context_dict['categoria'] = None
        context_dict['paginas'] = None

    return render(request, 'rango/category.html', context_dict)

