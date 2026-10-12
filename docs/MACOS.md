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
