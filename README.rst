===================
maskinporten_client
===================


.. image:: https://img.shields.io/pypi/v/maskinporten_client.svg
        :target: https://pypi.python.org/pypi/maskinporten_client

.. image:: https://img.shields.io/travis/samuelberntzen/maskinporten_client.svg
        :target: https://travis-ci.com/samuelberntzen/maskinporten_client

.. image:: https://readthedocs.org/projects/maskinporten-client/badge/?version=latest
        :target: https://maskinporten-client.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

Python library for instantiating a client which authenticates to Maskinporten using private/public key pair. 

Installation:
"pip install git+https://github.com/samuelberntzen/maskinporten-client-python.git"

Usage:

.. code-block:: python


    import requests
    from maskinporten_client.core.Client import MaskinportenClient
    from maskinporten_client.utils.loaders import load_private_key_from_json
    
    # Dev 
    private_key_json = load_private_key_from_json('private_key_dev.json') # Change path as needed
    token_url = "https://ver2.maskinporten.no/token" # dev
    audience = 'https://ver2.maskinporten.no/' # dev
    issuer = <dev-integration-id> # dev
    
    # Prod
    private_key_json = load_private_key_from_json('private_key_prod.json') # Change path as needed
    token_url = "https://maskinporten.no/token" # prod
    audience = 'https://maskinporten.no/' # prod
    issuer = <prod-integration-id> # porod
    # Common
    consumer_organization = <organization_id>
    scopes = ['ks:fiks'] # or other scope defined in Maskinporten
    
    
    maskinporten = MaskinportenClient(
        token_url=token_url,
        private_key_json = private_key_json,
        scopes = scopes, 
        audience = audience,
        issuer = issuer,
        consumer_organization = consumer_organization
    )
    
    maskinporten.get_access_token()


* Free software: MIT license
* Documentation: https://maskinporten-client.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
