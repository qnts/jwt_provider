from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class JwtAccessToken(models.Model):
    _name = 'jwt.access_token'

    token = fields.Char('Access Token', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True, ondelete='cascade')
    expires = fields.Datetime('Expires', required=True)

    @api.multi
    def is_valid(self):
        """
        Checks if the access token is valid.
        """
        self.ensure_one()
        return not self.is_expired()

    @api.multi
    def is_expired(self):
        self.ensure_one()
        return datetime.now() > datetime.strptime(self.expires, DEFAULT_SERVER_DATETIME_FORMAT)

