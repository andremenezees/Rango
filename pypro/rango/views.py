from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from pypro.rango.forms import CategoryForm, PageForm, UserProfileForm, UserForm
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


@login_required()
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


@login_required()
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


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('rango:index'))

            else:
                return HttpResponse("Your Rango account is disabled.")

        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return render(request, 'rango/login_error.html')

    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return HttpResponse("Voce está logado.")


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('rango:index'))


def login_required(request):
    return render(request, 'rango/login_required_add_category.html')
