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

This project was made to come up with fast `JSON Schema <http://json-schema.org/>`_
validations. See `documentation <https://seznam.github.io/python-fastjsonschema/>`_
for performance test details.

Current version is complete an implementation of the JSON Schema
`Draft v4 <https://tools.ietf.org/html/draft-zyp-json-schema-04>`_,
`Draft v6 <https://tools.ietf.org/html/draft-wright-json-schema-01>`_
and `Draft v7 <https://tools.ietf.org/html/draft-handrews-json-schema-validation-00>`_,
specifications.
It passes 100% of the `official JSON Schema Test Suite
<https://github.com/json-schema-org/JSON-Schema-Test-Suite>`_

Features
--------

* 100% compatible with draft-04, draft-06, and draft-07
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
