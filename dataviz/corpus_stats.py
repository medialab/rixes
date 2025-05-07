import pandas as pd
import json
import matplotlib.pyplot as plt

input_file = 'data/full_dataset_deduped.csv'


df = pd.read_csv(input_file)
# stats on the dataset (how many events per year)
df['year'] = df['year'].astype(int)

grouped = df.groupby('year')

output_json = {}

for year in sorted(grouped.groups.keys()):
    rows = grouped.get_group(year)
    print(f"{year} ({len(rows)} events)")

    event_list=[]

    for _, row in rows.iterrows():
        uniqueid = row.get('uniqueid','')
        print("\t", uniqueid)
        
        event_list.append({"uniqueid": uniqueid})

    output_json[str(year)] = event_list

    with open("data/retronews_par_annee.json", "w", encoding='utf-8') as f:
        json.dump(output_json, f, ensure_ascii=False, indent=4)

# dataviz sur stats
event_counts = df['year'].value_counts().sort_index()

plt.figure(figsize=(12, 6))
plt.plot(event_counts.index, event_counts.values, marker='o', linestyle='-', color='blue')

for year, count in zip(event_counts.index, event_counts.values):
    plt.text(year, count + 0.5, f"{year}", ha='center', va='bottom', fontsize=8, rotation=45)

plt.title("Repartition of events per year")
plt.xlabel("year")
plt.ylabel("number of events")
plt.grid(True)
plt.tight_layout()
plt.show()