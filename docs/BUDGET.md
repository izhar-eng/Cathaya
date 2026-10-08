# Deux budgets indépendants

## Budget 1 : prestations de développement

TJM : 300 EUR HT/jour-personne.

| Poste | Jours | Base HT EUR |
| --- | --- | --- |
| Cadrage et contrat FHIR | 5–7 | 1 500–2 100 |
| Socle et installation | 8–12 | 2 400–3 600 |
| Consultation/hospitalisation | 10–15 | 3 000–4 500 |
| Laboratoire/imagerie | 7–10 | 2 100–3 000 |
| Pharmacie, stocks et Odoo | 10–15 | 3 000–4 500 |
| Adaptateurs/FHIR | 6–10 | 1 800–3 000 |
| Recette/réplication | 9–16 | 2 700–4 800 |
| Total de base | 55–85 | 16 500–25 500 |
| Réserve de 20 % | 11–17 | 3 300–5 100 |
| Enveloppe avec réserve | 66–102 | 19 800–30 600 |

Référence : 70 jours, 21 000 EUR HT + 4 200 EUR HT de réserve.
La réserve n'est pas une facturation automatique.

## Budget 2 : moyens techniques

Provision séparée sur trois mois : 3 000–4 000 EUR, référence 3 500 EUR.
Les dépenses suivent les factures/consommations, distinctes des jours de prestation.

| Poste | Provision mensuelle EUR |
| --- | --- |
| Développement | 60–120 |
| Recette/démonstration | 80–160 |
| Sauvegardes externes | 20–50 |
| Agents IA | 150–350 |
| Crédits IA supplémentaires si nécessaires | 50–150 |
| Git et automatisation des tests | 0–30 |
| Domaine et petits services | 10–30 |
| Total | 370–890 |

Consommation estimée sur trois mois : 1 110–2 670 EUR avant marge.
Déduire les abonnements déjà financés. Hypothèse Odoo Community, hors licences
Enterprise/modules payants. Provisions à confirmer, hors taxes.

Les équipements, formation sur site, migration réelle, tiers payant, support humain
et mise en service clinique font l'objet de lots séparés.

## Sous-total Render du premier bloc OpenMRS

Configuration détaillée dans docs/RENDER.md : estimation de 129 USD/mois, soit
387 USD sur trois mois, hors taxes, frais de workspace et dépassements. Ce sous-total
est une composante des moyens techniques ; il ne couvre pas OpenELIS, Odoo,
Orthanc/OHIF, FHIR, les outils IA ou les sauvegardes externes. Il ne modifie pas
le TJM de développement de 300 EUR HT et n’est pas additionné une seconde fois
au budget technique global. Pas de conversion EUR non vérifiée dans cette note.

## Décision : démarrage gratuit

Pour la phase initiale, aucun service cloud payant ne doit être provisionné.
Le sous-total Render de 129 USD/mois est une option différée, pas une dépense
engagée. Une pile locale utilisant la machine existante évite les frais cloud.
Cette décision ne modifie pas le TJM ni les estimations de charge du développement.
