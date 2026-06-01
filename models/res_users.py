from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    # Accès module
    x_access_correction_ecarts = fields.Boolean(string="Accès Correction écarts")

    # Rôles workflow
    x_role_sup_log = fields.Boolean(string="Validateur 1")
    x_role_msc = fields.Boolean(string="Validateur 2")
    x_role_mfin = fields.Boolean(string="Validateur 3")
    x_role_md = fields.Boolean(string="Validateur 4")
    x_role_v5 = fields.Boolean(string="Validateur 5")
    x_role_n1 = fields.Boolean(string="Validation N+1")