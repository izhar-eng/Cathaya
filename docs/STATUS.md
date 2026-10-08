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
- Premier Blueprint render.yaml préparé : 4 services, 20 Go de disques persistants.
- Images figées par digest ; distribution stable 3.7.1 / Platform 2.8.8 inspectée.
- Variante Carthaya sans import de démo préparée.
- Schéma JSON officiel Render, références internes et syntaxe shell validés.

## À réaliser

- Application du Blueprint dans Carthaya Health et construction des images.
- Vérification des versions et compatibilités.
- Déploiement des applications, bases persistantes et comptes fictifs.

## Première preuve attendue

Patient créé dans OpenMRS, relu après reconnexion et redémarrage.
Preuve : procédure exécutée, identifiant fictif et journal de résultat.

## Prochaine action

Ouvrir le Blueprint depuis docs/RENDER.md dans le workspace Carthaya Health,
vérifier la région Frankfurt proposée et le coût, saisir un mot de passe admin unique, puis appliquer.
Après application : vérifier builds, démarrage et connexion avant toute preuve patient.
La structure du dépôt public est disponible sur main.
Aucun environnement applicatif validé pour le moment.
