# macOS : environnement gratuit séparé

Cette procédure prépare un profil Colima dédié au premier bloc Carthaya,
indépendant des données de Docker Desktop. Les anciens volumes ne sont pas
importés. Le stockage de la VM doit être placé sur un volume externe monté et
accessible en écriture ; APFS est recommandé pour cet essai. Ne pas reformater
un disque contenant des données pour appliquer cette procédure.

## Préparation

Installer Colima et Lima depuis leur source officielle. Vérifier l’espace libre,
la mémoire disponible et la présence de Rosetta sur Apple Silicon. Les images
inspectées sont amd64 ; compose.macos.yaml fixe la plateforme et limite le tas
Java à 2 Gio pour une VM de test de 4 Gio. La suite complète demande son propre
dimensionnement.

Définir CARTHAYA_STORAGE avec le chemin réel du volume externe monté et
CARTHAYA_REPO avec le chemin du dépôt cloné. Créer les dossiers AVANT d’utiliser
COLIMA_HOME : Colima 0.10.3 ignore cette variable si son chemin n’existe pas.
Ne pas lancer ces commandes si le volume externe n’est pas monté.

```sh
: "${CARTHAYA_STORAGE:?Définir le chemin du volume externe monté}"
: "${CARTHAYA_REPO:?Définir le chemin du dépôt}"
mkdir -p "$CARTHAYA_STORAGE/colima/_lima" "$CARTHAYA_STORAGE/colima-cache"
export COLIMA_HOME="$CARTHAYA_STORAGE/colima"
export LIMA_HOME="$CARTHAYA_STORAGE/colima/_lima"
export COLIMA_CACHE_HOME="$CARTHAYA_STORAGE/colima-cache"
colima start carthaya --vm-type vz --vz-rosetta --cpus 2 --memory 4 --disk 40 --activate=false --ssh-config=false --mount none
cd "$CARTHAYA_REPO"
docker --context colima-carthaya compose -f compose.yaml -f compose.macos.yaml config --quiet
docker --context colima-carthaya compose -f compose.yaml -f compose.macos.yaml up -d --build
docker --context colima-carthaya compose -f compose.yaml -f compose.macos.yaml ps
```

Configurer un DOCKER_CONFIG séparé pour isoler le client et ses contextes si
nécessaire. Ses plugins Compose et Buildx doivent être disponibles. Conserver
les mots de passe applicatifs dans .env, exclu de Git. Lire aussi
DEMARRAGE_GRATUIT.md pour l’initialisation, les comptes et les critères de preuve.
L’interface attendue est http://localhost:8080/openmrs/spa/.

## Arrêt et données

Avec les mêmes variables de stockage et le même client Docker :

```sh
docker --context colima-carthaya compose -f compose.yaml -f compose.macos.yaml down
colima stop carthaya
```

Arrêter Colima avant de démonter le volume. Ne pas utiliser down -v ni
colima delete --data sur une instance contenant des données à conserver.
Les volumes nommés résident dans le disque virtuel Colima externe ; la sauvegarde
logique de la base et sa restauration restent une recette distincte.
Une procédure préparée ne constitue pas une preuve de démarrage ou de persistance.

Sources : https://github.com/abiosoft/colima/blob/v0.10.3/config/files.go,
https://colima.run/docs/installation/ et https://colima.run/docs/commands/.

## Dépannage du réseau et du relais

Si la VM ne reçoit pas d'adresse avec le réseau utilisateur, Lima propose
le réseau natif vzNAT. Dans le LIMA_HOME réservé à ce projet, l'override
`_config/override.yaml` peut contenir :

```yaml
networks:
  - vzNAT: true
```

Arrêter puis relancer uniquement la VM pour appliquer cette modification.
Ce changement ne demande pas de redémarrer le Mac. Vérifier la connexion SSH
et le service Docker dans la VM avant de construire les applications.

Si le service Docker est actif dans la VM mais que son relais Unix échoue,
un tunnel SSH distinct permet de tester la connexion. Dans un terminal :

```sh
ssh -F "$LIMA_HOME/colima-carthaya/ssh.config" -o ControlMaster=no -o ControlPath=none -o ExitOnForwardFailure=yes -N -L "$CARTHAYA_STORAGE/carthaya-engine.sock:/var/run/docker.sock" lima-colima-carthaya
```

Dans un autre terminal, avec les mêmes variables et le même DOCKER_CONFIG :

```sh
export DOCKER_HOST="unix://$CARTHAYA_STORAGE/carthaya-engine.sock"
docker info
cd "$CARTHAYA_REPO"
docker compose -f compose.yaml -f compose.macos.yaml up -d --build
```

Utiliser DOCKER_HOST sans l'option --context dans ce cas, pour que Compose et
BuildKit héritent du même moteur. Le tunnel doit rester ouvert pendant son
utilisation. Il faut le recréer après un arrêt de la VM ; ce dépannage ne remplace
pas la validation du cycle complet de démarrage et d'arrêt.

Source réseau : https://lima-vm.io/docs/config/network/vmnet/.

## Reprise depuis une sauvegarde SQL

Conserver la source de récupération et travailler dans un autre moteur et un
autre projet Compose. Contrôler l'intégrité gzip, le marqueur de fin de dump et
l'empreinte après copie. Vérifier la version MariaDB source et la compatibilité
du schéma. Le chargement SQL doit viser une base vide, avec le backend arrêté.

Après une restauration réussie, ajouter compose.restore.yaml aux fichiers
Compose pour désactiver la création de tables. Vérifier les comptages SQL,
l'authentification et la relecture d'un dossier avant et après redémarrage.
Une sauvegarde antérieure à un import ne couvre pas les ajouts de cet import.
Ne pas reprendre un import massif avant validation de l'environnement restauré.

Pour Lima sur macOS, conserver un chemin réel court et un nom de profil court :
les liens symboliques peuvent être résolus avant le contrôle de longueur des
sockets SSH. Vérifier cette longueur avant de créer un gros disque virtuel.
