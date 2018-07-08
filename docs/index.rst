fastjsonschema documentation
############################

Installation
************

.. code-block:: bash

    pip install fastjsonschema

Documentation
*************

.. automodule:: fastjsonschema
    :members:

Testing
*******

Test suite contains all tests from  `JSON-Schema-Test-Suite <https://github.com/json-schema-org/JSON-Schema-Test-Suite>`_
for draft4, draft6, and draft7. In addition there are own tests.

Running the test suite is as simple as:

.. code-block:: bash

    pytest

Some performance tests included in test suite are slow, you can skip them:

.. code-block:: bash

    pytest --benchmark-skip

Running all tests in all environments and linters, docs, etc.:

.. code-block:: bash

    tox

Running one tox envitonment, in this case docs:

    tox -e docs

Running tox test envitonments, and skip slow test:

    tox -e py34,py45,py36 -- --benchmark-skip
