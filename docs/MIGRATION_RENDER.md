# Migration Carthaya vers Render

État vérifié le 16 octobre 2026 : préparation reprise, provisionnement bloqué.

## Cible et périmètre

Dépôt : https://github.com/izhar-eng/Cathaya
Workspace confirmé : Carthaya Health (tea-db427lijnfac73b92a20).
Premier lot : passerelle HTTPS, interface O3, API OpenMRS et MariaDB.
La migration de ce lot ne déploie pas encore Orthanc, OpenELIS, Odoo ou HAPI FHIR.
Les versions et digests préparés sont dans config/render-images.lock.json.
Les secrets et les sauvegardes restent hors Git.

## Point bloquant et décision attendue

La gratuité reste obligatoire dans les instructions actuelles.
L’inventaire Render ne renvoie aucun service dans le workspace dédié.
Free ne permet ni disque persistant ni service privé. La base PostgreSQL
Free expire après 30 jours ; elle ne remplace pas la MariaDB de cette distribution.
Aucune architecture intégrée et persistante gratuite sur Render n’est validée.
L’ancienne estimation payante dans docs/RENDER.md n’est ni une autorisation,
ni un devis actualisé. Recalculer le dimensionnement et le montant avant
provisionnement si le propriétaire accepte de modifier la contrainte de coût.
L’ancien Blueprint payant reste retiré du dépôt actif.

## Étapes de transfert après résolution du blocage

1. Contrôler la source sur le Mac : fin des imports CIEL, absence de rejets,
   authentification, patient fictif, volumes utilisés et erreurs de configuration.
   Le dernier suivi local mentionne des relations CIEL en cours le 14 octobre ;
   une fin réussie ne peut pas être déduite de ce suivi.
2. Mesurer mémoire, stockage et taille de sauvegarde. Présenter la topologie,
   les plans et le coût mensuel du seul premier lot avant toute création payante.
3. Préparer et valider le Blueprint correspondant aux ressources autorisées :
   même région pour les services, base privée, volumes MariaDB et OpenMRS,
   seule passerelle publique. Conserver les images compatibles figées.
4. Avant publication, remplacer les comptes et mots de passe locaux de test,
   injecter les secrets hors Git et vérifier les droits des comptes techniques.
5. Après arrêt des écritures et des imports, produire une sauvegarde logique
   MariaDB et une copie cohérente des fichiers OpenMRS. Vérifier les archives,
   leurs empreintes et leurs versions. Conserver les originaux locaux.
6. Restaurer dans une cible neuve, sans import de démonstration et sans
   réinitialisation du schéma. Démarrer la base puis l’API et l’interface ;
   brancher ensuite la passerelle HTTPS.
7. Recetter la connexion, les concepts et relations CIEL, la création d’un
   patient fictif et sa relecture. Redémarrer puis redéployer ; vérifier que
   le même patient, ses identifiants et les concepts sont conservés.
8. Sauvegarder la cible et tester une restauration isolée. Basculer l’usage
   seulement après ces preuves et documenter l’URL, la date et les résultats.

## Retour arrière

Conserver l’installation source et ses volumes sans les supprimer.
En cas d’échec avant bascule, poursuivre sur la source. Après bascule,
interrompre les écritures sur la cible et exporter les ajouts avant tout retour :
une source ancienne ne contient pas automatiquement les données cloud nouvelles.
Ne pas utiliser un snapshot de disque comme unique sauvegarde MariaDB.

## Preuves de recette attendues

- Dernier déploiement live et interface accessible par HTTPS.
- Authentification réussie et accès non authentifié refusé aux données cliniques.
- Patient fictif créé puis relu après redémarrage et redéploiement.
- Contrôles CIEL avant/après concordants et erreurs d’import examinées.
- Restauration isolée réussie à partir des sauvegardes de la cible.

Ces contrôles sont à réaliser ; ce document ne constitue pas leur validation.

## Références officielles vérifiées le 16 octobre 2026

- https://render.com/docs/free
- https://render.com/docs/deploy-mysql
- https://render.com/pricing
