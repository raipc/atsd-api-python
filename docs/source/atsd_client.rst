atsd_client
===========

connection parameters could be specified in property file
(default `connection.properties`)

For example:

.. code-block:: python

    base_url=http://atsd_server:8088
    username=username
    password=password

connect to ATSD using parameters specified in `connection.properties` file

.. code-block:: python

    >>>atsd_client.connect()

connect to atsd using credentials

.. code-block:: python

    >>>atsd_client.connect_url('http://atsd_server:8088',
                               username='username',
                               password='password')

.. autofunction:: atsd_client.connect

.. autofunction:: atsd_client.connect_url

.. toctree::

    atsd_client.services
    atsd_client.models
    atsd_client.exceptions
