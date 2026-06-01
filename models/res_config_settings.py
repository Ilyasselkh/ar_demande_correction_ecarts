from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    ar_taux_eur = fields.Float(string="Taux EUR (MAD pour 1€)",
                               config_parameter="ar_demande_correction_ecarts.taux_eur",
                               default=11.0)