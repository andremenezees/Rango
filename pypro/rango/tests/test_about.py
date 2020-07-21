from django.urls import reverse


def test_status_code(client, db):
    resp = client.get(reverse('rango:about'))
    assert resp.status_code == 200
