"""pypro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from pypro.rango import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  re_path(r'^$', views.index, name='index'),
                  re_path(r'^about/$', views.about, name='about'),
                  re_path(r'^categoria/(?P<category_name_slug>[\w\-]+)/$',
                          views.show_category, name='show_category'),
                  re_path(r'^categorias/', views.all_categories, name='all_categories'),
                  re_path(r'^pagina/', views.all_paginas, name='all_paginas')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(
        path('__debug__/', include(debug_toolbar.urls))
    )
