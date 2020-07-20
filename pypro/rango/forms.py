from pypro.rango.models import Categoria, Pagina
from django import forms


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Por favor digite o nome da categoria escolhida.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Categoria
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="Por favor digite o título da página.")
    url = forms.URLField(max_length=200,
                         help_text="Por favor informe o URL da página.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Pagina
        exclude = ('category',)

