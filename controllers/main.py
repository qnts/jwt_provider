# -*- coding: utf-8 -*-
import logging
import json
import jwt
import datetime
import werkzeug
from odoo import http
from odoo.http import request, Response
from pprint import pprint
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import UserError
# from urllib.parse import urlparse
# from urllib.parse import urlunparse
# try:
#     from oauthlib.oauth2.rfc6749 import errors
#     from oauthlib.common import urlencode, urlencoded, quote
# except Exception as e:
#     pass

from ..validator import validator

_logger = logging.getLogger(__name__)

return_fields = ['id', 'login', 'name', 'company_id']

class JwtProvider(http.Controller):
    # def _get_escaped_full_path(self, request):
    #     """
    #     Django considers "safe" some characters that aren't so for oauthlib. We have to search for
    #     them and properly escape.
    #     TODO: is it correct for odoo?
    #     """
    #     parsed = list(urlparse(request.httprequest.path))
    #     unsafe = set(c for c in parsed[4]).difference(urlencoded)
    #     for c in unsafe:
    #         parsed[4] = parsed[4].replace(c, quote(c, safe=''))

    #     return urlunparse(parsed)

    # def _extract_params(self, request, post_dict):
    #     """
    #     Extract parameters from the Django request object. Such parameters will then be passed to
    #     OAuthLib to build its own Request object
    #     """
    #     uri = self._get_escaped_full_path(request)
    #     http_method = request.httprequest.method

    #     headers = dict(list(request.httprequest.headers.items()))
    #     if 'wsgi.input' in headers:
    #         del headers['wsgi.input']
    #     if 'wsgi.errors' in headers:
    #         del headers['wsgi.errors']
    #     if 'HTTP_AUTHORIZATION' in headers:
    #         headers['Authorization'] = headers['HTTP_AUTHORIZATION']
    #     body = urlencode(list(post_dict.items()))
    #     return uri, http_method, body, headers

    def parse_request(self):
        http_method = request.httprequest.method
        try:
            body = http.request.params
        except Exception:
            body = {}

        headers = dict(list(request.httprequest.headers.items()))
        if 'wsgi.input' in headers:
            del headers['wsgi.input']
        if 'wsgi.errors' in headers:
            del headers['wsgi.errors']
        if 'HTTP_AUTHORIZATION' in headers:
            headers['Authorization'] = headers['HTTP_AUTHORIZATION']

        # extract token
        token = ''
        if 'Authorization' in headers:
            try:
                # Bearer token_string
                token = headers['Authorization'].split(' ')[1]
            except Exception:
                pass

        return http_method, body, headers, token

    def response(self, data=None, message=None, status=True, http=200):
        # headers = [
        #     ('Access-Control-Allow-Origin', '*'),
        #     ('Content-Type', 'application/json'),
        #     ('Accept', 'application/json'),
        # ]
        response = {
            'status': status,
            'data': data,
            'message': message
        }
        return response
    
    def json_response(self, **kw):
        res = self.response(**kw)

        return {
            'id': None,
            'result': res
        }

    @http.route('/api/v1/info', auth='public')
    def index(self, **kw):
        return 'Hello, world'

    def get_state(self):
        return {
            'd': request.session.db
        }

    @http.route('/api/v1/login', type='json', auth='public', csrf=False, cors='*')
    def login(self, **kw):
        # uri, http_method, body, headers = self._extract_params(request, kw)
        http_method, body, headers, token = self.parse_request()

        return self.do_login(body['login'], body['password'])
    
    def do_login(self, login, password):
        # get current db
        state = self.get_state()
        uid = request.session.authenticate(state['d'], login, password)
        if not uid:
            return self.response(message='incorrect login', status=False)
        # login success, generate token
        user = request.env.user.read(return_fields)[0]
        token = validator.create_token(user)
        return self.response(data={ 'user': user, 'token': token })

    @http.route('/api/v1/me', type='json', auth='public', csrf=False, cors='*')
    def me(self, **kw):
        http_method, body, headers, token = self.parse_request()
        result = validator.verify_token(token)
        if not result['status']:
            return self.response(status=False, message=result['message'])

        user = request.env.user.read()[0]
        return self.response(user)

    @http.route('/api/v1/logout', type='json', auth='public', csrf=False, cors='*')
    def logout(self, **kw):
        http_method, body, headers, token = self.parse_request()
        result = validator.verify_token(token)
        if not result['status']:
            return self.response(status=False, message=result['message'])

        self._logout(token)
        return self.response()

    def _logout(self, token):
        request.session.logout()
        request.env['jwt.access_token'].sudo().search([
            ('token', '=', token)
        ]).unlink()

    @http.route('/api/v1/register', type='json', auth='public', csrf=False, cors='*')
    def register(self, **kw):
        http_method, body, headers, token = self.parse_request()

        values = body.copy()

        # validate body
        if not validator.is_valid_email(values.get('login')):
            return self.response(status=False, message='email-invalid')
        # user = request.env['res.users'].sudo().search([('login', '=', values.get('login'))])

        # if user:
        #     return self.response(status=False, message='email-existed')

        if not values.get('name'):
            return self.response(status=False, message='name-empty')

        if not values.get('password'):
            return self.response(status=False, message='password-empty')

        supported_langs = [lang['code'] for lang in request.env['res.lang'].sudo().search_read([], ['code'])]
        if request.lang in supported_langs:
            values['lang'] = request.lang
        
        # sign up
        try:
            self._signup_with_values(values)
        except (SignupError, AssertionError) as e:
            if request.env["res.users"].sudo().search([("login", "=", values.get("login"))]):
                return self.response(status=False, message='email-existed')
            else:
                _logger.error("%s", e)
                return self.response(status=False, message='signup-disabled')

        # log the user in
        return self.do_login(values.get('login'), values.get('password'))

    def _signup_with_values(self, values):
        db, login, password = request.env['res.users'].sudo().signup(values, None)
        request.env.cr.commit()     # as authenticate will use its own cursor we need to commit the current transaction
        self.signup_email(values)
    
    def signup_email(self, values):
        user_sudo = request.env['res.users'].sudo().search([('login', '=', values.get('login'))])
        template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
        if user_sudo and template:
            template.sudo().with_context(
                lang=user_sudo.lang,
                auth_login=werkzeug.url_encode({'auth_login': user_sudo.email}),
            ).send_mail(user_sudo.id, force_send=True)