Nombre de lignes total : `xan parallel count ./**/ocr.csv.gz` -> 348 043 765

Nombre de revues :
- `xan parallel count ./**/docs.csv` : 473725
Mais que 472755 de remplies

Langue des revues : `xan parallel freq -s document_lang ./**/docs.csv | xan view`

┌───┬───────────────┬───────┬────────┐
│ - │ field         │ value │ count  │
├───┼───────────────┼───────┼────────┤
│ 0 │ document_lang │ fr    │ 436591 │
│ 1 │ document_lang │ de    │ 37128  │
│ 2 │ document_lang │ it    │ 6      │
└───┴───────────────┴───────┴────────┘

Revues les plus fréquentes : `xan parallel freq -s document_publication_title ./**/docs.csv | xan view`

┌───┬────────────────────────────┬───────────────────────────────────────────┬───────┐
│ - │ field                      │ value                                     │ count │
├───┼────────────────────────────┼───────────────────────────────────────────┼───────┤
│ 0 │ document_publication_title │ Neue Mülhauser Zeitung                    │ 18872 │
│ 1 │ document_publication_title │ Mémorial de la Loire et de la Haute-Loire │ 16054 │
│ 2 │ document_publication_title │ Le Petit Marseillais                      │ 15996 │
│ 3 │ document_publication_title │ Le Phare de la Loire                      │ 15981 │
│ 4 │ document_publication_title │ Le Progrès de la Côte-d'Or                │ 15488 │
│ 5 │ document_publication_title │ La Gironde                                │ 15444 │
│ 6 │ document_publication_title │ La Petite Gironde                         │ 15034 │
│ 7 │ document_publication_title │ Courrier de Saône-et-Loire                │ 14364 │
│ 8 │ document_publication_title │ La Dépêche (Toulouse)                     │ 14140 │
│ 9 │ document_publication_title │ Le Sémaphore de Marseille                 │ 13905 │
│ … │ …                          │ …                                         │ …     │
└───┴────────────────────────────┴───────────────────────────────────────────┴───────┘


Environ 10-15% de tokens mal ocrisés
Exemples :
 
document_id 3901283
text        Va* r-dr-t tr dr F Srma-in rr. — Contrairement â ce qui m- pa««r d m-le* bleu Charente-. « c -ont l •* weedews <|fii lontileijut «Lin* I Vrmagnac; le* mur* sont «loue dcmeuri-s Ire* ferme* au «lernler mare hc «le i.ontlom, son*changement *ut ccuxqu- n >u* donnions il y a huit jour*.
tokens      srma-in

document_id 5301218
text        L’orateur a fait l'historique eu régime pitrlwui'vilKîftt action et rappais l^^surt^das gens qui uut cutané sé ta Haute Cour: la mort venant supprimer brusquement N. Walde<*-Rou»»eau au moment où semici ni lait atteindre l'apogée de sa carrière politique. , — L'exil ne m’a rien fait oublier, dit-il. et je 1 vous reviens plus républioaitt et plu» patriote
tokens      pitrlwui



Thèmes :
- massacre
- attentats / attentat
- racisme_et_xenophobie
- terrorisme
- torture_et_punition_corporelle
- ethnologie
- crime_de_guerre / crimes_de_guerre


Périodicité des journaux : `xan parallel freq -s document_publication_periodicity ./**/docs.csv | xan view`

┌────┬──────────────────────────────────┬─────────────────────────┬────────┐
│ -  │ field                            │ value                   │ count  │
├────┼──────────────────────────────────┼─────────────────────────┼────────┤
│ 0  │ document_publication_periodicity │ Quotidien               │ 288817 │
│ 1  │ document_publication_periodicity │ Hebdomadaire            │ 77792  │
│ 2  │ document_publication_periodicity │ Bihebdomadaire          │ 71586  │
│ 3  │ document_publication_periodicity │ Trihebdomadaire         │ 13108  │
│ 4  │ document_publication_periodicity │ Quatre fois par semaine │ 12484  │
│ 5  │ document_publication_periodicity │ Inconnu                 │ 9428   │
│ 6  │ document_publication_periodicity │ Mensuel                 │ 317    │
│ 7  │ document_publication_periodicity │ Bimensuel               │ 119    │
│ 8  │ document_publication_periodicity │ Trimensuel              │ 64     │
│ 9  │ document_publication_periodicity │ Irrégulier              │ 6      │
│ 10 │ document_publication_periodicity │ Annuel                  │ 4      │
└────┴──────────────────────────────────┴─────────────────────────┴────────┘

Régions : `xan parallel freq -s document_publication_region ./**/docs.csv | xan view`

┌────┬─────────────────────────────┬────────────────────────────┬────────┐
│ -  │ field                       │ value                      │ count  │
├────┼─────────────────────────────┼────────────────────────────┼────────┤
│ 0  │ document_publication_region │ Grand Est                  │ 101558 │
│ 1  │ document_publication_region │ Nouvelle-Aquitaine         │ 74779  │
│ 2  │ document_publication_region │ Centre-Val de Loire        │ 47115  │
│ 3  │ document_publication_region │ Bourgogne-Franche-Comté    │ 46695  │
│ 4  │ document_publication_region │ Pays de la Loire           │ 44166  │
│ 5  │ document_publication_region │ Provence-Alpes-Côte d'Azur │ 43051  │
│ 6  │ document_publication_region │ Auvergne-Rhône-Alpes       │ 37280  │
│ 7  │ document_publication_region │ Hauts-de-France            │ 32449  │
│ 8  │ document_publication_region │ Occitanie                  │ 22283  │
│ 9  │ document_publication_region │ Île-de-France              │ 16973  │
│ 10 │ document_publication_region │ Bretagne                   │ 5764   │
│ 11 │ document_publication_region │ Martinique                 │ 1033   │
│ 12 │ document_publication_region │ Normandie                  │ 436    │
│ 13 │ document_publication_region │ Guyane                     │ 119    │
│ 14 │ document_publication_region │ Corse                      │ 24     │
└────┴─────────────────────────────┴────────────────────────────┴────────┘


