import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Charger les données
data = pd.read_csv("data/camembert_anchor_eval.csv")

# Fonction de catégorisation
def categorize_combined_match(gt_ville, gt_region, prediction, exact_match):
    if (pd.isna(gt_ville) or gt_ville == '') and (pd.isna(gt_region) or gt_region == '') and (pd.isna(prediction) or prediction == ''):
        return 'Empty match'
    elif exact_match == 1:
        return 'Exact match'
    else:
        return 'Non match'

# Appliquer la catégorisation
data['match_type'] = data.apply(
    lambda row: categorize_combined_match(row['gt_ville'], row['gt_region'], row['prediction'], row['exact_match']),
    axis=1
)

# Compter les occurrences par type de match
match_counts = data['match_type'].value_counts().reindex(['Exact match', 'Empty match', 'Non match'], fill_value=0)

# Créer DataFrame pour plotting
df = pd.DataFrame(match_counts).T
df.index = ['Global']
df['Total'] = df.sum(axis=1)

# Visualisation
fig, ax = plt.subplots(figsize=(5, 5))

# Barres empilées
non_match_bar = ax.bar(df.index, df['Non match'], color='lightcoral', label='Non match')
exact_match_bar = ax.bar(df.index, df['Exact match'], bottom=df['Non match'], color='mediumseagreen', label='Exact match')
empty_match_bar = ax.bar(df.index, df['Empty match'], bottom=df['Non match'] + df['Exact match'], color='slateblue', label='Empty match')

# Étiquettes sur chaque segment
for idx, row in df.iterrows():
    if row['Non match'] > 0:
        ax.text(idx, row['Non match'] / 2, str(int(row['Non match'])), ha='center', va='center', color='white', fontsize=10)
    if row['Exact match'] > 0:
        ax.text(idx, row['Non match'] + row['Exact match'] / 2, str(int(row['Exact match'])), ha='center', va='center', color='white', fontsize=10)
    if row['Empty match'] > 0:
        ax.text(idx, row['Non match'] + row['Exact match'] + row['Empty match'] / 2, str(int(row['Empty match'])), ha='center', va='center', color='black', fontsize=10)

# Valeur totale sur le dessus
for idx in range(len(df)):
    ax.text(idx, df.iloc[idx]['Total'] + 1, f"{df.iloc[idx]['Total']}", ha='center', va='bottom', fontsize=10, color='black')

# Réglages finaux du graphique
ax.set_title("Répartition des types de match (ville + région combinées)")
ax.set_ylabel("Nombre d'entrées")
ax.set_ylim(0, df['Total'].max() * 1.2)

sns.despine()
ax.legend(loc='upper right')
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_axisbelow(True)

plt.tight_layout()
plt.show()