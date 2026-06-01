from odoo import models, fields, api, _
from odoo.exceptions import AccessError, ValidationError
import re


class ARDemandeCorrection(models.Model):
    _name = "ar.demande.correction"
    _description = "Demande de correction des écarts"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(string="Référence", default="Nouveau", readonly=True, copy=False, tracking=True)

    state = fields.Selection([
        ("draft", "Nouvelle demande"),
        ("n1", "Validation N+1"),
        ("sup_log", "Validateur 1"),
        ("msc", "Validateur 2"),
        ("mfin", "Validateur 3"),
        ("md", "Validateur 4"),
        ("v5", "Validateur 5"),
        ("valide", "Validée"),
        ("refuse", "Refusée"),
    ], default="draft", tracking=True, required=True)

    demandeur_id = fields.Many2one(
        "res.users", string="Demandeur",
        readonly=True, tracking=True,
        default=lambda self: self.env.user
    )

    date_demande = fields.Datetime(string="Date", default=fields.Datetime.now, readonly=True)

    department_id = fields.Many2one(
        "hr.department", string="Département", readonly=True,
        default=lambda self: self._default_department_id()
    )

    manager_n1_id = fields.Many2one(
        "res.users", string="Manager N+1", readonly=True,
        default=lambda self: self._default_manager_n1_id()
    )

    employee_id = fields.Many2one("hr.employee", string="Employé", readonly=True)

    line_ids = fields.One2many("ar.demande.correction.line", "demande_id", string="Lignes", copy=True)

    total_mad = fields.Float(string="Total Valeur (MAD)", compute="_compute_totaux", store=True)
    total_absolu = fields.Float(string="Total absolu", compute="_compute_totaux", store=True)
    commentaire = fields.Text(string="Commentaire géréral", required=False, tracking=True)

    regle_id = fields.Many2one("ar.regle.validation", string="Règle appliquée", readonly=True)

    # validateurs choisis 
    validateur1_id = fields.Many2one("res.users", readonly=True)
    validateur2_id = fields.Many2one("res.users", readonly=True)
    validateur3_id = fields.Many2one("res.users", readonly=True)
    validateur4_id = fields.Many2one("res.users", readonly=True)
    validateur5_id = fields.Many2one("res.users", readonly=True)

    # Dates/Heures de validation
    date_validation_n1 = fields.Datetime(string="Date validation N+1", readonly=True, tracking=True)
    date_validation_v1 = fields.Datetime(string="Date validation Validateur 1", readonly=True, tracking=True)
    date_validation_v2 = fields.Datetime(string="Date validation Validateur 2", readonly=True, tracking=True)
    date_validation_v3 = fields.Datetime(string="Date validation Validateur 3", readonly=True, tracking=True)
    date_validation_v4 = fields.Datetime(string="Date validation Validateur 4", readonly=True, tracking=True)
    date_validation_v5 = fields.Datetime(string="Date validation Validateur 5", readonly=True, tracking=True)

    current_level = fields.Integer(string="Niveau actuel", default=0, readonly=True)

    is_demandeur = fields.Boolean(string="Est demandeur", compute="_compute_is_demandeur", store=False)

    ajustement = fields.Selection([
        ("ecarts", "Ecarts d'inventaire"),
        ("manuel", "Consommation manuel"),
        ("scrap", "Scrap"),
    ], string="Ajustement de Stock", required=True, tracking=True)

    inventaire_tournant = fields.Selection(
        [("oui", "Oui"), ("non", "Non")],
        string="Inventaire tournant",
        tracking=True
    )

    numero_session = fields.Char(
        string="Numéro de session",
        tracking=True
    )

    @api.constrains("inventaire_tournant", "numero_session")
    def _check_numero_session(self):
        for rec in self:
            if rec.inventaire_tournant == "oui" and not rec.numero_session:
                raise ValidationError(_("Le champ 'Numéro de session' est obligatoire lorsque 'Inventaire tournant' = Oui."))

    @api.constrains("ajustement", "inventaire_tournant")
    def _check_inventaire_tournant(self):
        for rec in self:
            if rec.ajustement == "ecarts" and not rec.inventaire_tournant:
                raise ValidationError(_("Le champ 'Inventaire tournant' est obligatoire pour 'Ecarts d'inventaire'."))
            
    @api.onchange("inventaire_tournant")
    def _onchange_inventaire_tournant(self):
        for rec in self:
            if rec.inventaire_tournant != "oui":
                rec.numero_session = False

    @api.onchange("ajustement")
    def _onchange_ajustement_reset_inventaire(self):
        for rec in self:
            if rec.ajustement != "ecarts":
                rec.inventaire_tournant = False
                rec.numero_session = False

    def _compute_is_demandeur(self):
        for rec in self:
            rec.is_demandeur = (rec.demandeur_id == self.env.user)

    # =========================================================
    # Defaults HR
    # =========================================================
    def _get_employee_of_user(self, user=None):
        user = user or self.env.user
        return self.env["hr.employee"].sudo().search([("user_id", "=", user.id)], limit=1)

    def _default_department_id(self):
        emp = self._get_employee_of_user()
        return emp.department_id.id if emp and emp.department_id else False

    def _default_manager_n1_id(self):
        emp = self._get_employee_of_user()
        if emp and emp.parent_id and emp.parent_id.user_id:
            return emp.parent_id.user_id.id
        return False

    # =========================================================
    # Sécurité (res.users)
    # =========================================================
    def _check_access_module(self):
        if not self.env.user.x_access_correction_ecarts:
            raise AccessError(_("Vous n'avez pas accès au module Correction des écarts."))

    def _check_role_for_state(self):
        self.ensure_one()

        if self.state == "n1" and not self.env.user.x_role_n1:
            raise AccessError(_("Seul le Manager N+1 (rôle Validation N+1) peut valider cette étape."))

        if self.state == "sup_log" and not self.env.user.x_role_sup_log:
            raise AccessError(_("Seul le Validateur 1 peut valider cette étape."))
        if self.state == "msc" and not self.env.user.x_role_msc:
            raise AccessError(_("Seul le Validateur 2 peut valider cette étape."))
        if self.state == "mfin" and not self.env.user.x_role_mfin:
            raise AccessError(_("Seul le Validateur 3 peut valider cette étape."))
        if self.state == "md" and not self.env.user.x_role_md:
            raise AccessError(_("Seul le Validateur 4 peut valider cette étape."))
        if self.state == "v5" and not self.env.user.x_role_v5:
            raise AccessError(_("Seul le Validateur 5 peut valider cette étape."))

    # =========================================================
    # Create + auto-fill
    # =========================================================
    @api.model_create_multi
    def create(self, vals_list):
        seq_model = self.env["ir.sequence"]

        for vals in vals_list:
            if vals.get("name", "Nouveau") == "Nouveau":
                vals["name"] = seq_model.next_by_code("ar.demande.correction") or "DC-0000"

        records = super().create(vals_list)
        records._init_auto_fields()
        return records

    def _init_auto_fields(self):
        for rec in self:
            user = self.env.user
            rec.demandeur_id = user.id

            emp = self.env["hr.employee"].sudo().search([("user_id", "=", user.id)], limit=1)
            rec.employee_id = emp.id
            rec.department_id = emp.department_id.id if emp else False
            rec.manager_n1_id = emp.parent_id.user_id.id if emp and emp.parent_id and emp.parent_id.user_id else False

    # =========================================================
    # Totaux
    # =========================================================
    @api.depends("line_ids.valeur_mad")
    def _compute_totaux(self):
        for rec in self:
            valeurs = rec.line_ids.mapped("valeur_mad")
            rec.total_mad = sum(valeurs)
            rec.total_absolu = sum(abs(v) for v in valeurs)

    def _get_regle_by_total_absolu(self, total_absolu, ajustement):
        domain = [
            ("ajustement", "=", ajustement),
            ("montant_min_mad", "<=", total_absolu),
            "|", ("montant_max_mad", "=", False), ("montant_max_mad", ">=", total_absolu),
        ]
        regle = self.env["ar.regle.validation"].sudo().search(
            domain,
            limit=1,
            order="montant_min_mad desc"
        )
        if not regle:
            raise ValidationError(
                _("Aucune règle configurée pour ce total absolu (%s MAD) et cet ajustement (%s).")
                % (total_absolu, ajustement)
            )
        return regle

    # =========================================================
    # EMAILS
    # =========================================================
    def _clean_header(self, value):
        if not value:
            return False
        return str(value).replace("\n", "").replace("\r", "").strip()

    def _get_user_email(self, user):
        if not user:
            return False
        user = user.sudo()
        email = user.partner_id.email or user.email
        return self._clean_header(email) if email else False

    def _send_template(self, xmlid, email_to_list):
        self.ensure_one()
        template = self.env.ref(xmlid, raise_if_not_found=False)
        if not template:
            return

        recipients = [self._clean_header(e) for e in (email_to_list or [])]
        recipients = [e for e in recipients if e]
        if not recipients:
            return

        email_values = {
            "email_to": self._clean_header(",".join(recipients)),
            "reply_to": self._clean_header(self.env.user.partner_id.email or self.env.user.email or ""),
        }
        template.send_mail(self.id, force_send=True, email_values=email_values)

    def _send_to_validator(self, template_xmlid, user):
        self.ensure_one()
        email = self._get_user_email(user)
        if email:
            self._send_template(template_xmlid, [email])

    def _send_to_demandeur(self, template_xmlid):
        self.ensure_one()
        email = self._get_user_email(self.demandeur_id)
        if email:
            self._send_template(template_xmlid, [email])

    # =========================================================
    # Helpers Workflow 
    # =========================================================
    def _level_to_state(self, level):
        return {
            1: "sup_log",
            2: "msc",
            3: "mfin",
            4: "md",
            5: "v5",
        }.get(level)

    def _validator_at_level(self, level):
        return {
            1: self.validateur1_id,
            2: self.validateur2_id,
            3: self.validateur3_id,
            4: self.validateur4_id,
            5: self.validateur5_id,
        }.get(level)

    def _find_levels_of_user(self, user):
        """Retourne la liste des niveaux (1..5) où ce user apparaît."""
        if not user:
            return []
        levels = []
        for lvl in range(1, 6):
            u = self._validator_at_level(lvl)
            if u and u.id == user.id:
                levels.append(lvl)
        return levels

    def _compute_seen_users_until_level(self, level, extra_seen_ids=None):
        """
        seen = users déjà traités/validés (pour gérer doublons).
        On considère que tous les validateurs des niveaux <= level ont déjà été "passés".
        """
        seen = set(extra_seen_ids or [])
        for lvl in range(1, level + 1):
            u = self._validator_at_level(lvl)
            if u:
                seen.add(u.id)
        return seen

    def _next_level_to_validate(self, start_level, skip_user_ids=None, seen_user_ids=None):
        """
        Retourne le prochain niveau > start_level-1 à valider en respectant:
        - skip_user_ids : demandeur + manager déjà validé en n1
        - seen_user_ids : doublons (user déjà passé)
        - niveaux vides
        """
        self.ensure_one()
        skip_user_ids = set(skip_user_ids or [])
        seen_user_ids = set(seen_user_ids or [])

        for lvl in range(start_level, 6):
            u = self._validator_at_level(lvl)
            if not u:
                continue
            if u.id in skip_user_ids:
                continue
            if u.id in seen_user_ids:
                continue
            return lvl
        return 0

    def _goto_level_or_finish(self, level, template_to_validator):
        """Place la demande sur le niveau donné, ou valide directement si level=0."""
        self.ensure_one()

        if not level:
            self.current_level = 0
            self.state = "valide"
            self._send_to_demandeur(
                "ar_demande_correction_ecarts.mail_template_ecarts_validated_to_demandeur"
            )
            return

        self.current_level = level
        self.state = self._level_to_state(level)
        self._send_to_validator(template_to_validator, self._validator_at_level(level))

    def _check_user_can_validate_level(self):
        """Vérifie que user = validateur du niveau courant."""
        self.ensure_one()
        current = self._validator_at_level(self.current_level)
        if not current:
            raise AccessError(_("Aucun validateur n'est défini pour ce niveau."))
        if self.env.user != current:
            raise AccessError(_("Vous n'êtes pas autorisé à valider à cette étape."))

    def _check_user_can_validate_n1(self):
        self.ensure_one()
        if not self.manager_n1_id:
            raise AccessError(_("Aucun Manager N+1 n'est défini pour cette demande."))
        if self.env.user != self.manager_n1_id:
            raise AccessError(_("Seul le Manager N+1 peut valider cette étape."))

    def _start_flow_after_submit_or_n1(self, manager_already_validated=False):
        """
        Démarre la validation "par règle" en appliquant la logique :
        - si demandeur apparaît dans validateurs => sauter son niveau
        - si manager apparaît dans validateurs ET manager_already_validated=True => sauter son niveau
        - gérer doublons
        - respecter les états correspondants aux niveaux
        """
        self.ensure_one()

        demandeur = self.demandeur_id
        manager = self.manager_n1_id

        skip_ids = set()
        if demandeur:
            skip_ids.add(demandeur.id)

        # si le manager a déjà validé en n1 -> il ne doit pas revalider dans la règle
        if manager_already_validated and manager:
            skip_ids.add(manager.id)

        # seen pour gérer doublons 
        seen_ids = set()
        if manager_already_validated and manager:
            seen_ids.add(manager.id)

        start_level = 1
        if manager_already_validated and manager:
            manager_levels = self._find_levels_of_user(manager)
            if manager_levels:
                # on démarre après le dernier niveau où le manager est présent
                start_level = max(manager_levels) + 1

        next_level = self._next_level_to_validate(start_level, skip_user_ids=skip_ids, seen_user_ids=seen_ids)

        # Aller au bon état correspondant à ce niveau
        self._goto_level_or_finish(
            next_level,
            "ar_demande_correction_ecarts.mail_template_ecarts_to_validator"
        )

    # =========================================================
    # Actions workflow
    # =========================================================
    def action_soumettre(self):
        self._check_access_module()

        for rec in self:
            if rec.state != "draft":
                raise ValidationError(_("Vous ne pouvez soumettre que depuis 'Nouvelle demande'."))

            if not rec.line_ids:
                raise ValidationError(_("Veuillez saisir au moins une ligne."))

            for l in rec.line_ids:
                l._check_required_line()

            # 1) appliquer la règle et charger les validateurs EXACTS 
            regle = rec._get_regle_by_total_absolu(rec.total_absolu, rec.ajustement)
            rec.regle_id = regle.id

            rec.validateur1_id = regle.validateur1_id.id
            rec.validateur2_id = regle.validateur2_id.id
            rec.validateur3_id = regle.validateur3_id.id
            rec.validateur4_id = regle.validateur4_id.id
            rec.validateur5_id = regle.validateur5_id.id

            rec.current_level = 0

            # 2) Gestion de l'étape N+1
            # - si pas de manager ou manager = demandeur => on saute n1 et on démarre directement le flux
            if not rec.manager_n1_id or rec.manager_n1_id == rec.demandeur_id:
                rec._start_flow_after_submit_or_n1(manager_already_validated=False)
            else:
                rec.state = "n1"
                rec._send_to_validator(
                    "ar_demande_correction_ecarts.mail_template_ecarts_to_manager_n1",
                    rec.manager_n1_id
                )

    def action_valider(self):
        self._check_access_module()

        for rec in self:
            if rec.state in ("draft", "valide", "refuse"):
                raise ValidationError(_("Vous ne pouvez pas valider dans cet état."))

            # ===========
            # Étape N+1
            # ===========
            if rec.state == "n1":
                # demandeur ne peut pas valider, et seul manager peut valider n1
                if rec.demandeur_id == rec.env.user:
                    raise AccessError(_("Le demandeur ne peut pas valider sa propre demande."))
                rec._check_user_can_validate_n1()
                rec._check_role_for_state()

                rec.date_validation_n1 = fields.Datetime.now()
                rec._start_flow_after_submit_or_n1(manager_already_validated=True)
                continue

            # ========================
            # Validation niveaux 1..5
            # ========================
            if rec.demandeur_id == rec.env.user:
                raise AccessError(_("Le demandeur ne peut pas valider sa propre demande."))

            if not rec.current_level:
                raise ValidationError(_("Niveau de validation invalide."))

            rec._check_user_can_validate_level()
            rec._check_role_for_state()
            
            now = fields.Datetime.now()
            if rec.current_level == 1:
                rec.date_validation_v1 = now
            elif rec.current_level == 2:
                rec.date_validation_v2 = now
            elif rec.current_level == 3:
                rec.date_validation_v3 = now
            elif rec.current_level == 4:
                rec.date_validation_v4 = now
            elif rec.current_level == 5:
                rec.date_validation_v5 = now

            extra_seen = set()
            if rec.demandeur_id:
                extra_seen.add(rec.demandeur_id.id)

            if rec.manager_n1_id and rec.state not in ("draft", "n1"):
                extra_seen.add(rec.manager_n1_id.id)

            seen_ids = rec._compute_seen_users_until_level(rec.current_level, extra_seen_ids=extra_seen)

            # next level à partir du niveau suivant
            next_level = rec._next_level_to_validate(
                rec.current_level + 1,
                skip_user_ids=extra_seen,     # demandeur + manager déjà validé
                seen_user_ids=seen_ids        # doublons
            )

            if next_level:
                rec._goto_level_or_finish(
                    next_level,
                    "ar_demande_correction_ecarts.mail_template_ecarts_to_validator"
                )
            else:
                rec.current_level = 0
                rec.state = "valide"
                rec._send_to_demandeur(
                    "ar_demande_correction_ecarts.mail_template_ecarts_validated_to_demandeur"
                )

    def action_refuser(self):
        self._check_access_module()

        for rec in self:
            if rec.demandeur_id == rec.env.user:
                raise AccessError(_("Le demandeur ne peut pas refuser sa propre demande."))
            if rec.state == "valide":
                raise ValidationError(_("Une demande validée ne peut pas être refusée."))

            if rec.state == "n1":
                rec._check_user_can_validate_n1()
                rec._check_role_for_state()
            elif rec.state not in ("draft", "refuse"):
                rec._check_user_can_validate_level()
                rec._check_role_for_state()

            rec.state = "refuse"
            rec.current_level = 0

            rec._send_to_demandeur(
                "ar_demande_correction_ecarts.mail_template_ecarts_refused_to_demandeur"
            )


