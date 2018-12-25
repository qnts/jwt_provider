import werkzeug

from odoo.exceptions import AccessDenied
from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

from ..validator import validator

class Users(models.Model):
    _inherit = "res.users"

    access_token_ids = fields.One2many(
        string='Access Tokens',
        comodel_name='jwt_provider.access_token',
        inverse_name='user_id',
    )

    avatar = fields.Char(compute='_compute_avatar')

    @classmethod
    def _login(cls, db, login, password):
        user_id = super(Users, cls)._login(db, login, password)
        if user_id:
            return user_id
        
        uid = validator.verify(password)
        _logger.info(uid)

        return uid

    @api.model
    def _check_credentials(self, password):
        try:
            super(Users, self)._check_credentials(password)
        except AccessDenied:
            # verify password as token
            if not validator.verify(password):
                raise

    @api.depends('image')
    def _compute_avatar(self):
        base = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for u in self:
            u.avatar = werkzeug.urls.url_join(base, 'web/avatar/%d' % u.id)

    @api.multi
    def to_dict(self, single=False):
        res = []
        for u in self:
            d = u.read(['email', 'name', 'avatar', 'company_id'])[0]
            res.append(d)

        return res[0] if single else res