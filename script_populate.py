import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'pypro.settings')

import django

django.setup()

from pypro.rango.models import Categoria, Pagina


def populate():
    python_cat = add_cat('Python', views=1280, likes=640)

    add_page(cat=python_cat,
             title="Official Python Tutorial",
             url="http://docs.python.org/2/tutorial/",
             views=300,
             likes=100)

    add_page(cat=python_cat,
             title="How to Think like a Computer Scientist",
             url="http://www.greenteapress.com/thinkpython/",
             views=150,
             likes=125)

    add_page(cat=python_cat,
             title="Learn Python in 10 Minutes",
             url="http://www.korokithakis.net/tutorials/python/",
             views=30,
             likes=10)

    django_cat = add_cat("Django", views=640, likes=320)

    add_page(cat=django_cat,
             title="Official Django Tutorial",
             url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/",
             views=150,
             likes=30)

    add_page(cat=django_cat,
             title="Django Rocks",
             url="http://www.djangorocks.com/",
             views=200,
             likes=50)

    add_page(cat=django_cat,
             title="How to Tango with Django",
             url="http://www.tangowithdjango.com/",
             views=222,
             likes=130)

    frame_cat = add_cat("Other Frameworks", views=320, likes=160)

    add_page(cat=frame_cat,
             title="Bottle",
             url="http://bottlepy.org/docs/dev/",
             views=144,
             likes=77)

    add_page(cat=frame_cat,
             title="Flask",
             url="http://flask.pocoo.org",
             views=20,
             likes=5)

    # Print out what we have added to the user.
    for c in Categoria.objects.all():
        for p in Pagina.objects.filter(category=c):
            print(f"{(str(c))} - {str(p)}")


def add_page(cat, title, url, views=0, likes=0):
    p = Pagina.objects.get_or_create(category=cat, title=title, url=url, views=views, likes=likes)[0]
    p.url = url
    p.views = views
    p.likes = likes
    p.save()
    return p


def add_cat(name, views=0, likes=0):
    c = Categoria.objects.get_or_create(name=name, views=views, likes=likes)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
