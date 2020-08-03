# noqa: E722

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from pypro.rango.forms import CategoryForm, PageForm, UserProfileForm
from pypro.rango.models import Categoria, Pagina, UserProfile
from pypro.rango.webhose_search import run_query


def index(request):
    request.session.set_test_cookie()
    category_list = Categoria.objects.order_by('-likes')[:5]
    context_dict = {'categorias': category_list}

    page_list = Pagina.objects.order_by('-views')[:5]
    context_dict['paginas'] = page_list

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context=context_dict)

    return response


def about(request):
    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)
    visitor_cookie_handler(request)
    context_dict = {'visits': request.session['visits']}
    response = render(request, 'rango/about.html', context=context_dict)

    return response


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

    context_dict['query'] = categoria.name

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our search API function to get the results list!
            result_list = run_query(query)
            context_dict['query'] = query
            context_dict['result_list'] = result_list

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
    try:
        categoria = Categoria.objects.get(slug=category_name_slug)
    except Categoria.DoesNotExist:
        categoria = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if categoria:
                page = form.save(commit=False)
                page.category = categoria
                page.likes = 0
                page.save()
                return redirect('rango:show_category', category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'categoria': categoria}
    return render(request, 'rango/add_page.html', context_dict)


# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits


def search(request):
    query = ''
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our Webhose search function to get the results list!
            result_list = run_query(query)
    context_dict = {'result_list': result_list, 'query': query}
    return render(request, 'rango/search.html', context_dict)


@login_required()
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('rango:index')
        else:
            print(form.errors)

    context_dict = {'form': form}

    return render(request, 'registration/profile_registration.html', context_dict)


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('rango:index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'website': userprofile.website, 'picture': userprofile.picture})

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)

    return render(request, 'rango/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})


@login_required
def list_profiles(request):
    # user_list = User.objects.all()
    userprofile_list = UserProfile.objects.all()
    return render(request, 'rango/list_profiles.html', {'userprofile_list': userprofile_list})


# Funcao que faz com que aumente o numero de views quando algum usuario clicar em uma das páginas
def track_url(request):
    page_id = None
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
    if page_id:
        try:
            page = Pagina.objects.get(id=page_id)
            page.views = page.views + 1
            page.save()
            return redirect(page.url)
        except:
            return HttpResponse("Page id {0} not found".format(page_id))
    print("No page_id in get string")
    return redirect(reverse('rango:index'))


# Funcao que aumenta o numero de likes ao clicar no botão de like
@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
    likes = 0
    if cat_id:
        cat = Categoria.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)


def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Categoria.objects.filter(name__istartswith=starts_with)

        if max_results > 0:
            if len(cat_list) > max_results:
                cat_list = cat_list[:max_results]
    return cat_list


def suggest_category(request):
    cat_list = []
    starts_with = ''

    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        cat_list = get_category_list(8, starts_with)

    return render(request, 'rango/cats.html', {'cats': cat_list})


@login_required
def auto_add_page(request):
    cat_id = None
    url = None
    title = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.GET.get('category_id', False)
        url = request.GET.get('url', False)
        title = request.GET.get('title', False)
        if cat_id:
            category = Categoria.objects.get(id=int(cat_id))
            pagina = Pagina.objects.get_or_create(category=category, title=title, url=url)
            paginas = Pagina.objects.filter(category=category).order_by('-views')[:10000]
            # Adds our results list to the template context under name pages.
            context_dict['paginas'] = paginas
            context_dict['pagina'] = pagina

    return render(request, 'rango/page_list.html', context_dict)


def login_required(request):
    return render(request, 'rango/login_required_add_category.html')
