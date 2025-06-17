# Analyse du traitement des événements dans la presse régionale entre 1870 et 1914

## /explore
Dossier contenant les scripts d'exploration du corpus océrisé :
* Echantillonnage d'extraits du corpus autour du mot 'rixe' et des mots relatifs à la nationalité des étrangers concernés (italiens/belges).
* Pre-processing de l'échantillon pour annotation manuelle (ajout colonnes location_ville et location_region, en_france, participants).

## /ner
Dossier contenant les scripts de Named Entity Recognition réalisés avec le modèle camembert-ner.
* Scripts d'extraction des entités LOC (deux méthodes : une méthode avec un ancrage des chunks autour de mots clés comme rixe et bagarre et une méthode sans encrage).
* Script d'extraction avec évaluation des résultats calculée à partir de l'échantillon annoté.

## /stats
Dossier contenant un notebook permettant d'extraire des statistiques pour comparer les datasets.
