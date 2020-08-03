from django.conf import settings
from django.conf.urls.static import static
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
    re_path(r'search/$', views.search, name='search'),
    re_path('register_profile/', views.register_profile, name='register_profile'),
    re_path(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    re_path('profiles/', views.list_profiles, name='list_profiles'),
    re_path('goto/', views.track_url, name='goto'),
    re_path('like_category/', views.like_category, name='like_category'),
    re_path('suggest/', views.suggest_category, name='suggest_category'),
    re_path('add/', views.auto_add_page, name='auto_add_page'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
