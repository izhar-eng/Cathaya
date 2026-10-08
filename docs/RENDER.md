# Déploiement Render — Carthaya Health

État au 9 octobre 2026 : workspace dédié créé et accessible. Aucun service
ni base PostgreSQL n’a été trouvé dans cet espace. render.yaml est préparé et
validé contre le schéma JSON officiel. Aucun Blueprint n’est appliqué.

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

Les images backend et frontend 3.7.1 sont figées par digest. Le contenu OCI du
backend annonce Platform 2.8.8, referenceapplication 1.4.0 et demo 1.9.2.
Le Dockerfile Carthaya retire les répertoires referenceapplication-demo, le module
referencedemodata 2.6.1 et leurs déclarations, avant le premier démarrage.
Les fichiers de configuration de base restent présents. Ce filtrage est limité
à la distribution inspectée ; des assertions arrêtent le build en cas d’écart.

Le tag 3.7.x-no-demo a été écarté après inspection : il contient des snapshots
3.8.0 / Platform 2.8.10. Le verrou des images est config/render-images.lock.json.
Les contrôles et leurs limites sont consignés dans config/render-verification.json.

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

## Configuration proposée et coût du premier bloc

| Service | Ressources | Coût mensuel USD |
| --- | --- | ---: |
| Passerelle | Starter, 512 Mo | 7 |
| Interface | Starter, 512 Mo | 7 |
| API OpenMRS | Pro, 4 Go | 85 |
| MariaDB | Standard, 2 Go | 25 |
| Disques | 15 Go base + 5 Go application, 0,25 USD/Go | 5 |
| Total du premier bloc | Développement, une instance par service | 129 |

Estimation au 9 octobre 2026, hors taxes, frais éventuels de workspace, trafic,
minutes de build supplémentaires, destination des sauvegardes et autres modules.
Source : https://render.com/pricing. Coût sur trois mois à configuration constante :
387 USD. Ce montant couvre uniquement OpenMRS, et reste distinct du développement.
Ne pas remplacer le budget de toute la pile par ce sous-total.

## Appliquer le Blueprint

1. Dans Render, sélectionner le workspace Carthaya Health.
2. Ouvrir https://dashboard.render.com/blueprint/new?repo=https://github.com/izhar-eng/Cathaya
3. Relier le dépôt et choisir la branche main si Render le demande.
4. Vérifier les quatre services, Frankfurt et le coût annoncé.
5. Renseigner OMRS_CONFIG_ADMIN_USER_PASSWORD avec un mot de passe unique fort,
   conservé dans le gestionnaire de mots de passe ; ne pas l’envoyer dans le chat.
6. Cliquer Apply. Les mots de passe de base sont générés et reliés automatiquement.
7. Vérifier les builds et les démarrages avec les logs de chaque service.

Le plugin ne crée pas directement les services privés avec leurs disques ;
la première application de cette infrastructure passe par le Dashboard Blueprint.
Les déploiements automatiques des Dockerfiles sont désactivés pour maîtriser
les mises à jour de ce premier environnement ; les redéploiements sont manuels.

Le health check /healthz prouve uniquement que la passerelle répond. Il ne prouve
pas que la base ou OpenMRS est prêt. La connexion doit être testée sur /openmrs/spa/.
Après démarrage sans démo, configurer les lieux, identifiants et rôles de Carthaya
avant la création du premier patient. Aucun parcours clinique n’est encore validé.

Docker et le CLI Render n’étant pas disponibles dans l’environnement de préparation,
la validation locale couvre le schéma public, les références et la syntaxe shell.
Les builds, le test nginx et la compatibilité en exécution seront vérifiés sur Render.
