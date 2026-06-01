# AR - Demande Ajustement de Stock

Module Odoo pour declarer et valider les corrections ecarts de stock: ecarts inventaire, consommation manuelle ou scrap.

## Objectif

Cette documentation explique le perimetre fonctionnel du module, les roles utilisateurs, le workflow, la configuration et les principaux objets techniques.

## Utilisateurs concernes

- Demandeur
- Manager N+1
- Validateurs metier
- Administrateur Odoo

## Workflow metier

1. Nouvelle demande
2. Validation N+1
3. Validateur 1
4. Validateur 2
5. Validateur 3
6. Validateur 4
7. Validateur 5 si necessaire
8. Validee
9. Refusee

## Fonctionnement operationnel

- Creer une demande.
- Choisir le type ajustement.
- Ajouter les lignes ecart.
- Soumettre.
- Valider selon les niveaux requis.
- Refuser avec motif si necessaire.

## Configuration recommandee

- Creer les regles de validation.
- Renseigner les validateurs.
- Verifier utilisateur, employe et manager.
- Configurer sequence, templates mail et rapport.

## Dependances Odoo

- `base`
- `mail`
- `hr`

## Modeles principaux

- `ar.demande.correction`
- `ar.demande.correction.line`
- `ar.regle.validation`
- `ar.demande.correction.decision.wizard`
- `ar.demande.correction.documentation`

## Structure importante du module

- `security/ir.model.access.csv`
- `security/security.xml`
- `data/mail_templates.xml`
- `data/report_demande_correction.xml`
- `data/sequence.xml`
- `views/demande_correction_decision_wizard_views.xml`
- `views/demande_correction_documentation_views.xml`
- `views/demande_correction_views.xml`
- `views/menus.xml`
- `views/regle_validation_views.xml`
- `views/res_config_settings_views.xml`
- `views/res_users_views.xml`
- `models/__init__.py`
- `models/demande_correction.py`
- `models/demande_correction_decision_wizard.py`
- `models/demande_correction_documentation.py`
- `models/regle_validation.py`
- `models/res_config_settings.py`
- `models/res_users.py`

## Securite

Les droits sont geres par les fichiers du dossier `security`. Il faut verifier les groupes, les regles enregistrement et les acces CSV apres installation ou modification du module.

## Notifications et suivi

Les modules qui dependent de `mail` utilisent le chatter Odoo pour tracer les changements. Les templates mail presents dans le dossier `data` servent a notifier les acteurs concernes par les transitions.

## Installation

1. Copier le module dans le dossier addons Odoo.
2. Redemarrer le serveur Odoo si necessaire.
3. Mettre a jour la liste des applications.
4. Installer ou mettre a jour le module.
5. Verifier les droits utilisateurs et tester un dossier de bout en bout.

## Maintenance

- Ajouter toute nouvelle etape a la fois dans le modele Python, les vues XML, les droits et les notifications.
- Tester les workflows avec plusieurs roles utilisateurs.
- Mettre a jour les rapports et templates mail quand la procedure interne change.
- Eviter de modifier les donnees de production sans sauvegarde.
- Documenter toute evolution fonctionnelle dans ce README.
