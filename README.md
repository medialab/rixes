# Detecting Xenophobic Events in French Regional Press (1870-1914)

This repository contains scripts used to analyze xenophobic events targeted at Italian and Belgian people in the French regional press from 1870 to 1914.

## Repository structure
   Folder | Description |
 |--------|-------------|
 | `rixes` | Main folder containing all subfolders. |
 | `rixes/dataviz` | Contains scripts used to create visualizations of data processing results. |
 | `rixes/explore` | Contains scripts used to explore datasets. |
 | `rixes/ner` | Contains scripts used to perform Named Entity Recognition (NER) for location entities. |
 | `rixes/explode_archives` | Contains a shell script to process a dataset created manually with archival sources. |
 | `rixes/stats` | Contains scripts and a Jupyter notebook to get statistical information on the datasets used. |
 | `rixes/train_and_test` | Contains scripts used to create testing and training datasets. |
 | `rixes/events` | Contains a script used to evaluate the event overlap between the events found by a finetuned classifier and events already found with previous methods.|

### rixes/explore
* sample_rixe.py
    * As explained in extract_and_sample_rixes.md, this script samples the dataset extracted with the rixe keyword.

### rixes/dataviz
* events_repartition.py 
    * This script produces a plot which shows the repartition of events in the archives and retronews datasets.
* ner_matches.py
    * This script produces a plot which shows the amout of exact and partial matches detected between ground truth locations and locations predicted by a NER model.

### rixes/explode_archives
* explode_archives.sh
    * This shell script explodes data from the archives dataset and joins it with retronews dataset metadata and 'text' column.

### rixes/ner
This folder contains GLiNER and camembert-ner pipelines (with and without evaluation with an annotated dataset) for Named Entity Recognition, to detect towns/cities and regions in the articles. 

### rixes/stats
This folder contains scripts and a Jupyter notebook used to extract statistical data on the retronews and archives datasets.

### rixes/events
Contains a script used to evaluate the event overlap between the events found by a finetuned classifier and events already found with previous methods.