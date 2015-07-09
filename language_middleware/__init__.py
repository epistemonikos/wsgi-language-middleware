# -*- coding: utf-8 -*-
import gettext
import os
import re


class LanguageMiddleware(object):
    def __init__(
        self,
        app,
        default_language='en',
        valid_languages=('en', 'es'),
        force_lang=False,
        clean_url=True,
        locale_path=None,
        locale_name=None,
        set_script_name=False,
        do_gettext_install=True
    ):
        if default_language not in valid_languages:
            raise Exception("Default language must be contained in valid languages")

        self.app = app
        self.default_language = default_language
        self.valid_languages = valid_languages
        self.force_lang = force_lang
        self.clean_url = clean_url
        self.locale_path = locale_path
        self.locale_name = locale_name
        self.set_script_name = set_script_name
        self.do_gettext_install = do_gettext_install

    def _validate_language(self, language):
        if language and language in self.valid_languages:
            return language

    def _get_url_language(self, environ):
        could_have_language = environ.get('PATH_INFO', '')[0:4]
        if len(could_have_language) == 3:
            could_have_language += "/"
        language = re.findall('\/([a-z]{2,2})\/', could_have_language)
        if len(language) > 0:
            if self.clean_url:
                environ['PATH_INFO'] = environ['PATH_INFO'][3:]  # Remove language from url
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
            environ['HTTP_ACTIVE_LANGUAGE'] = url_language
        else:
            headers_language = self._get_headers_language(environ)
            if headers_language and self._validate_language(headers_language) and not self.force_lang:
                environ['HTTP_ACTIVE_LANGUAGE'] = headers_language
            else:
                environ['HTTP_ACTIVE_LANGUAGE'] = self.default_language
        if self.do_gettext_install and self.locale_path and self.locale_name:
            if os.path.exists(os.path.join(self.locale_path, environ['HTTP_ACTIVE_LANGUAGE'], "LC_MESSAGES")):
                translation = gettext.translation(
                    self.locale_name,
                    self.locale_path,
                    languages=[environ['HTTP_ACTIVE_LANGUAGE']],
                    codeset="utf-8"
                )
                translation.install(unicode=True)
        if self.set_script_name:
            environ['SCRIPT_NAME'] = "/%s" % environ['HTTP_ACTIVE_LANGUAGE']
        return self.app(environ, start_response)
