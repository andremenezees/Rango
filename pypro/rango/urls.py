from django.urls import re_path, path

from pypro.rango import views

app_name = 'rango'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    re_path(r'^categoria/(?P<category_name_slug>[\w\-]+)/$',
            views.show_category, name='show_category'),
    path('categorias/', views.all_categories, name='all_categories'),
    path('pagina/', views.all_paginas, name='all_paginas'),
    path('add-categoria/', views.add_category, name='add_category'),
    re_path(r'^categoria/(?P<category_name_slug>[\w\-]+)/add-pagina/$', views.add_page, name='add_page'),
    re_path('login-required/', views.login_required, name='login_required'),
]
