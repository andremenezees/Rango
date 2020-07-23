from django.contrib import admin

from pypro.rango.models import Categoria, Pagina, UserProfile

admin.site.register(UserProfile)


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Pagina, PageAdmin)
