import pytest
from django.urls import reverse

from pypro.django_assertions import assert_contains


@pytest.fixture
def resp(client, db):
    resp = client.get(reverse('rango:index'))
    return resp


def test_status_code(resp):
    assert resp.status_code == 200


def test_title(resp):
    assert_contains(resp, 'Rango')


def test_index_link(resp):
    assert_contains(resp, f'href="{reverse("rango:index")}">Home</a>')


def test_image_shown(resp):
    assert_contains(resp, '<img src="')
