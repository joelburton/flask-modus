# -*- coding: utf-8 -*-

import sys

from werkzeug import url_decode


class Middleware(object):
    """ WSGI Method Overriding Middleware """
    
    header_key = 'HTTP_X_HTTP_METHOD_OVERRIDE'
    qs_key = '_method'
    
    allowed_methods = frozenset([
        'GET',
        'HEAD',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS'
    ])
    bodyless_methods = frozenset(['GET', 'HEAD', 'OPTIONS', 'DELETE'])

    def __init__(self, app=None, input_name=''):
        self.app = app
        self.input_name = input_name

    def __call__(self, environ, response):
        """ Extract the new method from the Query String """

        method = None
        
        # Can get from HTTP header
        if self.header_key in environ:
            method = environ[self.header_key]

        # Or from query string
        elif self.qs_key in environ.get('QUERY_STRING', ''):
            args = url_decode(environ['QUERY_STRING'])
            method = args.get(self.qs_key, '')
            
        if method:
            method = method.upper()            
            if method in self.allowed_methods:
                environ['REQUEST_METHOD'] = method
            if method in self.bodyless_methods:
                environ['CONTENT_LENGTH'] = '0'

        return self.app(environ, response)


class Modus(object):
    """ Enables Flask Method Overriding """

    def __init__(self, app=None):
        self.app = app

        if self.app:
            self.init_app(self.app)

    def init_app(self, app):
        """ Configures the Flask Overriding Middleware """

        app.wsgi_app = Middleware(app.wsgi_app)
