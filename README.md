# Carthaya Health

Distribution hospitalière réplicable, indépendante de FIT.

## État au 8 octobre 2026

Le dépôt GitHub est initialisé. Cette livraison prépare la structure et le suivi.
Les applications ne sont pas encore installées. Un workspace Render dédié Carthaya Health est créé ; aucun service applicatif n’est encore provisionné.
Le dépôt GitHub izhar-eng/Cathaya est public.
La connexion izhar-eng dispose des droits d’écriture. Les versions restent à vérifier puis à figer.

## Périmètre

- OpenMRS 3 : ambulatoire et hospitalisation.
- OpenELIS Global : demandes, prélèvements et résultats de laboratoire.
- Orthanc et OHIF : archivage DICOM et visualisation.
- Odoo : pharmacie, stock, achats et facturation locale.
- Couche d'intégration et serveur FHIR R4 : publication des données.
- L'équipe distincte de tiers payant consomme FHIR et gère les payeurs/FSE.

Les premières recettes utilisent des données fictives persistées dans les bases métier.
Les tarifs, catalogues et paramètres d'établissement sont administrables.
Une installation sans données de démonstration doit fonctionner.

## Démarrage

1. Consulter `docs/STATUS.md`, `docs/TASKS.csv` et `docs/ROADMAP.md`.
2. Suivre les fichiers et commits sur `https://github.com/izhar-eng/Cathaya`.
3. Consulter `docs/DEMARRAGE_GRATUIT.md` pour le démarrage sans frais cloud.
4. Préparer une machine de développement avec Docker Compose et les mots de passe hors Git.
5. Vérifier les versions et compatibilités dans `config/components.json`.
6. Écrire le déploiement après ces vérifications, puis installer le premier parcours.

La phase actuelle est exclusivement gratuite. `compose.yaml` prépare le premier
bloc OpenMRS sur une machine locale, avec volumes persistants. Le Blueprint
Render payant est retiré. Les images sont figées ; les builds et les parcours
restent à vérifier. Voir `docs/DEMARRAGE_GRATUIT.md`.

## Suivi

Chaque tâche reçoit un statut, un résultat attendu et une preuve.
L'avancement se mesure par les critères réellement validés.
Le premier résultat applicatif attendu est une identité patient enregistrée puis relue
après redémarrage. Les contrôles du squelette ne valident pas une installation SIH.

## Budgets séparés

Prestations : 300 EUR HT/jour, 55 à 85 jours-personne, soit 16 500 à 25 500 EUR HT.
Réserve de 20 % présentée séparément : 3 300 à 5 100 EUR HT.
Moyens techniques : provision distincte de 3 000 à 4 000 EUR sur trois mois.
Détails dans `docs/BUDGET.md`.
