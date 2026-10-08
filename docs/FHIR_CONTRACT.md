# Contrat FHIR à convenir

Cible proposée : FHIR R4. Le SIH publie les données, le tiers payant les consomme.

À préciser avec l'autre équipe : profils, champs obligatoires, systèmes
d'identifiants, référentiels, codes de prestations, unités, monnaie XOF,
statuts, corrections, annulations et récupération incrémentale.

Ressources proposées : Patient, Encounter, Condition, Observation, Procedure,
Coverage, Organization, PractitionerRole, Location, ServiceRequest, Specimen,
DiagnosticReport, MedicationRequest, MedicationDispense, MedicationAdministration,
ImagingStudy, DocumentReference, ChargeItem, Invoice et Provenance.

Cette liste est une cible de mapping. Le support réel sera vérifié pour chaque
version. Le SIH ne présume aucune éligibilité auprès des payeurs. Claim reste
optionnel selon contrat ; réponses payeurs/FSE relèvent de l'équipe tiers payant.

Livrable : exemples JSON fictifs, CapabilityStatement réel, droits d'accès,
recherches autorisées et tests de correction/annulation.
