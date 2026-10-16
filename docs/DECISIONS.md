# Décisions

| Date | Décision | Statut |
| --- | --- | --- |
| 2026-10-08 | Nom Carthaya Health et projet indépendant de FIT | Confirmé |
| 2026-10-08 | Première version sur bases neuves avec données fictives persistées | Confirmé |
| 2026-10-08 | Tiers payant/FSE par une équipe distincte, interface FHIR | Confirmé |
| 2026-10-08 | TJM développement de 300 EUR HT | Confirmé |
| 2026-10-08 | Budgets développement et moyens techniques séparés | Confirmé |
| 2026-10-08 | Cible de 12 semaines sous disponibilité des intervenants et référents | Planification provisoire |
| 2026-10-08 | Dépôt fourni : izhar-eng/Cathaya | Initialisé, public |
| 2026-10-08 | Accès en écriture de la connexion GitHub izhar-eng | Vérifié |
| 2026-10-09 | Publication des documents et budgets sur le dépôt public | Autorisée explicitement |
| 2026-10-09 | Hébergeur Render et workspace dédié Carthaya Health | Confirmé et accès vérifié |
| 2026-10-09 | Région Frankfurt pour le premier bloc de développement | Proposition dans le Blueprint, à vérifier avant Apply |
| 2026-10-09 | Domaines Render par défaut pour le démarrage | Configuration prévue |
| 2026-10-08 | Versions, images et moteurs de bases par composant | À vérifier |
| 2026-10-08 | Édition et modules Odoo | À confirmer |


Le tag amont 3.7.x-no-demo a été écarté : ses propriétés annoncent 3.8.0-SNAPSHOT et Platform 2.8.10-SNAPSHOT. La variante Carthaya repose sur les artefacts stables 3.7.1 / 2.8.8, épinglés par digest.

Décision du 9 octobre 2026 : démarrage exclusivement gratuit, instruction du propriétaire.

Le Blueprint Render payant est retiré du dépôt actif. Il reste dans l’historique Git.
La configuration locale à volumes persistants est proposée pour tester réellement OpenMRS
sans frais cloud. Le workspace dédié Render ne reçoit aucun service payant.

Procédure macOS avec profil Colima séparé : voir docs/MACOS.md.
La préparation de cette procédure ne valide pas son exécution.

## Reprise du 14 octobre 2026

La remise en service part d'une sauvegarde logique antérieure à l'import CIEL,
restaurée dans une cible séparée. Les sources de récupération sont conservées.
La création de tables est désactivée pour démarrer OpenMRS sur le schéma restauré.
L’import du dictionnaire est autorisé après validation de l’accès et de la persistance.
Ce résultat ne constitue pas une restauration intégrale des ajouts postérieurs
à la sauvegarde.

La connexion administrateur et la relecture du patient restauré par API ont été
vérifiées. Cette preuve porte sur le dossier déjà sauvegardé ; la saisie d’un
nouveau patient et la recette clinique restent des étapes distinctes.

La persistance du patient restauré et l’authentification après redémarrage des
quatre services sont vérifiées. Les erreurs de configuration signalées au
démarrage sont à traiter avant de valider un parcours clinique complet.

Installation CIEL explicitement demandée le 14 octobre. Import par ZIP local
en deux phases ordonnées pour respecter la limite d’envoi OpenMRS, sans
réinitialiser les données. Sauvegarde avant import obligatoire. La phase
relations est retenue si des erreurs subsistent dans la phase concepts.
Un chargement partiel ne vaut pas installation validée.

Correction des neuf rejets demandée explicitement le 14 octobre. Réimport
ciblé par OCL après sauvegarde, sans modification du schéma ni troncature
de termes médicaux : noms trop longs conservés en description, nom français
conflictuel conservé comme terme d’index non préféré. Adaptations locales
auditées ; codes et identités conceptuelles préservés. L’import historique
reste enregistré comme échoué ; un import de réparation sans erreur fournit
la preuve de résolution.

## Reprise Render — 16 octobre 2026

Workspace Carthaya Health confirmé par le propriétaire dans cette session.
L’inventaire des services est vide. L’instruction de reprise n’est pas une
levée de la restriction de gratuité : aucun provisionnement payant autorisé.
La cible OpenMRS/MariaDB et ses données persistantes sont conservées ; aucune
substitution PostgreSQL, base éphémère ou interface seule n’est déployée.
