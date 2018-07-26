from odoo.exceptions import AccessDenied
import logging
from odoo import api, models, registry, SUPERUSER_ID

_logger = logging.getLogger(__name__)
from ..validator import validator

class Users(models.Model):
    _inherit = "res.users"

    @classmethod
    def _login(cls, db, login, password):
        user_id = super(Users, cls)._login(db, login, password)
        if user_id:
            return user_id
        
        uid = validator.verify(password)
        _logger.info(uid)

        return uid
            

    @api.model
    def check_credentials(self, password):
        try:
            super(Users, self).check_credentials(password)
        except AccessDenied:
            # verify password as token
            if not validator.verify(password):
                raise

