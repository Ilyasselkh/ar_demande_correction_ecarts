# AR - Demande d'Ajustement de Stock

Module Odoo de gestion des demandes de correction d'écarts et d'ajustements de stock.

## Objectif

Ce module permet de déclarer des écarts d'inventaire, consommations manuelles ou scrap, de calculer leur valeur et de les faire valider par une chaîne dynamique de validateurs selon les règles configurées.

## Dépendances

- `base`
- `mail`
- `hr`

## Modèles principaux

- `ar.demande.correction` : demande de correction.
- `ar.demande.correction.line` : lignes d'écart.
- `ar.regle.validation` : règles de validation.
- `ar.demande.correction.decision.wizard` : assistant de validation/refus.
- `ar.demande.correction.documentation` : documentation métier.

## Workflow

1. `draft` : nouvelle demande.
2. `n1` : validation manager N+1.
3. `sup_log` : validateur 1.
4. `msc` : validateur 2.
5. `mfin` : validateur 3.
6. `md` : validateur 4.
7. `v5` : validateur 5.
8. `valide` : demande validée.
9. `refuse` : demande refusée.

## Fonctionnement

- Le demandeur est l'utilisateur courant.
- Le département et le manager N+1 sont calculés depuis les données RH.
- Les lignes permettent de renseigner les références, quantités, valeurs et motifs.
- Les totaux MAD et absolus sont calculés automatiquement.
- La règle de validation détermine les validateurs et le nombre de niveaux requis.
- Chaque action enregistre le niveau courant, la date de validation et le validateur.

## Sécurité

Les règles de sécurité et droits sont définis dans :

- `security/security.xml`
- `security/ir.model.access.csv`

## Rapports et interface

Le module fournit un rapport de correction, des vues de configuration, des menus, une documentation et des assets backend pour le formulaire.

