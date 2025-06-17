# script to explode archive data and join it with retronews dataset metadata and text column

# keep only rows with values
#xan search -N -s retronews_uniqueid archives_annotated_notfound.csv |\

# transform to split and keep only 5 first uniqueids for each row
xan transform retronews_uniqueid '_.split("|") | _[:min(5,_.len())]' data/archives_annotated_notfound.csv > data/archives_split.csv
# explode on uniqueid column and remove rows where no uniqueid has been identified
xan explode retronews_uniqueid --drop-empty data/archives_split.csv > data/exploded_archives_annotated.csv
# copy rows (metadata and text) from the etrangers files
xan cat rows /store/retronews/etrangers/*.csv |\
# join both datasets on uniqueid columns
xan join --left retronews_uniqueid data/exploded_archives_annotated.csv uniqueid - |\
# shuffle output file
xan shuffle --in-memory > data/archives_retronews_shuffled.csv
