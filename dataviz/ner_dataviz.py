import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data = pd.read_csv("data/camembert_combined_eval.csv")

# Define match categories
def categorize_match(gt, pred, exact_match):
    if (pd.isna(gt) or gt == '') and (pd.isna(pred) or pred == ''):
        return 'Empty match'
    elif exact_match == 1:
        return 'Exact match'
    else:
        return 'Non match'

# Apply categorization for ville
data['match_type_ville'] = data.apply(
    lambda row: categorize_match(row['gt_ville'], row['prediction_ville'], row['exmatch_ville']),
    axis=1
)

# Apply categorization for region
data['match_type_region'] = data.apply(
    lambda row: categorize_match(row['gt_region'], row['prediction_region'], row['exmatch_region']),
    axis=1
)

# Count per match type
ville_counts = data['match_type_ville'].value_counts().reindex(['Exact match', 'Empty match', 'Non match'], fill_value=0)
region_counts = data['match_type_region'].value_counts().reindex(['Exact match', 'Empty match', 'Non match'], fill_value=0)

# Combine into one DataFrame
df = pd.DataFrame({
    'Exact match': [ville_counts['Exact match'], region_counts['Exact match']],
    'Empty match': [ville_counts['Empty match'], region_counts['Empty match']],
    'Non match': [ville_counts['Non match'], region_counts['Non match']],
}, index=['Ville', 'Région'])

df['Total'] = df.sum(axis=1)

fig, ax = plt.subplots(figsize=(6, 5))

# Bar segments
non_match_bar = ax.bar(df.index, df['Non match'], color='lightcoral', label='Non match')
exact_match_bar = ax.bar(df.index, df['Exact match'], bottom=df['Non match'], color='mediumseagreen', label='Exact match')
empty_match_bar = ax.bar(df.index, df['Empty match'], bottom=df['Non match'] + df['Exact match'], color='slateblue', label='Empty match')

# Add text labels to each segment
for idx, row in df.iterrows():
    # Non match
    if row['Non match'] > 0:
        ax.text(idx, row['Non match'] / 2, str(int(row['Non match'])), ha='center', va='center', color='white', fontsize=10)
    # Exact match
    if row['Exact match'] > 0:
        ax.text(idx, row['Non match'] + row['Exact match'] / 2, str(int(row['Exact match'])), ha='center', va='center', color='white', fontsize=10)
    # Empty match
    if row['Empty match'] > 0:
        ax.text(idx, row['Non match'] + row['Exact match'] + row['Empty match'] / 2, str(int(row['Empty match'])), ha='center', va='center', color='black', fontsize=10)

# Add total value on top of boxes
for idx in range(len(df)):
    ax.text(idx, df.iloc[idx]['Total'] + 1, f"{df.iloc[idx]['Total']}", ha='center', va='bottom', fontsize=10, color='black')

# Final plot setup
ax.set_title("Nature des matches pour ville et région")
ax.set_ylabel("Nombre d'entrées")
ax.set_ylim(0, df['Total'].max() * 1.2)

sns.despine()
ax.legend(loc='upper right')
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_axisbelow(True)

plt.show()
