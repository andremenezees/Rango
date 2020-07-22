from django.shortcuts import render

from pypro.rango.forms import CategoryForm, PageForm
from pypro.rango.models import Categoria, Pagina


def index(request):
    category_list = Categoria.objects.order_by('-likes')[:5]
    context_dict = {'categorias': category_list}

    page_list = Pagina.objects.order_by('-views')[:5]
    context_dict['paginas'] = page_list

    return render(request, 'rango/index.html', context_dict)


def about(request):
    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)
    return render(request, 'rango/about.html', {})


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


def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.views = 0
            categoria.save()
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    categoria = Categoria.objects.get(slug=category_name_slug)

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if categoria:
                page = form.save(commit=False)
                page.category = categoria
                page.likes = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'categoria': categoria}
    return render(request, 'rango/add_page.html', context_dict)
