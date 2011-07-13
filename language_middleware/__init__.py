import re

class LanguageMiddleware(object):
    def __init__(self, app, default_language = 'en', valid_languages = ('en', 'es')):
        if default_language not in valid_languages:
            raise Exception("Default language must be contained in valid languages")
        self.app = app
        self.default_language = default_language
        self.valid_languages = valid_languages
    
    def _validate_language(self, language):
        if language and language in self.valid_languages:
            return language
    
    def _get_url_language(self, environ):
        could_have_language = environ.get('PATH_INFO', '')[0:4]
        language = re.findall('\/([a-z]{2,2})\/', could_have_language)
        if len(language) > 0:
            environ['PATH_INFO'] = environ['PATH_INFO'][3:] #Remove language from url
            return self._validate_language(language[0])
    
    def _get_headers_language(self, environ):
        accept_language = environ.get("HTTP_ACCEPT_LANGUAGE", "")
        if accept_language:
            accept_language = accept_language[0:2]
            if self._validate_language(accept_language):
                return accept_language
    
    def __call__(self, environ, start_response):
        url_language = self._get_url_language(environ)
        if url_language and self._validate_language(url_language):
            environ['ACTIVE_LANGUAGE'] = url_language
        else:
            headers_language = self._get_headers_language(environ)
            if headers_language and self._validate_language(headers_language):
                environ['ACTIVE_LANGUAGE'] = headers_language
            else:
                environ['ACTIVE_LANGUAGE'] = self.default_language
        return self.app(environ, start_response)