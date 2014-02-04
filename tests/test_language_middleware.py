#!/usr/bin/env python
# encoding: utf-8
import os
import unittest

import mock

from language_middleware import LanguageMiddleware


class TestLanguageMiddleware(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = mock.Mock(side_effect=lambda x, y: 'Some text ;)')
    
    def test_get_language_from_url_with_language(self):
        language_middleware = LanguageMiddleware(self.app)
        environ = {'PATH_INFO': '/es/ok'}
        language_middleware.__call__(environ, None)
        self.assertEquals('es', environ['HTTP_ACTIVE_LANGUAGE'])
        self.assertEquals('/ok', environ['PATH_INFO'])

    def test_get_language_from_url_without_language(self):
        language_middleware = LanguageMiddleware(self.app)
        environ = {'PATH_INFO': '/documents/1'}
        language_middleware.__call__(environ, None)
        self.assertEquals('en', environ['HTTP_ACTIVE_LANGUAGE'])
        self.assertEquals('/documents/1', environ['PATH_INFO'])

    def test_get_language_from_headers(self):
        language_middleware = LanguageMiddleware(self.app)
        environ = {'PATH_INFO': '/documents/1', 'HTTP_ACCEPT_LANGUAGE': 'es-cl,es;q=0.5'}
        language_middleware.__call__(environ, None)
        self.assertEquals('es', environ['HTTP_ACTIVE_LANGUAGE'])
    
    def test_default_language_should_be_in_valid_languages(self):
        self.assertRaises(Exception, LanguageMiddleware, self.app, 'fr')
    
    def test_get_language_using_another_default_language(self):
        language_middleware = LanguageMiddleware(
            self.app,
            default_language = 'fr',
            valid_languages = ('en', 'es', 'fr')
        )
        environ = {}
        language_middleware.__call__(environ, None)
        self.assertEquals('fr', environ['HTTP_ACTIVE_LANGUAGE'])
    
    def test_get_language_but_do_not_remove_language_part_from_url(self):
        language_middleware = LanguageMiddleware(
            self.app,
            default_language = 'fr',
            valid_languages = ('en', 'es', 'fr'),
            clean_url = False
        )
        environ = {'PATH_INFO': '/es/documents'}
        language_middleware.__call__(environ, None)
        self.assertEquals('es', environ['HTTP_ACTIVE_LANGUAGE'])
        self.assertEquals('/es/documents', environ['PATH_INFO'])
        
    def test_use_correct_locale(self):
        def html(environ, start_response):
            from mako.template import Template
            return Template("${_('Hello World')}").render()
        locale_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures/locale')
        language_middleware = LanguageMiddleware(
            html,
            default_language = 'fr',
            valid_languages = ('en', 'es', 'fr'),
            clean_url = False,
            locale_path = locale_path,
            locale_name = 'hello'
        )
        spanish_response = language_middleware.__call__({'PATH_INFO': '/es/documents'}, None)
        english_response = language_middleware.__call__({'PATH_INFO': '/en/documents'}, None)
        self.assertEquals('Hola Mundo', spanish_response)
        self.assertEquals('Hello World', english_response)

    
if __name__ == '__main__':
    unittest.main()