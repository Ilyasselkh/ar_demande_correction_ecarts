{
    "name": "AR - Demande D'ajustement De Stock",
    "version": "1.0",
    "category": "Operations",
    "depends": ["base", "mail", "hr"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/report_araymond_layout.xml",
        "data/report_demande_correction.xml",
        "data/sequence.xml",
        "data/mail_templates.xml",

        "views/regle_validation_views.xml",
        "views/demande_correction_views.xml",
        "views/demande_correction_decision_wizard_views.xml",
        "views/demande_correction_documentation_views.xml",
        "views/res_config_settings_views.xml",
        "views/res_users_views.xml",

        "views/menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "ar_demande_correction_ecarts/static/src/scss/demande_correction_form.scss",
            "ar_demande_correction_ecarts/static/src/js/demande_correction_animations.js",
        ],
    },
    "application": True,
}
