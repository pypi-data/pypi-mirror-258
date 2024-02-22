========================
pytest-fixturecollection
========================

.. image:: https://img.shields.io/pypi/v/pytest-fixturecollection.svg
    :target: https://pypi.org/project/pytest-fixturecollection
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-fixturecollection.svg
    :target: https://pypi.org/project/pytest-fixturecollection
    :alt: Python versions

.. image:: https://ci.appveyor.com/api/projects/status/github/jyejare/pytest-fixturecollection?branch=master
    :target: https://ci.appveyor.com/project/jyejare/pytest-fixturecollection/branch/master
    :alt: See Build Status on AppVeyor

A pytest plugin to collect tests based on fixtures being used in tests

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

* Filter tests collection/execution based on fixtures being used by tests
* One or more number(comma separated) of fixtures are supported with option `--uses-fixtures`

One can combine fixture based collection with pytests default options/plugins for further smart collection.

Requirements
------------

* Python >= 3.9
* Pytest >= 3.5



Installation
------------

You can install "pytest-fixturecollection" via `pip`_ from `PyPI`_::

    $ pip install pytest-fixturecollection


Usage
-----


Once plugin is installed, run pytest command with "--uses-fixtures" option as shown below::

    # pytest --uses-fixtures fixture1,fixture2 tests/


Explanation: All the tests using `fixture1` or `fixture2` inside tests directory would be collected and executed and rest tests would be uncollected (not executed). You can also choose to just `--collect-only` to view what tests are collected.

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `BSD-3`_ license, "pytest-fixturecollection" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/jyejare/pytest-fixturecollection/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
