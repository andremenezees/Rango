import pytest
from django.urls import reverse
from model_mommy import mommy

from pypro.django_assertions import assert_contains
from pypro.rango.models import Categoria


@pytest.fixture
def categorias(db):
    return mommy.make(Categoria, 2, name='barakalol')


@pytest.fixture
def resp(client, db):
    resp = client.get(reverse('rango:index'))
    return resp


def test_status_code(resp):
    assert resp.status_code == 200


def test_title(resp):
    assert_contains(resp, '<title>Rango</title>')


def test_index_link(resp):
    assert_contains(resp, f'href="{reverse("rango:index")}">Home</a>')


def test_image_shown(resp):
    assert_contains(resp, '<img src="')


def test_nome_das_categorias(resp, categorias: Categoria):
    for categoria in categorias:
        assert_contains(resp, categoria.name)
