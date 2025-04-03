import pandas as pd
import numpy as np

def reduce_csv(input_file, output_file, sample_size=250, keep_first_n=25): # Garder les 25 premières lignes déjà annotées à la main
    df = pd.read_csv(input_file)
    
    # Extraire les 4 premiers caractères de 'unique_id' pour la récupérer la date
    df['year'] = df['uniqueid'].str[:4]

    # Filtrer les années entre 1870 et 1914
    df = df[df['year'].between('1870', '1914')]

    # Garder les 25 premières lignes
    df_first_25 = df.head(keep_first_n)

    # Créer un échantillon représentatif en se basant sur les dates
    remaining_df = df.iloc[keep_first_n:]

    # Calculer la distribution des dates sur tout le document
    year_counts = remaining_df['year'].value_counts().sort_index()

    # Calculer la proportion de chaque année dans les données
    year_proportions = year_counts / len(remaining_df)

    # Calculer combien de lignes à prendre pour chaque année
    sample_per_year = (year_proportions * (sample_size - keep_first_n)).round().astype(int)

    # Échantillonner
    sampled_rows = []
    for year, count in sample_per_year.items():
        sampled_rows.append(remaining_df[remaining_df['year'] == year].sample(n=count, random_state=42))

    # Concatenation de l'échantillon avec les 25 premières lignes
    final_sampled_df = pd.concat([df_first_25] + sampled_rows, ignore_index=True)

    # Nouveau fichier csv
    final_sampled_df.to_csv(output_file, index=False)
    print(f"Fichier réduit sauvegardé: {output_file}")

input_file = '/home/lilla/Downloads/rixe_italiens_full_annote.csv' 
output_file = '/home/lilla/sample_annotations_rixe.csv'  
reduce_csv(input_file, output_file)
