from django.contrib.auth.models import User

from pypro.rango.models import Categoria, Pagina, UserProfile
from django import forms


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Digite o nome da categoria escolhida.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(initial=0, help_text="Digite o numero de likes.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Categoria
        fields = ('name', 'likes')


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="Digite o título da página.")
    url = forms.URLField(max_length=200,
                         help_text="Informe o URL da página.")
    views = forms.IntegerField(initial=0, help_text="Digite o numero de views.")
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Pagina
        exclude = ('category',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    website = forms.URLField(required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
