from django.test import Client


def test_status_code(client: Client):
    resp = client.get('/rango/about')
    assert resp.status_code == 200
