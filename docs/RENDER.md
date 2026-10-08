# Déploiement Render — Carthaya Health

État au 9 octobre 2026 : workspace dédié créé et accessible. Aucun service
ni base PostgreSQL n’a été trouvé dans cet espace. Aucun Blueprint n’est appliqué.

## Premier bloc : identité patient OpenMRS

L’architecture de la distribution officielle comporte quatre services.
Sur Render, chacun sera déclaré séparément dans un Blueprint versionné.

| Composant | Type Render prévu | Persistance prévue | Rôle |
| --- | --- | --- | --- |
| Passerelle Carthaya | Web Docker | Sans disque | Point d’entrée HTTPS commun de l’interface et de l’API |
| Interface OpenMRS O3 | Service privé Docker | Assets dans l’image | Interface utilisateur derrière la passerelle |
| API OpenMRS | Service privé Docker | Disque /openmrs/data | Application et configuration métier |
| MariaDB OpenMRS | Service privé Docker | Disque /var/lib/mysql | Base clinique neuve et persistante |

Tous les services du bloc utiliseront la même région. Le choix de région est
encore ouvert. Les hôtes internes seront référencés par fromService ; les noms
Docker Compose backend/frontend/db ne doivent pas être repris tels quels.
Le point d’entrée public devra gérer l’authentification et empêcher l’exposition
de comptes administrateurs de démonstration. Aucun secret ne sera stocké dans Git.

## Versions et absence de données en dur

La version stable 3.7.1 existe dans le dépôt officiel et dans le registre du
backend ; elle est une candidate, non une installation validée.
Le dépôt fournit distro-no-demo.properties, qui exclut referencedemodata et
referenceapplication-demo. Une variante 3.7.x-no-demo existe dans le registre,
mais son contenu et sa correspondance avec l’interface doivent être vérifiés
avant sélection. Tous les artefacts retenus seront figés par digest.

La configuration métier requise (concepts, lieux, rôles, identifiants) reste
nécessaire même sans patients de démonstration. Elle sera configurable et
séparée des fixtures patients. La première preuve sera la création d’un patient
fictif par l’interface/API, puis sa relecture après redémarrage et redéploiement.

## Conditions avant application du Blueprint

1. Vérifier la cohérence backend/interface/modules et la construction sans démo.
2. Figer les images et documenter leurs digests et origines.
3. Adapter la passerelle aux hôtes Render et au port du service.
4. Définir ressources et tailles de disques ; présenter le coût mensuel du bloc.
5. Valider le schéma render.yaml, les références et les secrets hors Git.
6. Appliquer le Blueprint dans le workspace Carthaya Health, puis inspecter les logs.
7. Créer/re lire un patient fictif, tester la persistance et la restauration.

Les services privés et les disques persistants nécessitent des offres payantes.
Le workspace créé ne vaut pas provisionnement de ces ressources. Les prix exacts
seront ceux affichés par Render pour la configuration avant son application.
Le coût Render sera comptabilisé dans les moyens techniques, séparément du
TJM de développement à 300 EUR HT. Le budget global n’est pas recalculé ici.

## Sauvegardes

Sauvegarder MariaDB avec un outil logique adapté (mariadb-dump), exporter hors
service, puis tester une restauration sur une base séparée. Render déconseille
la restauration d’un snapshot de disque pour récupérer une base autogérée,
car elle peut aboutir à une base corrompue. Sauvegarder également /openmrs/data.

## Composants suivants

Après validation de l’identité patient : Odoo, OpenELIS Global, Orthanc/OHIF,
puis la couche d’intégration et le serveur FHIR. Le tiers payant/FSE reste
hors périmètre de notre équipe. La réplication s’appuiera sur un Blueprint,
les configurations d’établissement et les procédures de restauration.

## Sources vérifiées

- https://github.com/openmrs/openmrs-distro-referenceapplication/blob/3.7.1/docker-compose.yml
- https://github.com/openmrs/openmrs-distro-referenceapplication/blob/3.7.1/distro/distro-no-demo.properties
- https://hub.docker.com/r/openmrs/openmrs-reference-application-3-backend/tags
- https://render.com/docs/blueprint-spec
- https://render.com/docs/disks
- https://render.com/docs/deploy-mysql
- https://render.com/docs/compute-plans
