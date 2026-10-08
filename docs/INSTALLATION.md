# Préparation de l'installation

## Hébergement retenu

Render, workspace dédié Carthaya Health, accès vérifié le 9 octobre 2026.
Voir docs/RENDER.md pour les services et leurs disques. Les informations Linux
ci-dessous concernent une éventuelle installation autogérée, et non le PaaS Render.

## Informations à renseigner

- Fournisseur, localisation et coût mensuel du serveur.
- Distribution Linux et accès SSH du responsable.
- Ressources disponibles : CPU, RAM, SSD et capacité DICOM attendue.
- Noms de domaine de développement et recette.
- Destination de sauvegarde séparée et politique de rétention.
- Identité du référent clinique et contact technique tiers payant.

Exécuter `python3 scripts/preflight.py` pour obtenir un diagnostic local, sans
installation, sans lecture des secrets et sans transmission réseau.
La sortie peut être redirigée dans un rapport local ignoré par Git.

## Ordre de validation

1. Vérifier les distributions officielles et documenter les compatibilités.
2. Figer images et versions exactes ; aucun tag flottant latest.
3. Préparer volumes persistants, secrets hors Git et réseau privé des bases.
4. Installer OpenMRS et réaliser un premier enregistrement/relecture.
5. Ajouter les autres composants et vérifier leurs bases/API.
6. Tester sauvegarde et restauration avant toute recette transversale.

Les ressources de départ restent à mesurer sur la pile : environ 8 vCPU,
32 Go RAM et 300 Go SSD pour développement. Recette séparée suivant les volumes.
Le workspace Render existe ; aucun service payant n’est encore créé.
Le dimensionnement Linux ci-dessus ne constitue pas une configuration de services Render.
