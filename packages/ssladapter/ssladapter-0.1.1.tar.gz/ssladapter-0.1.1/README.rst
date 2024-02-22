.. ssladapter:

===================
SSL Adapter Package
===================

Overview
--------

SSL Adapter is a Python package that provides utilities for handling SSL connections and creating sessions with SSL adapters.

Installation
------------

Install Your Package Name using pip:

.. code-block:: bash

    pip install ssladapter

Usage
-----

Creating a Session with SSL Adapter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a session with an SSL adapter, you can use the ``session_ssl_adapter`` function provided by the package.

.. code-block:: python

    from ssladapter.entry import session_ssl_adapter

    # Create a session with SSL adapter
    session = session_ssl_adapter(
        certfile='/path/to/client_certificate.pem',
        keyfile='/path/to/client_private_key.pem',
        password='your_password', # Optional
        cacertfile='/path/to/ca_certificate.pem' # Optional
    )

    # Use the session for making requests
    response = session.get('https://example.com/api')

Creating an SSL Adapter
~~~~~~~~~~~~~~~~~~~~~~~~

Alternatively, you can directly create an instance of the ``SSLAdapter`` class and use it to customize a session with SSL configuration.

.. code-block:: python

    from ssladapter.ssl_adapter import SSLAdapter
    from requests import Session

    # Create an SSL adapter instance
    ssl_adapter = SSLAdapter(
        certfile='/path/to/client_certificate.pem',
        keyfile='/path/to/client_private_key.pem',
        password='your_password', # Optional
        cacertfile='/path/to/ca_certificate.pem' # Optional
    )

    # Create a session and mount the SSL adapter
    session = Session()
    session.mount('https://', ssl_adapter)

    # Use the session for making requests
    response = session.get('https://example.com/api')
