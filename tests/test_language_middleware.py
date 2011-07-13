#!/usr/bin/env python
# encoding: utf-8
"""
test_language_middleware.py
"""

import unittest

from ludibrio import Stub, any

from language_middleware import LanguageMiddleware

class test_language_middleware(unittest.TestCase):
	def setUp(self):
	    with Stub() as app:
	        app(any(), any()) >> "Some text ;)"
	    self.app = app
	
	def test_get_language_from_url_with_language(self):
	    language_middleware = LanguageMiddleware(self.app)
	    environ = {'PATH_INFO': '/es/ok'}
	    language_middleware.__call__(environ, None)
	    self.assertEquals("es", environ['ACTIVE_LANGUAGE'])

	def test_get_language_from_url_without_language(self):
	    language_middleware = LanguageMiddleware(self.app)
	    environ = {'PATH_INFO': '/documents/1'}
	    language_middleware.__call__(environ, None)
	    self.assertEquals("en", environ['ACTIVE_LANGUAGE'])

	def test_get_language_from_url_without_language(self):
	    language_middleware = LanguageMiddleware(self.app)
	    environ = {'PATH_INFO': '/documents/1', 'HTTP_ACCEPT_LANGUAGE': 'es-cl,es;q=0.5'}
	    language_middleware.__call__(environ, None)
	    self.assertEquals("es", environ['ACTIVE_LANGUAGE'])
    
if __name__ == '__main__':
	unittest.main()