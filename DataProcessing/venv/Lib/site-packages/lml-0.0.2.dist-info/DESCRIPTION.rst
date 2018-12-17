================================================================================
lml - Load me later. A lazy loading plugin management system.
================================================================================

.. image:: https://api.travis-ci.org/chfw/lml.svg?branch=master
   :target: http://travis-ci.org/chfw/lml

.. image:: https://codecov.io/gh/chfw/lml/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/chfw/lml

.. image:: https://readthedocs.org/projects/lml/badge/?version=latest
   :target: http://lml.readthedocs.org/en/latest/

**lml** seamlessly finds the lml based plugins from your current python
environment but loads your plugins on demand. It is designed to support
plugins that have external dependencies, especially bulky and/or
memory hungry ones. lml provides the plugin management system only and the
plugin interface is on your shoulder.

**lml** enabled applications helps your customers [#f1]_ in two ways:

#. Your customers could cherry-pick the plugins from pypi per python environment.
   They could remove a plugin using `pip uninstall` command.
#. Only the plugins used at runtime gets loaded into computer memory.

When you would use **lml** to refactor your existing code, it aims to flatten the
complexity and to shrink the size of your bulky python library by
distributing the similar functionalities across its plugins. However, you as
the developer need to do the code refactoring by yourself and lml would lend you a hand.

.. [#f1] the end developers who uses your library and packages achieve their
         objectives.

Installation
================================================================================


You can install lml via pip:

.. code-block:: bash

    $ pip install lml


or clone it and install it:

.. code-block:: bash

    $ git clone https://github.com/chfw/lml.git
    $ cd lml
    $ python setup.py install

License
================================================================================

New BSD


Change log
===========

0.0.2 - 23.10.2017
--------------------------------------------------------------------------------

#. pyexcel `#103 <https://github.com/pyexcel/pyexcel/issues/103>`_, include
   LICENSE in tar ball

0.0.1 - 30/05/2017
--------------------------------------------------------------------------------

first release



