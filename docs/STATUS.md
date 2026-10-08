# État du projet

Date : 9 octobre 2026
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

- Construction et démarrage de la pile locale sur une machine équipée de Docker Compose.
- Vérification des versions et compatibilités.
- Déploiement des applications, bases persistantes et comptes fictifs.

## Première preuve attendue

Patient créé dans OpenMRS, relu après reconnexion et redémarrage.
Preuve : procédure exécutée, identifiant fictif et journal de résultat.

## Prochaine action

Suivre docs/DEMARRAGE_GRATUIT.md sur la machine de développement.
Après démarrage : vérifier logs et connexion, puis configurer l’établissement et tester un patient.
La structure du dépôt public est disponible sur main.
Aucun environnement applicatif validé pour le moment.
