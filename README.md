# AR - Demande d'Ajustement de Stock

Module Odoo de gestion des demandes de correction d'ecarts de stock.

Le module couvre les ecarts d'inventaire, les consommations manuelles et le scrap, avec validation Manager N+1, validateurs successifs, regularisation SAP et archivage.

## Objectif fonctionnel

Encadrer les corrections de stock afin que chaque ajustement soit justifie, valide et regularise dans SAP.

Le module permet de :

- creer une demande de correction ;
- choisir le type d'ajustement ;
- renseigner les lignes d'ecart ;
- calculer les totaux en MAD et en valeur absolue ;
- appliquer une regle de validation ;
- selectionner les validateurs selon le niveau requis ;
- faire valider jusqu'a cinq niveaux ;
- envoyer la demande en regularisation SAP ;
- tracer la regularisation ;
- refuser avec motif ;
- notifier les acteurs par email ;
- imprimer un rapport.

## Roles fonctionnels

### Demandeur

Le demandeur initie la demande de correction.

Il peut :

- creer une demande ;
- renseigner le type d'ajustement ;
- ajouter les lignes ;
- indiquer le commentaire general ;
- soumettre la demande ;
- suivre l'etat de validation.

### Manager N+1

Le Manager N+1 valide la demande avant les validateurs metier.

### Validateurs metier

Les validateurs successifs valident selon la regle appliquee.

Le module prevoit jusqu'a cinq niveaux :

- Validateur 1 ;
- Validateur 2 ;
- Validateur 3 ;
- Validateur 4 ;
- Validateur 5.

### Regularisateur SAP

Le regularisateur SAP intervient apres les validations.

Il confirme la regularisation et archive la demande.

## Types d'ajustement

Les types disponibles sont :

- `Ecarts d'inventaire`
- `Consommation manuel`
- `Scrap`

Pour les ecarts d'inventaire, le champ `Inventaire tournant` est obligatoire.

Si `Inventaire tournant = Oui`, le numero de session est obligatoire.

## Etats du workflow

Les etats principaux sont :

- `Nouvelle demande`
- `Validation N+1`
- `Validateur 1`
- `Validateur 2`
- `Validateur 3`
- `Validateur 4`
- `Validateur 5`
- `Regularisation sur SAP`
- `Archive`
- `Refusee`

## Flux standard

1. `Nouvelle demande`
2. `Validation N+1`
3. `Validateur 1`
4. `Validateur 2`
5. `Validateur 3`
6. `Validateur 4`
7. `Validateur 5` si requis
8. `Regularisation sur SAP`
9. `Archive`

Le nombre de validateurs depend de la regle de validation appliquee.

## Regles de validation

Les regles de validation definissent les validateurs a utiliser selon le contexte de la demande.

Elles permettent de piloter :

- le type d'ajustement ;
- les niveaux de validation ;
- les utilisateurs validateurs ;
- le passage vers regularisation SAP.

## Refus

Un refus peut intervenir aux etapes de validation.

Le module conserve :

- l'utilisateur ayant refuse ;
- la date de refus ;
- l'etape du refus ;
- le motif saisi dans l'assistant.

## Notifications

Les templates email couvrent notamment :

- envoi vers Manager N+1 ;
- envoi vers validateur courant ;
- envoi vers regularisateur SAP ;
- acceptation vers demandeur ;
- refus vers demandeur.

Fichier principal :

- `data/mail_templates.xml`

## Rapports

Le module fournit un rapport de demande de correction.

Fichier principal :

- `data/report_demande_correction.xml`

## Modeles principaux

- `ar.demande.correction`
- `ar.demande.correction.line`
- `ar.regle.validation`
- `ar.demande.correction.decision.wizard`
- `ar.demande.correction.documentation`

## Structure du module

- `security/security.xml`
- `security/ir.model.access.csv`
- `data/sequence.xml`
- `data/mail_templates.xml`
- `data/report_araymond_layout.xml`
- `data/report_demande_correction.xml`
- `views/regle_validation_views.xml`
- `views/demande_correction_views.xml`
- `views/demande_correction_decision_wizard_views.xml`
- `views/demande_correction_documentation_views.xml`
- `views/res_config_settings_views.xml`
- `views/res_users_views.xml`
- `views/menus.xml`
- `models/demande_correction.py`
- `models/regle_validation.py`
- `models/demande_correction_decision_wizard.py`
- `models/demande_correction_documentation.py`
- `models/res_config_settings.py`
- `models/res_users.py`

## Installation

1. Copier le module dans le dossier addons Odoo.
2. Redemarrer le serveur Odoo si necessaire.
3. Mettre a jour la liste des applications.
4. Installer le module.
5. Configurer les groupes et droits.
6. Creer les regles de validation.
7. Verifier les validateurs et le regularisateur SAP.
8. Tester un flux complet par type d'ajustement.

## Maintenance fonctionnelle

Lorsqu'une regle de stock change, verifier aussi :

- les regles de validation ;
- les contraintes sur inventaire tournant ;
- les boutons de workflow ;
- les assistants ;
- les templates email ;
- le rapport ;
- ce README.
