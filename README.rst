Welcome to jinja-kit's documentation!
======================================

Collestion of utilities and extensions for jinja2.

.. image:: https://secure.travis-ci.org/lispython/jinja-kit.png
	   :target: https://secure.travis-ci.org/lispython/jinja-kit


INSTALLATION
------------

To use jinja-kit use `pip` or `easy_install`:

``pip install jinja-kit``

or

``easy_install jinja-kit``


DJANGO USAGE
------------


Added `jinja_kit.contrib.django` to your `INSTALLED_APPS`:

.. code_block::

   INSTALLED_APPS += 'jinja_kit.contrib.django',

   JINJA_FILTERTS = [
   "jinja_kit.contrib.django.filters",
   "myapp.filters"]

   JINJA_GLOBALS = [
   "jinja_kit.contrib.django.globals",
   ]

CONTRIBUTE
----------

Fork https://github.com/lispython/jinja-kit/ , create commit and pull request.

