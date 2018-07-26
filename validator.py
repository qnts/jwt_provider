import logging
import jwt
import datetime
from odoo import http, service, registry, SUPERUSER_ID
from odoo.http import request
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)

SECRET_KEY = "skjdfe48ueq893rihesdio*($U*WIO$u8"

class Validator:

    def create_token(self, user):
        try:
            exp = datetime.datetime.utcnow() + datetime.timedelta(days=30)
            payload = {
                'exp': exp,
                'iat': datetime.datetime.utcnow(),
                'sub': user['id'],
                'lgn': user['login'],
            }

            token = jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )

            self.save_token(token, user['id'], exp)

            return token
        except Exception as ex:
            _logger.error(ex)
            raise

    def save_token(self, token, uid, exp):
        request.env['jwt.access_token'].sudo().create({
            'user_id': uid,
            'expires': exp.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            'token': token,
        })

    def verify(self, token):
        record = request.env['jwt.access_token'].sudo().search([
            ('token', '=', token)
        ])

        if len(record) != 1:

            _logger.info('not found %s' % token)
            return False

        if not record.is_valid():
            return False
        

        _logger.info('found for %s' % token)
        return record.user_id
        
    
    def verify_token(self, token):
        try:
            result = {
                'status': False,
                'message': None,
            }
            payload = jwt.decode(token, SECRET_KEY)

            if not self.verify(token):
                result['message'] = 'token-invalid'
                return result
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
            uid = request.session.authenticate(request.session.db, uid=payload['sub'], password=token)
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
        except Exception:
            # raise
            result['message'] = 'token-invalid'
            return result
            # return result


validator = Validator()