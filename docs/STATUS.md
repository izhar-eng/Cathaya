# État du projet

Date : 14 octobre 2026
Jalon actif : J1, préparation du socle.

## Réalisé

- Note de cadrage et présentation avec budgets séparés.
- Structure de dépôt publiée sur izhar-eng/Cathaya, tâches et critères de recette préparés.
- Connexion izhar-eng avec droits d’écriture vérifiés.
- Diagnostic serveur en lecture seule fourni pour une éventuelle installation Linux.
- Espace Render dédié Carthaya Health créé par le propriétaire et accès vérifié.
- Aucun service ni base PostgreSQL trouvé dans cet espace au 9 octobre 2026.
- Blueprint payant retiré du dépôt actif à la demande du propriétaire.
- Configuration Compose locale gratuite préparée : 4 services, volumes persistants.
- Images figées par digest ; distribution stable 3.7.1 / Platform 2.8.8 inspectée.
- Variante Carthaya sans import de démo préparée.
- Schéma JSON officiel Render, références internes et syntaxe shell validés.

## À réaliser

- Vérification des versions et compatibilités.
- Déploiement des applications, bases persistantes et comptes fictifs.

## Première preuve attendue

Patient restauré dans OpenMRS et relu après redémarrage : vérifié.
La création d’un nouveau patient par l’interface reste à tester.
Preuve : procédure exécutée, identifiant fictif et journal de résultat.

## Prochaine action

Traiter les erreurs de chargement de configuration, configurer l’établissement
et tester la saisie puis la relecture d’un nouveau patient fictif.
La structure du dépôt public est disponible sur main.
L’interface et l’authentification du socle restauré sont vérifiées ; la recette clinique complète reste à réaliser.

Procédure macOS avec profil Colima séparé : voir docs/MACOS.md.
La préparation de cette procédure ne valide pas son exécution.

## Reprise et restauration isolée

Une sauvegarde SQL du 12 octobre, antérieure à l'import CIEL, a été vérifiée :
intégrité gzip, marqueur de fin d'export et empreinte identique après copie.
La restauration dans une cible neuve et vide a réussi sous MariaDB 10.11.19 :
239 tables, 86 concepts et un patient du jeu de test sauvegardé.
Les sources de récupération sont conservées ; les ajouts postérieurs à cette
sauvegarde ne sont pas couverts par ce résultat.

Les quatre conteneurs de la restauration ont démarré. OpenMRS utilise une
configuration de reprise avec création de tables désactivée. L'import CIEL
massif reste suspendu. L’interface répond en HTTP 200, la connexion administrateur
est authentifiée par l’API et le patient restauré est relu par l’API REST.
Après redémarrage des quatre services, l’authentification et la relecture REST
du même patient réussissent à nouveau. La base conserve 239 tables, 86 concepts
et un patient, sans patient dépourvu de personne associée. Le démarrage contrôlé
a nécessité environ quatre minutes ; aucune réinitialisation de base.

Des erreurs de chargement de configuration (hiérarchie d’adresses et CSV)
sont présentes dans les journaux : le parcours clinique complet reste à recetter.
