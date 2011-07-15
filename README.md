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
### Basic
    from language_middleware import LanguageMiddleware
    application = my_wsgi_app()
    application = LanguageMiddleware(application, default_language = 'es', valid_languages = ('en', 'es', 'fr'))

Call to the url **/fr/documents**, and my_wsgi_app will receive:

    environ['HTTP_ACTIVE_LANGUAGE'] = 'fr'

Call to the url **/documents/1**, and my_wsgi_app will receive:

    environ['HTTP_ACTIVE_LANGUAGE'] = 'es'
    
### Clean URL
The clean_url option, removes the language info from the URL.

    from language_middleware import LanguageMiddleware
    application = my_wsgi_app()
    application = LanguageMiddleware(application, default_language = 'es', valid_languages = ('en', 'es', 'fr'), clean_url = True)

Call to the url **/fr/documents**, and my_wsgi_app will receive:

    environ['PATH_INFO'] = '/documents'
    environ['HTTP_ACTIVE_LANGUAGE'] = 'fr'

Call to the url **/documents/1**, and my_wsgi_app will receive:

    environ['PATH_INFO'] = '/documents/1'
    environ['HTTP_ACTIVE_LANGUAGE'] = 'es'

### With locale
If you have the following locale directory

    /home/user/locale/es/LC_MESSAGES/hello.po
    /home/user/locale/es/LC_MESSAGES/hello.mo
    /home/user/locale/en/LC_MESSAGES/hello.po
    /home/user/locale/en/LC_MESSAGES/hello.mo

You can set an option to active the language, check the test from more info:+

IMPORTANT: **Default language locale path must exists, if not last successfully used locale will be used (if any)**

    from language_middleware import LanguageMiddleware
    application = my_wsgi_app()
    application = LanguageMiddleware(
        application,
        default_language = 'es',
        valid_languages = ('en', 'es', 'fr')
        clean_url = True,
        locale_path = '/home/user/locale',
        locale_name = 'hello'
    )