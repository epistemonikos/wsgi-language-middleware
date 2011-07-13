#!/usr/bin/env python
# encoding: utf-8
'''
test_language_middleware.py
'''

import unittest

from ludibrio import Stub, any

from language_middleware import LanguageMiddleware

class TestLanguageMiddleware(unittest.TestCase):
	def setUp(self):
	    with Stub() as app:
	        app(any(), any()) >> 'Some text ;)'
	    self.app = app
	
	def test_get_language_from_url_with_language(self):
	    language_middleware = LanguageMiddleware(self.app)
	    environ = {'PATH_INFO': '/es/ok'}
	    language_middleware.__call__(environ, None)
	    self.assertEquals('es', environ['ACTIVE_LANGUAGE'])
	    self.assertEquals('/ok', environ['PATH_INFO'])

	def test_get_language_from_url_without_language(self):
	    language_middleware = LanguageMiddleware(self.app)
	    environ = {'PATH_INFO': '/documents/1'}
	    language_middleware.__call__(environ, None)
	    self.assertEquals('en', environ['ACTIVE_LANGUAGE'])
	    self.assertEquals('/documents/1', environ['PATH_INFO'])

	def test_get_language_from_headers(self):
	    language_middleware = LanguageMiddleware(self.app)
	    environ = {'PATH_INFO': '/documents/1', 'HTTP_ACCEPT_LANGUAGE': 'es-cl,es;q=0.5'}
	    language_middleware.__call__(environ, None)
	    self.assertEquals('es', environ['ACTIVE_LANGUAGE'])
	
	def test_default_language_should_be_in_valid_languages(self):
	    self.assertRaises(Exception, LanguageMiddleware, self.app, 'fr')
	
	def test_get_language_using_another_default_language(self):
	    language_middleware = LanguageMiddleware(self.app, default_language = 'fr', valid_languages = ('en', 'es', 'fr'))
	    environ = {}
	    language_middleware.__call__(environ, None)
	    self.assertEquals('fr', environ['ACTIVE_LANGUAGE'])
    
if __name__ == '__main__':
	unittest.main()