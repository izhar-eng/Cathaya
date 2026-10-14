# Installation CIEL locale

Version retenue : CIEL v2026-09-24. Module installé : Open Concept Lab 3.1.0,
OpenMRS Platform 2.8.8. L'installation complète reste à valider.

## Source et préparation

L'export officiel est conservé. Une archive dérivée `clean-v2` corrige les
doublons de noms par locale, les variantes de casse et les noms vides, avec
priorité aux noms actifs et préférés. Ce traitement ne remplace pas la
validation OpenMRS. Les UUID et codes CIEL sont conservés.

Le fichier contient 58 870 objets concept et 58 869 identifiants externes
uniques : l'identifiant de CIEL 149996 apparaît deux fois. Les deux objets
sont conservés ; la recette vérifie les identités uniques attendues.

Une sauvegarde SQL cohérente doit être réalisée avant l'import. Vérifier le
gzip, le marqueur de fin du dump et les empreintes des archives copiées.
Ne pas versionner sauvegardes, secrets ou données patients.

## Deux phases ordonnées

L'API OpenMRS limite les envois à 75 000 000 octets. L'archive complète reste
trop volumineuse même recompressée. Les deux phases, contrôlées par CRC,
contiennent respectivement les concepts et les correspondances/relations.
Les relations sont importées après les concepts, avec les mêmes identifiants.
Les fichiers passent par l'API interne du backend : la passerelle locale
limite les envois à 20 Mo.

Le préparateur accepte un export OCL déjà normalisé et validé, avec
`concepts` dans l'en-tête et `mappings` après les concepts. Il ne normalise
pas lui-même les noms et n'est pas un validateur de schéma OCL.

```sh
python3 infra/openmrs/ciel-prepare-phases.py "$CIEL_ARCHIVE" "$CIEL_WORK"
```

Le lanceur lit les identifiants uniquement dans `.env`. Il vérifie le moteur
Docker ciblé, refuse un second lancement, refuse de démarrer pendant un
import actif, et conditionne la phase suivante à l'absence d'erreurs.
Il exige `archive-proof.json`, issu du contrôle préalable de sauvegarde.
Charger les variables de connexion Docker de l'environnement restauré avant
de l'exécuter. Adapter `--engine` et `--prefix` à la cible isolée vérifiée.

```sh
python3 infra/openmrs/ciel-install-phases.py \
  --repo "$CARTHAYA_REPO" --work "$CIEL_WORK" --status "$CIEL_STATUS" \
  "$CIEL_WORK/concepts.zip" "$CIEL_WORK/mappings.zip"
```

La surveillance écrit `progress.json` et un fichier de suivi lisible.
L'import continue dans OpenMRS si la liaison de contrôle disparaît.
Ne pas relancer un envoi, redémarrer le backend ou retirer le disque pendant
un import actif. Si la surveillance s'interrompt, inspecter les imports et
les journaux avant toute reprise ; ne pas supprimer le marqueur de lancement.

## Critères de fin

- Chaque phase a une date de fin, sans erreur générale ni élément en erreur.
- Tous les identifiants externes attendus sont présents dans `concept`.
- Authentification et relecture du patient restauré réussissent.
- Les recherches REST diabetes, malaria et hypertension retournent des résultats.

`running` indique un import en cours. `needs-review` demande un diagnostic.
`validated` signifie que les contrôles ci-dessus ont réussi. Cela ne vaut
pas recette de tous les parcours cliniques ni validation de chaque mapping.
Une relecture après redémarrage et une sauvegarde après import restent à
réaliser séparément une fois le chargement terminé.

## Références

- [Module OCL et règles de validation](https://github.com/openmrs/openmrs-module-openconceptlab)
- [Documentation officielle : import depuis un fichier](https://openmrs.atlassian.net/wiki/spaces/docs/pages/25474980/Open%2BConcept%2BLab)
- [Limite d'envoi de Platform 2.8.8](https://github.com/openmrs/openmrs-core/blob/2.8.8/web/src/main/resources/openmrs-servlet.xml)

## Réparation des neuf concepts rejetés

Le passage concepts a rencontré huit rejets de longueur et un nom français
en conflit avec un autre concept. Le réimport ciblé a traité neuf éléments
sans erreur. Douze noms dépassant 255 caractères sont conservés intégralement
en descriptions dans leur langue d’origine, avec des UUID locaux déterministes.
Ils ne sont plus utilisés comme noms de recherche ; les autres noms existants
sont conservés. Cette adaptation concerne notamment un nom français de vaccin.
Le nom français en conflit a été demandé comme synonyme non préféré ; OCL
l’a enregistré comme `INDEX_TERM`, avec le même UUID de nom.

Le script `ciel-repair-rejected.py` prépare un ZIP limité aux rejets et un
journal de transformation. Les IDs de concept, les UUID et les URLs restent
identiques. Il ne modifie ni le schéma SQL ni l’historique des imports.
L’archive officielle et l’export dérivé initial sont conservés. La comparaison
directe en base a confirmé les douze descriptions verbatim et le terme d’index
non préféré ; les neuf concepts ont été relus par REST. Les noms transférés
en description et le terme d’index sont des adaptations locales à conserver
ou à réappliquer lors d’une future mise à jour OCL.

Créer un dossier de reprise distinct après sauvegarde ; ne pas effacer le
marqueur du premier lancement. Copier la liste complète des identifiants
attendus dans le dossier de reprise. Le lanceur reçoit le ZIP des neuf concepts
corrigés, puis le ZIP des correspondances/relations. Il vérifie le réimport
avant de démarrer les relations.
