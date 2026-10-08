# Démarrage gratuit de Carthaya

Décision du 9 octobre 2026 : uniquement des ressources gratuites au démarrage.
Aucun service payant Render ne doit être créé. Le workspace dédié est vide lors
de la dernière vérification. L’ancien Blueprint payant est retiré du dépôt actif.

## Ce que permet Render Free

L’offre gratuite ne propose pas de disque persistant pour les web services.
La base PostgreSQL gratuite expire après 30 jours. Notre distribution OpenMRS
utilise MariaDB : remplacer sa base par PostgreSQL n’est pas une adaptation validée.
La pile intégrée persistante préparée ne peut donc pas être présentée comme
fonctionnelle gratuitement sur Render. Les sites statiques et les composants
compatibles avec les limites Free pourront y être ajoutés séparément plus tard.

Sources : https://render.com/docs/free et https://render.com/docs/disks.

## Première pile réelle : sur la machine de développement

compose.yaml conserve OpenMRS 3.7.1 / Platform 2.8.8 et MariaDB 10.11.19 avec
leurs données sur deux volumes locaux. Interface et passerelle sont incluses.
La variante backend retire les imports de démonstration avant démarrage.
Aucun patient n’est simulé dans le code ; les patients fictifs seront saisis par l’application.

Prévoir Docker Engine et Docker Compose v2, ou un environnement compatible.
Vérifier les conditions de licence de l’outil choisi pour l’organisation.
Prévoir environ 8 Go de RAM disponibles pour ce premier bloc et 15 à 20 Go de
disque libre au départ. Ce dimensionnement est une cible de test, à mesurer.
Docker n’est pas installé dans l’environnement de préparation : les builds et
les tests applicatifs n’ont pas été exécutés ici.

Depuis le dépôt :

```sh
cp .env.example .env
```

Renseigner trois mots de passe uniques forts dans .env, puis :

```sh
docker compose config --quiet
docker compose up -d --build
docker compose ps
docker compose logs --tail=100 backend
```

La première construction et l’initialisation peuvent prendre plusieurs minutes.
Ouvrir http://localhost:8080/openmrs/spa/ et utiliser admin avec le mot de passe
CARTHAYA_ADMIN_PASSWORD. Ne pas publier ces mots de passe ni les logs sensibles.
Le port est lié uniquement à 127.0.0.1. Les services métier et MariaDB ne sont
pas exposés directement sur la machine.

Après démarrage sans démo, configurer les lieux, les identifiants et les rôles
nécessaires à l’établissement avant de créer le premier patient fictif.
Pour les essais réels : création, stockage, relecture après reconnexion, puis
redémarrage et relecture. Une réponse de la passerelle ne valide pas la base.

```sh
docker compose restart
```

Les volumes sont conservés lors d’un arrêt normal :

```sh
docker compose down
```

Ne pas utiliser l’option -v pour les données à conserver : elle supprime les volumes.
La sauvegarde logique et la restauration sur une base séparée restent à valider.
Les identifiants de base de .env s’appliquent à la première initialisation : les
modifier ensuite ne change pas les comptes existants dans MariaDB.

## Coût et progression

Pas de frais cloud pour cette pile locale sur une machine existante ; les coûts
habituels de la machine et de sa connexion restent ceux de son propriétaire.
Le TJM développement et la charge estimée restent séparés de l’hébergement.
Le résultat recherché reste une application avec données réellement persistées.
