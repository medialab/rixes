# Analyse du traitement des rixes dans le corpus Retronews

## Etape 1 - Echantillonnage
Prendre un échantillon du fichier contenant les extraits de presse contenant les mots 'rixe' et 'italien'.

## Etape 2 - Annotation
### Sous-étape 1 - Modification et ajout des colonnes pour annotation
Scinder la colonne location en deux :
* location_ville
* location_region

Ajouter des colonnes :
* en_france -> 0 (non) ou 1 (oui)
* xenophobe -> 0 (non) ou 1 (oui)
* participants -> EE (étranger-étranger), EF (étranger-français), FF (français-français), NA (non-applicable)

### Sous-étape 2 - Annotation manuelle de l'échantillon de 250 lignes
Annoter manuellement l'échantillon pour les colonnes :
* location_ville
* location_region
* description_of_event
* en_france
* xenophobe
* participants
