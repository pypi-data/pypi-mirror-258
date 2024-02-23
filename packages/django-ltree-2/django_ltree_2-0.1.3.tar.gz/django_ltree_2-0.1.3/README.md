# django-ltree

A tree extension implementation to support hierarchical tree-like data in Django models,
using the native Postgres extension `ltree`.

Postgresql has already a optimized and very useful tree implementation for data.
The extension is [ltree](https://www.postgresql.org/docs/9.6/static/ltree.html)

This fork contains is a continuation of the work done by [`mariocesar`](https://github.com/mariocesar/) on [`django-ltree`](https://github.com/mariocesar/django-ltree) and merges the work done by [`simkimsia`](https://github.com/simkimsia) on [`greendeploy-django-ltree`](https://github.com/GreenDeploy-io/greendeploy-django-ltree)

<!--
[![Test](https://github.com/mariocesar/django-ltree/actions/workflows/test.yml/badge.svg)](https://github.com/mariocesar/django-ltree/actions/workflows/test.yml)
 -->

## Install

```py
pip install django-ltree
```

Then add `django_ltree` to `INSTALLED_APPS` in your Django project settings.

```python
INSTALLED_APPS = [
    ...,
    'django_ltree',
    ...
]
```

And make sure to run `django_ltree` migrations before you added the `PathField`

```
python manage.py migrate django_ltree
```

`django_ltree` migrations will install the `ltree` extension if not exist.

You can alternatively specify the `django_ltree` dependency in the migrations of
your applications that requires `PathField`, and run migrations smoothly.

```python
class Migration(migrations.Migration):
    dependencies = [
            ('django_ltree', '__latest__'),
    ]
```

## Requires

-   Django 5.0 or superior
-   Python 3.10 or higher

## Testing

Make sure you have Postgres installed. Then simply run `tox` in the root directory of the project.
