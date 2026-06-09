from odoo import _, fields, models
from odoo.exceptions import ValidationError


class ARDemandeCorrectionDecisionWizard(models.TransientModel):
    _name = "ar.demande.correction.decision.wizard"
    _description = "Confirmation soumission/validation/refus demande de correction"

    demande_id = fields.Many2one(
        "ar.demande.correction",
        string="Demande",
        required=True,
        readonly=True,
    )
    action_type = fields.Selection(
        [
            ("submit", "Soumettre"),
            ("validate", "Valider"),
            ("refuse", "Refuser"),
        ],
        string="Action",
        required=True,
        readonly=True,
    )
    def action_confirm(self):
        self.ensure_one()
        if not self.demande_id:
            raise ValidationError(_("Aucune demande selectionnee."))

        if self.action_type == "submit":
            self.demande_id.action_soumettre()
        elif self.action_type == "validate":
            self.demande_id.action_valider()
        elif self.action_type == "refuse":
            self.demande_id.action_refuser()
        else:
            raise ValidationError(_("Action inconnue."))

        return {"type": "ir.actions.act_window_close"}
