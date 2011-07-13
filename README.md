# WSGI Language Middleware 

## Why?

This Wsgi middleware, takes the language from urls similiar to "/es/documents" or from the Accept language header.

## Instalation

### Prerequisites:

* Python >= 2.6
* Ludibrio (for the tests)

### Install

	python setup.py install

## Test

	nosetests
	
## Usage
    from language_middleware import LanguageMiddleware
    application = my_wsgi_app()
    application = LanguageMiddleware(application, default_language = 'es', valid_languages = ('en', 'es', 'fr'))

Call to the url **/fr/documents**, and my_wsgi_app will receive:

    environ['PATH_INFO'] = '/documents'
    environ['ACTIVE_LANGUAGE'] = 'fr'

Call to the url **/documents/1**, and my_wsgi_app will receive:

    environ['PATH_INFO'] = '/documents/1'
    environ['ACTIVE_LANGUAGE'] = 'es'
