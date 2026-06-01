from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ARRegleValidation(models.Model):
    _name = "ar.regle.validation"
    _description = "Règles de validation - Correction écarts"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "ajustement, montant_min_mad"

    ajustement = fields.Selection([
        ("ecarts", "Ecarts d'inventaire"),
        ("manuel", "Consommation manuel"),
        ("scrap", "Scrap"),
    ], required=True, tracking=True)

    montant_min_mad = fields.Float(string="Montant min (MAD)", required=True, tracking=True, default=0.0)
    montant_max_mad = fields.Float(string="Montant max (MAD)", tracking=True)  

    validateur1_id = fields.Many2one("res.users", string="Validateur 1", tracking=True)
    validateur2_id = fields.Many2one("res.users", string="Validateur 2", tracking=True)
    validateur3_id = fields.Many2one("res.users", string="Validateur 3", tracking=True)
    validateur4_id = fields.Many2one("res.users", string="Validateur 4", tracking=True)
    validateur5_id = fields.Many2one("res.users", string="Validateur 5", tracking=True)

    @api.constrains("montant_min_mad", "montant_max_mad")
    def _check_plage_mad(self):
        for rec in self:
            if rec.montant_min_mad < 0:
                raise ValidationError(_("Le montant minimum (MAD) ne peut pas être négatif."))
            if rec.montant_max_mad and rec.montant_max_mad < rec.montant_min_mad:
                raise ValidationError(_("Le montant max (MAD) doit être >= au montant min (MAD)."))

    @api.constrains("validateur1_id", "validateur2_id", "validateur3_id", "validateur4_id", "validateur5_id")
    def _check_validateurs(self):
        for rec in self:
            if not rec.validateur1_id or not rec.validateur2_id:
                raise ValidationError(_("Il faut renseigner au minimum Validateur 1 et Validateur 2."))

            if rec.validateur4_id and not rec.validateur3_id:
                raise ValidationError(_("Si Validateur 4 est renseigné, Validateur 3 doit l’être aussi."))
            if rec.validateur5_id and not rec.validateur4_id:
                raise ValidationError(_("Si Validateur 5 est renseigné, Validateur 4 doit l’être aussi."))