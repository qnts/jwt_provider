import logging
import jwt
import datetime
from odoo import http
from odoo.http import request, Response


_logger = logging.getLogger(__name__)

SECRET_KEY = "skjdfe48ueq893rihesdio*($U*WIO$u8"

class Validator:

    def create_token(self, user):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
                'iat': datetime.datetime.utcnow(),
                'sub': user['id'],
                'company_id': 12312
            }

            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as ex:
            _logger.error(ex)
            return ex
    
    def verify_token(self, token):
        try:
            result = {
                'status': False,
                'message': None,
            }
            payload = jwt.decode(token, SECRET_KEY)
            # verify expiration
            # We don't need to verify since jwt has done it for us (which would raise a 'jwt.ExpiredSignatureError')
            # if datetime.datetime.utcnow().timestamp() > payload['exp']:
            #     return False

            # get user password
            # usr = request.env['res.users'].sudo().browse(payload['sub']).read(['password'])
            # if len(usr) == 0:
            #     result['message'] = 'user-not-found'
            #     return result
            # usr = usr[0]
            # log the user in
            try:
                uid = request.session.authenticate(request.session.db, uid=payload['sub'], password=token)
            except Exception:
                raise
            if not uid:
                result['message'] = 'login-failed'
                return result

            result['status'] = True
            return result
        except jwt.ExpiredSignatureError:
            result['message'] = 'token-expired'
            return result
        except jwt.InvalidTokenError:
            result['message'] = 'token-invalid'
            return result


validator = Validator()