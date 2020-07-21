import pytest
from django.test import Client
from django.urls import reverse

from pypro.django_assertions import assert_contains


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

