from odoo.exceptions import AccessDenied

from odoo import api, models, registry, SUPERUSER_ID


class Users(models.Model):
    _inherit = "res.users"

    # @classmethod
    # def _login(cls, db, login, password):
    #     user_id = super(Users, cls)._login(db, login, password)
    #     if user_id:
    #         return user_id
    #     with registry(db).cursor() as cr:
    #         cr.execute("SELECT id FROM res_users WHERE lower(login)=%s", (login,))
    #         res = cr.fetchone()
    #         if not res:
    #             return False
    #         return res['id']
            

    # @api.model
    # def check_credentials(self, password):
    #     try:
    #         super(Users, self).check_credentials(password)
    #     except AccessDenied:
    #         # verify password as token
            
    #         raise
