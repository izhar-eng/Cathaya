# Scénarios de recette

| ID | Scénario | Preuve attendue |
| --- | --- | --- |
| A01 | Installation vierge sans fixtures | Applications accessibles et bases initialisées |
| A02 | Création/relecture après redémarrage | Même patient fictif et valeurs persistées |
| A03 | Consultation avec médicaments | Prescription, délivrance et stock cohérents |
| A04 | Examen de laboratoire | Demande, échantillon et résultat validé liés |
| A05 | Imagerie | Étude DICOM et compte rendu liés au patient/visite |
| A06 | Séjour avec transfert | Occupation des lits et sortie cohérentes |
| A07 | Délivrance partielle/lot expiré | Reliquat exact et contrôle du lot |
| A08 | Résultat corrigé | Version et provenance visibles |
| A09 | Facture annulée et rejeu | Aucun doublon de facture ou de mouvement |
| A10 | Consommation externe FHIR | Identifiants, statuts et montants convenus |
| A11 | Accès interdit | Refus effectif par rôle |
| A12 | Restauration | Bases et images restaurées et relues |

Les scénarios ne sont pas encore exécutés. Chaque preuve indique l'environnement,
la version Git, les données fictives, la date et le résultat observé.
