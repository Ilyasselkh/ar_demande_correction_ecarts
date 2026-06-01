# AR - Demande d'Ajustement de Stock


> Documentation du module de correction des ?carts de stock.


## Vue d?ensemble

Ce module encadre les demandes d?ajustement de stock li?es aux ?carts d?inventaire, consommations manuelles ou scrap. Il calcule les valeurs, s?lectionne une r?gle de validation et fait avancer la demande dans une cha?ne multi-niveaux.

## Utilisateurs concern?s

- Demandeur : d?clare l??cart et les lignes.
- Manager N+1 : premier contr?le.
- Validateurs m?tier : logistique, finance, MD ou niveaux configur?s.
- Administrateur : configure r?gles de validation et acc?s.

## Workflow m?tier

1. Nouvelle demande
2. Validation N+1
3. Validateur 1
4. Validateur 2
5. Validateur 3
6. Validateur 4
7. Validateur 5 si n?cessaire
8. Valid?e
9. Refus?e

## Fonctionnement op?rationnel

- Cr?er une demande et choisir le type d?ajustement.
- Ajouter les lignes d??cart avec r?f?rence, quantit? et valeur.
- Soumettre la demande.
- Valider ?tape par ?tape selon la r?gle appliqu?e.
- Refuser avec motif si n?cessaire.
- Imprimer ou consulter le rapport.

## Configuration recommand?e

- Cr?er les r?gles de validation avec les validateurs et niveaux requis.
- V?rifier la relation utilisateur-employ?-manager.
- Configurer la s?quence, templates et rapport.
- Contr?ler les droits d?acc?s.

## D?pendances Odoo

- `base`
- `mail`
- `hr`

## Mod?les techniques

- `ar.demande.correction` : Demande de correction des écarts (`models/demande_correction.py`)
- `ar.demande.correction.line` : Lignes - Demande correction (`models/demande_correction.py`)
- `ar.demande.correction.decision.wizard` : Confirmation validation/refus demande de correction (`models/demande_correction_decision_wizard.py`)
- `ar.demande.correction.documentation` : Correction écarts - Documentation (`models/demande_correction_documentation.py`)
- `ar.regle.validation` : Règles de validation - Correction écarts (`models/regle_validation.py`)

## ?tats d?tect?s dans le code

- `models/demande_correction.py` : `draft` (Nouvelle demande), `n1` (Validation N+1), `sup_log` (Validateur 1), `msc` (Validateur 2), `mfin` (Validateur 3), `md` (Validateur 4), `v5` (Validateur 5), `valide` (Validée), `refuse` (Refusée)

## Actions serveur principales

- `action_soumettre` (`models/demande_correction.py`)
- `action_valider` (`models/demande_correction.py`)
- `action_refuser` (`models/demande_correction.py`)
- `action_confirm` (`models/demande_correction_decision_wizard.py`)

## Fichiers charg?s par le manifest

- `security/security.xml`
- `security/ir.model.access.csv`
- `data/report_demande_correction.xml`
- `data/sequence.xml`
- `data/mail_templates.xml`
- `views/regle_validation_views.xml`
- `views/demande_correction_views.xml`
- `views/demande_correction_documentation_views.xml`
- `views/res_config_settings_views.xml`
- `views/res_users_views.xml`
- `views/menus.xml`

## S?curit? et droits

Le module s?appuie sur les fichiers suivants pour d?finir les groupes, r?gles d?enregistrement et droits d?acc?s :

- `security/ir.model.access.csv`
- `security/security.xml`

## Assets et interface

- `static/src/js/demande_correction_animations.js`
- `static/src/scss/demande_correction_form.scss`

## Bonnes pratiques d?utilisation

- V?rifier que chaque utilisateur Odoo est li? au bon employ? lorsque le module d?pend de `hr.employee`.
- Tester le workflow avec un dossier de test avant utilisation en production.
- Contr?ler les groupes de s?curit? apr?s installation afin que seuls les bons r?les voient les boutons de validation.
- Garder les templates e-mail et rapports align?s avec les proc?dures internes.
- Sauvegarder la base avant toute modification structurelle du module.

## Maintenance

- Les ?volutions fonctionnelles doivent ?tre ajout?es dans les mod?les Python, les vues XML et les r?gles de s?curit? correspondantes.
- Apr?s modification des vues, mettre ? jour le module depuis Odoo ou red?marrer le serveur selon le type de changement.
- Apr?s modification des assets, vider le cache navigateur et recompiler les assets si n?cessaire.
- Toute nouvelle ?tape de workflow doit ?tre accompagn?e des droits, boutons, notifications et filtres correspondants.