Lieux les plus cités : `xan p freq -s entities_geo -P "search -s entities_geo ." ./**/ocr.csv.gz --progress | xan view -l10`

┌───┬──────────────┬───────────┬─────────┐
│ - │ field        │ value     │ count   │
├───┼──────────────┼───────────┼─────────┤
│ 0 │ entities_geo │ Paris     │ 3276381 │
│ 1 │ entities_geo │ France    │ 1467520 │
│ 2 │ entities_geo │ Bordeaux  │ 1174797 │
│ 3 │ entities_geo │ Marseille │ 1006010 │
│ 4 │ entities_geo │ Londres   │ 484735  │
│ 5 │ entities_geo │ Die       │ 468319  │
│ 6 │ entities_geo │ Nantes    │ 433256  │
│ 7 │ entities_geo │ Troyes    │ 346297  │
│ 8 │ entities_geo │ Tours     │ 335451  │
│ 9 │ entities_geo │ Amiens    │ 304330  │
│ … │ …            │ …         │ …       │
└───┴──────────────┴───────────┴─────────┘



Nombre de revues par année : `xan parallel count -S name ./**/docs.csv -P 'search -s document_lang fr' | xan sort | xan transform name name[2:6] | xan hist -v count -l name -S`

1870 | 4,230   0.97%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                                                                                             |
1871 | 4,563   1.05%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                                                                                        |
1872 | 5,108   1.17%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                                                                                 |
1873 | 5,789   1.33%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                                                                       |
1874 | 5,543   1.27%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                                                                           |
1875 | 5,924   1.36%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                                                                     |
1876 | 6,433   1.47%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                                                              |
1877 | 6,498   1.49%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                                                             |
1878 | 6,691   1.53%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                                                           |
1879 | 7,137   1.63%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                                                     |
1880 | 7,252   1.66%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                                                   |
1881 | 7,334   1.68%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                                                  |
1882 | 8,029   1.84%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                                        |
1883 | 7,894   1.81%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                                          |
1884 | 8,757   2.01%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                              |
1885 | 9,224   2.11%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                        |
1886 | 9,592   2.20%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                   |
1887 | 9,822   2.25%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                               |
1888 | 9,808   2.25%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                                |
1889 |10,314   2.36%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                         |
1890 |10,725   2.46%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                   |
1891 |10,590   2.43%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸                     |
1892 |11,028   2.53%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸               |
1893 |11,501   2.63%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸        |
1894 |11,594   2.66%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸       |
1895 |11,565   2.65%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸       |
1896 |11,455   2.62%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸         |
1897 |11,514   2.64%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸        |
1898 |11,678   2.67%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸      |
1899 |11,733   2.69%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸     |
1900 |11,906   2.73%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸  |
1901 |12,031   2.76%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ |
1902 |11,949   2.74%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸  |
1903 |11,922   2.73%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸  |
1904 |11,985   2.75%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ |
1905 |11,836   2.71%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸   |
1906 |12,120   2.78%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|
1907 |12,078   2.77%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸|
1908 |11,920   2.73%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸  |
1909 |11,832   2.71%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸   |
1910 |11,906   2.73%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸  |
1911 |12,024   2.75%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ |
1912 |11,458   2.62%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸         |
1913 |11,298   2.59%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸           |
1914 |11,001   2.52%|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸               |


Exemple de passages :

En cherchant immigration dans le text de l'année 1883 :

document_id                           3998179
page                                  2
block_id                              PAG_00000002_TB000148
text                                  Si les Américains font accueil aux Irlandais, aux Allemands, a tous les émigrants d’Europe. I ur hostilité a l’égard des Chinois s’accentue chaque jour davantage. A San-Francisco, et dons la plupart d<s villes de la Californie et des province» voisines, l'agitation antichinoisc prend des proportions redoutables. Il y a quelques jours, les Aiso-ialions ouvrières réunies sous les auspices des kn gels o* labour ichcxaliers du travail) ont fait un- démonstration en faveur de l’expulsion totale des Chinois et de l'inlenliction de l’immigration asiatique. Un» assemblée de délégués ouvriers a voté des résolutions invitant tous les Chinois à quitter immédiatement San-Francisco et la côte du Pacifique. A Sacramento, on organise une ligue des ouvriers et des gens d'affaires en vue de fermer aux Chinois l’accès des ateliers. On signale aussi les menées dè certains socialistes qui projetaient de faire sauter avec de la dynamite le quartier chinois dj SanFrancisco. Quatre de ces dynamitais viennent d’être arrêtés; l'autorité a, parait-il, trouvé chez eux tous les détails du complut, dont le point de départ devait être l’assassinat du gouverneur provincial et du maire de San Francisco, coupables de protéger les Chinois contre les ouvriers blancs.
vpos                                  2751
hpos                                  5736
width                                 1085
height                                1017
word_offset                           4781
word_count                            199
font_size                             8
article_id                            96b5eda558073615a3d85f30b665edf4
themes                                assassinat
entities_geo                          Europe
entities_person                       <empty>
entities_function                     <empty>
entities_organisation                 <empty>
entities_person_firstname             <empty>
entities_person_function              <empty>
entities_function_organisation        <empty>
entities_organisation_person_function <empty>
entities_person_organisation          <empty>


