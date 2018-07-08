===========================
Fast JSON schema for Python
===========================

|PyPI| |Pythons|

.. |PyPI| image:: https://img.shields.io/pypi/v/fastjsonschema.svg
   :alt: PyPI version
   :target: https://pypi.python.org/pypi/fastjsonschema

.. |Pythons| image:: https://img.shields.io/pypi/pyversions/fastjsonschema.svg
   :alt: Supported Python versions
   :target: https://pypi.python.org/pypi/fastjsonschema

This project was made to come up with fast JSON validations. It is at
least an order of magnitude faster than other Python implemantaions.
See `documentation <https://seznam.github.io/python-fastjsonschema/>`_ for
performance test details.

Current version is implementation of `json-schema <http://json-schema.org/>`_
draft-04, draft-06, and draft-07.
Note that there are some differences compared to JSON schema standard:

* Regular expressions are full Python ones, not only what JSON schema
  allows. It's easier to allow everything and also it's faster to
  compile without limits. So keep in mind that when you will use more
  advanced regular expression, it may not work with other library.
* JSON schema says you can use keyword ``default`` for providing default
  values. This implementation uses that and always returns transformed
  input data.

Features
--------

* Compatible with draft-04, draft-06, and draft-07
* Fast validation
* Commandline usage
* Validation function as code
* Easy to extend

Install
-------

.. code-block:: bash

    pip install fastjsonschema

Support for Python 3.4 and higher.

Documentation
-------------

Documentation: `https://seznam.github.io/python-fastjsonschema/
<https://seznam.github.io/python-fastjsonschema/>`_
