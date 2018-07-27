from odoo import http
from odoo.http import request, Response
from .validator import validator


return_fields = ['id', 'login', 'name', 'company_id']

class JwtHttp:

    def get_state(self):
        return {
            'd': request.session.db
        }

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
    
    def do_logout(self, token):
        request.session.logout()
        request.env['jwt.access_token'].sudo().search([
            ('token', '=', token)
        ]).unlink()

    def cleanup(self):
        # Clean up things after success request
        # use logout here to make request as stateless as possible



        request.session.logout()


jwt_http = JwtHttp()