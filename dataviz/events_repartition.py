import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

df_full = pd.read_csv("data/full_dataset_deduped.csv") # full rixe dataset

input_file = "data/archives.csv" # archives dataset
output_file = "data/archives_preprocessed.csv" # preprocessed archives dataset
colonne_cible = "date" 

df = pd.read_csv(input_file)

nb_empty_date = df['date'].isna().sum() + (df['date'] == '').sum()
print(f"Number of lines where date is empty : {nb_empty_date}")

df['date'] = df['date'].astype(str)
df['date'] = df['date'].replace(['nan', 'NaN', ''], np.nan)

# delete lines where date column is empty or NaN
df_clean = df.dropna(subset=[colonne_cible])
df_clean = df_clean[df_clean[colonne_cible] != '']
df_clean['date'] = df_clean['date'].astype(float).astype(int)
df_clean = df_clean[df_clean['date'] >= 1870]  # delete lines where the date is anterior to 1870

# region column
df_clean['region'] = pd.Series(dtype='object')
df_clean['region'] = df_clean['localite'].str.extract(r'\((.*?)\)', expand=False)
df_clean['localite'] = df_clean['localite'].str.replace(r'\s*\(.*?\)', '', regex=True).str.strip()

# normalise months
mois_map = {
    'janv.': '01', 'janvier': '01', 'févr.': '02', 'fév.':'02','février': '02', 'mars': '03',
    'avril': '04', 'mai': '05', 'juin': '06', 'juil.': '07', 'juillet': '07',
    'août': '08', 'sept.': '09', 'sept': '09', 'oct.': '10', 'nov.': '11', 'déc.': '12',
    'été': '06-07-08', 'aout':'08', 'Jun':'06', 'Déc':'12', 'Aug':'08', '22':'', '23':'', 
    '08\xa009':'08-09', 'Mar':'03', 'fin':'', 'aôut':'08','1er':'', 'May':'05', '-Dec':'12','2-3':'',
    ' et ':'-', '-05':'05', '-08':'08', '(du 6 au 10)':'', '- 06':'06', '2 ':'', '3 ':'', '7 ':'', '4 ':'', '-08':'08', '09 ()':'09', '02, 06, 10':'02-06-10',
    '111':'11', '110':'10', '5-08':'08', '-05':'05', '-06':'06', '- 06':'06', '107':'07', '01 à 04':'01-04', '-08':'08', '09()':'09'
}

region_replacements = {
    r'\bPas de C\b': 'Pas-de-Calais',
    r'\bM-et-Moselle\b': 'Meurthe-et-Moselle',
    r'\bBdR\b': 'Bouches-du-Rhône',
    r'\bHte\b': 'Haute',
    r'\barrdt\b': 'arrondissement',
    r'\bS et Marne\b': 'Seine et Marne',
    r'\bM-M-\b': 'Meurthe-et-Moselle',
    r'\bM.? et M.?\b':'Meurthe-et-Moselle',
    r'\bAlpes Marit\b':'Alpes Maritimes',
    r'\bS et L\b':'Saône et Loire',
    r'\bM-et-Moselle\b':'Meurthe-et-Moselle',
    r'\bPyr Atl\b':'Pyrénées Atlantiques',
    r'\bPyr.Orien\b':'Pyrénées Orientales'
}

# clean and normalize mois
df_clean["mois"] = df_clean["mois"].replace(mois_map, regex=True)
df_clean["mois"] = df_clean["mois"].str.replace(
    r'([a-zéàûA-Z]+)\s*-\s*([a-zéàûA-Z]+)',
    lambda m: mois_map.get(m.group(1).strip().lower(), '') + '-' + mois_map.get(m.group(2).strip().lower(), ''),
    regex=True
)
df_clean["mois"] = df_clean["mois"].str.replace(r'\(\d+(?:, \d+)*\)', '', regex=True)
df_clean['mois'] = df_clean['mois'].str.replace(r'\b(1[3-9]|[2-9][0-9]+)\b', '', regex=True)
df_clean['mois'] = df_clean['mois'].str.replace(r'\b(\d{2})\s+(\d{2})\b', r'\1-\2', regex=True)
df_clean["mois"] = df_clean["mois"].str.strip()

# clean regions
df_clean['region'] = df_clean['region'].replace(region_replacements, regex=True)

# create unique ids for archive dataset events
df_clean.reset_index(drop=True, inplace=True)
df_clean['uniqueid'] = df_clean.index.map(lambda x: f"EVT_{x + 1:04d}")

df_clean.to_csv(output_file, index=False)

# stats on the archives dataset
df_clean['date'] = df_clean['date'].astype(int)
df_full['year'] = df_full['year'].astype(int)

grouped = df_clean.groupby('date')
output_json = {}

for year in sorted(grouped.groups.keys()):
    rows = grouped.get_group(year)
    print(f"{year} ({len(rows)} events)")

    event_list = []

    for _, row in rows.iterrows():
        mois = row.get('mois', '')
        localite = row.get('localite', '')
        region = row.get('region', '')
        print("\t", mois, localite, region)

        event_list.append({
            "mois": mois,
            "localite": localite,
            "region": region
        })

    output_json[str(year)] = event_list

    with open("data/evenements_par_annee.json", "w", encoding='utf-8') as f:
        json.dump(output_json, f, ensure_ascii=False, indent=4)


counts_dataset = df_clean['date'].value_counts().sort_index()
counts_full = df_full['year'].value_counts().sort_index()

scale_factor = len(df_full) / len(input_file)
counts_dataset_scaled = counts_dataset * scale_factor

# plot
fig, ax1 = plt.subplots(figsize=(14, 7))

# y axis (primary)
color = 'tab:blue'
ax1.set_xlabel("Year")
ax1.set_ylabel("Full rixe dataset", color=color)
ax1.plot(counts_full.index, counts_full.values, color=color, marker='o', label="Full rixe dataset")
ax1.tick_params(axis='y', labelcolor=color)

for year, count in zip(counts_full.index, counts_full.values):
    ax1.text(year, count + 5, str(year), ha='center', fontsize=7, rotation=45, color=color)

# y axis (secondary)
ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel("Archives dataset", color=color)
ax2.plot(counts_dataset.index, counts_dataset.values, color=color, marker='s', linestyle='--', label="Archives dataset")
ax2.tick_params(axis='y', labelcolor=color)

for year, count in zip(counts_dataset.index, counts_dataset.values):
    ax2.text(year, count + 0.2, str(year), ha='center', fontsize=7, rotation=45, color=color)

plt.title("Repartition of events per year")
fig.tight_layout()
plt.grid(True)
plt.show()