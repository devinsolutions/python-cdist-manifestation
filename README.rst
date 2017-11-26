cdist manifestation
===================

A helper for writing cdist manifests in Python.

Motivation
----------

Writing complex manifests in shell can be painful and laborious. With Python and
a proper abstraction layer, we can write manifests more easily.

Usage
-----

First of all make sure your manifest is executable and contains
``#!/usr/bin/env python`` shebang.

Types
`````

To use type ``__directory``, import ``directory`` (without leading underscores)
from ``cdist_manifestation.types`` like this:

.. code-block:: python

    from cdist_manifestation.types import directory

Every type is a function accepting a single positional argument, ``object_id``
which is optional, and arbitrary amount of keyword arguments, which are the
type parameters.

So, one could create a cdist object of type ``__directory`` like this:

.. code-block:: python

    from cdist_manifestation.types import directory

    directory('/my/dir', mode=755, owner='me', parents=True)

This is equivalent to ``__directory /my/dir --mode 755 --owner me --parents``.

When you want to use the same parameter multiple times, just provide an iterable
like this:

.. code-block:: python

    from cdist_manifestation.types import user_groups

    user_groups('me', group=['group1', 'group2'])

This is equivalent to ``__user_groups me --group group1 --group group2``.

To sum it up, these are the rules for using type parameters:

- Underscores in parameter name will be implicitly converted to hyphens
- Parameter values are implicitly converted to strings, except:

  * Booleans, which simply denote a presence of a boolean parameter
  * Iterables like lists and tuples, which denote presence of multiple
    instances of the same parameter. Items of these iterables will be
    converted to strings implicitly, disregarding these exceptions.

Dependencies
````````````

Every type returns its dependency string which can be passed to ``require``
context manager from ``cdist_manifestation.dependencies``. This function
emulates behavior of ``require`` environmental variable.

For example, if creating a file depends on creating its parent directory first,
you can use ``require()`` like this:

.. code-block:: python

    from cdist_manifestation.dependencies import require
    from cdist_manifestation.types import directory, file

    my_dir = directory('/my/dir')

    with require(my_dir):
        file('/my/dir/file')

This is equivalent to:

.. code-block:: bash

    __directory /my/dir
    require="__directory/my/dir" __file /my/dir/file

You can pass multiple requirements to ``require()`` or even nest one to another.

To emulate behavior of ``CDIST_ORDER_DEPENDENCY`` environmental variable, one
can use ``order_dependency`` context manager from
``cdist_manifestation.dependencies``.

For example, if you want to create three links in the same order you've defined
them in, you can write some like this:

.. code-block:: python

    from cdist_manifestation.dependencies import order_dependency
    from cdist_manifestation.types import link

    with order_dependency():
        link('/my/link1', source='/my/source', type='symbolic')
        link('/my/link2', source='/my/source', type='symbolic')
        link('/my/link3', source='/my/source', type='symbolic')

Which is equivalent to this:

.. code-block:: bash

    CDIST_ORDER_DEPENDENCY=on __link /my/link1 --source /my/source --type symbolic
    CDIST_ORDER_DEPENDENCY=on __link /my/link2 --source /my/source --type symbolic
    CDIST_ORDER_DEPENDENCY=on __link /my/link3 --source /my/source --type symbolic

You can also nest ``order_dependency`` into ``require`` or vice versa. Nesting
``order_dependency`` into itself will not change the behavior.

Examples
--------

For more advanced configuration example, see ``example`` directory.

Limitations
-----------

This library is not designed to be thread-safe.
