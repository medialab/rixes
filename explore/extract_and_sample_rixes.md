## Commandes bash / xan utilisées pour filtrer le corpus : extraire les rixes relatives aux italiens et aux belges

Afin de pouvoir rechercher des événements à caractère xénophobe ayant eu lieu en France et impliquant des italiens et/ou des belges, nous avons filtré les données du corpus à partir des mots clés "rixe" et des mots clés relatifs à la nationalité des individus :

### Pour les italiens
* "italien"
* "rital"
* "macaroni"
* "piemontais"
* "genois"
* "calabrais"

### Pour les belges
* "belge"

## Etape 1 : extraire les textes contenant les mots clés de nationalité et "rixe"

Prérequis : créer un fichier patterns.csv contenant les expréssions régulières qui vont nous permettre d'accéder aux mots clés dans le texte océrisé.

On a utilisé :
* \britals?\b
* \bpi[eé]montais?\b
* \bmacaroni?\b
* \bgenois\b
* \bcalabrais\b
* \bitaliens?\b
* \bbelges?\b

```
# Extraire les extraits dans lesquels apparaissent les mots : italien, belge, génois, piémontais, calabrais, macaroni et rital en cooccurrence avec rixe

for i in $(seq 1870 1914); do # Exécuter la boucle pour chaque dossier année
    PRESSE="/home/lilla/retronews/${i}/ocr.csv.gz"; # Variable fichiers OCR
    METADONNEES="/home/lilla/retronews/${i}/docs.csv"; # Variable fichiers métadonnées
    xan map $i year $PRESSE | \ 
    xan map 'concat(year, document_id, article_id, block_id)' uniqueid |\
    xan search -s text -ri "rixe" |\
    xan regex-join text - pattern patterns.csv -t 8 | \
    xan implode pattern -P --cmp uniqueid | \
    xan join document_id  - document_id $METADONNEES --left >> matches.csv
    done 
    # Une colonne uniqueid est créée à partir des colonnes year, document_id, article_id et block_id du fichier de métadonnées.
    # On récupère les extraits où le mot rixe apparaît puis on filtre avec les mots désignant des italiens ou des belges.

```
Pour vérifier combien de lignes on a au total :

```xan count matches.csv```

Pour visualiser le fichier de sortie dans un pager :

```xan view -p matches.csv```

Pour visualiser les entrées complètes (notamment pour la colonne text) du fichier de sortie :

```xan flatten matches.csv```

## Etape 2 : supprimer les lignes superflues ajoutées au fichier de sortie

Comme le filtrage a été fait au moyen d'une boucle, à chaque nouveau dossier année les headers du fichier csv étaient rajoutés dans le fichier de sortie, ce qui a créé des lignes inutiles.

``` xan search -v -s uniqueid uniqueid -e matches.csv |xan sort -s year > result.csv ```

## Etape 3 : vérifier le nombre de lignes présentes dans le csv et que les lignes inutiles ont bien été supprimées

```xan count result.csv```

## Etape 4 : créer un échantillon de result.csv pour préparer l'annotation manuelle des résultats

On génère un échantillon de 250 lignes représentatives du fichier entier.

```xan sample 250 result.csv > sample_result.csv```

## Etape 5 : mélanger les lignes de l'échantillon pour annoter dans un ordre non-chronologique (garantir que l'annotation est représentative même si incomplète)

```xan shuffle sample_result.csv > sample_result_shuffled.csv```