class ARDemandeCorrectionLine(models.Model):
    _name = "ar.demande.correction.line"
    _description = "Lignes - Demande correction"

    demande_id = fields.Many2one("ar.demande.correction", required=True, ondelete="cascade")

    magasin = fields.Selection([
        ("TR37", "TR37"),
        ("TR00", "TR00"),
        ("SP00", "SP00"),
        ("SF01", "SF01"),
        ("RP00", "RP00"),
        ("RM01", "RM01"),
        ("RM00", "RM00"),
        ("PROD", "PROD"),
        ("JL00", "JL00"),
        ("FG01", "FG01"),
        ("FG00", "FG00"),
        ("EX00", "EX00"),
        ("EMBW", "EMBW"),
        ("EMB", "EMB"),
        ("CL00", "CL00"),
        ("CC00", "CC00"),
    ], required=True, tracking=True)

    reference = fields.Char(required=True, tracking=True)
    designation = fields.Char(required=True, tracking=True)
    lot = fields.Char(required=True, tracking=True)
    quantite = fields.Float(required=True, tracking=True)
    unite = fields.Selection([
        ("PCE", "PCE"),
        ("KG", "KG"),
        ("M", "M"),
    ], string="Unité", required=True, tracking=True)
    valeur_mad = fields.Float(string="Valeur en MAD", required=True, tracking=True)
    motif_ecart = fields.Char(required=True, tracking=True)

    @api.constrains("reference")
    def _check_reference_9_digits(self):
        for rec in self:
            ref = (rec.reference or "").strip()
            # exactement 9 chiffres
            if not re.fullmatch(r"\d{9}", ref):
                raise ValidationError(_("La référence doit contenir exactement 9 chiffres (ex: 123456789)."))

    def _check_required_line(self):
        for l in self:
            missing = []
            for f in ["magasin", "reference", "designation", "lot", "quantite", "unite", "valeur_mad", "motif_ecart"]:
                if not l[f]:
                    missing.append(f)
            if missing:
                raise ValidationError(_("Ligne incomplète : champs obligatoires manquants (%s).") % ", ".join(missing))
            
    def write(self, vals):
        for rec in self:
            if rec.demande_id and rec.demande_id.state != "draft":
                raise ValidationError(_("Les lignes ne sont modifiables que dans l'état 'Nouvelle demande'."))
        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.demande_id and rec.demande_id.state != "draft":
                raise ValidationError(_("Les lignes ne sont supprimables que dans l'état 'Nouvelle demande'."))
        return super().unlink()