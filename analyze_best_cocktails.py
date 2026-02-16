#!/usr/bin/env python3
import json
import pandas as pd
from collections import Counter

# load data
with open('cocktail_history.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)

# analyze by host
hosts = df['host'].unique()

print("=" * 60)
print("COCKTAIL LIST ANALYSIS BY HOST")
print("=" * 60)

for host in sorted(hosts):
    host_df = df[df['host'] == host]

    print(f"\n{host.upper()} ({len(host_df)} cocktails)")
    print("-" * 40)

    # diversity metrics
    unique_countries = host_df['country_of_origin'].nunique()
    unique_liquors = host_df['primary_liquor'].nunique()

    print(f"Country diversity: {unique_countries} countries")
    print(f"  {', '.join(host_df['country_of_origin'].value_counts().head(3).index.tolist())}")

    print(f"Liquor diversity: {unique_liquors} types")
    print(f"  {', '.join(host_df['primary_liquor'].value_counts().head(3).index.tolist())}")

    # era analysis
    years = host_df['year_invented'].dropna()
    if len(years) > 0:
        avg_year = years.mean()
        oldest = years.min()
        newest = years.max()
        print(f"Era: avg {int(avg_year)}, range {int(oldest)}-{int(newest)}")

        # classic vs modern split
        classics = sum(years < 1980)
        modern = sum(years >= 1980)
        print(f"  Classic (pre-1980): {classics}, Modern (1980+): {modern}")

    # notable cocktails
    print(f"Cocktails:")
    for _, row in host_df.iterrows():
        year = f"({int(row['year_invented'])})" if pd.notna(row['year_invented']) else ""
        print(f"  • {row['cocktail']} {year}")

# overall diversity scores
print("\n" + "=" * 60)
print("DIVERSITY RANKINGS")
print("=" * 60)

diversity_scores = []
for host in sorted(hosts):
    host_df = df[df['host'] == host]

    score = {
        'host': host,
        'total': len(host_df),
        'countries': host_df['country_of_origin'].nunique(),
        'liquors': host_df['primary_liquor'].nunique(),
        'era_spread': host_df['year_invented'].max() - host_df['year_invented'].min() if len(host_df['year_invented'].dropna()) > 0 else 0
    }

    # calculate diversity score (normalized)
    score['diversity_score'] = (
        score['countries'] * 2 +  # weight country diversity more
        score['liquors'] * 1.5 +
        (score['era_spread'] / 50)  # normalize era spread
    )

    diversity_scores.append(score)

# sort by diversity
diversity_scores.sort(key=lambda x: x['diversity_score'], reverse=True)

print("\nBy Overall Diversity:")
for i, s in enumerate(diversity_scores, 1):
    print(f"{i}. {s['host']}: score {s['diversity_score']:.1f} "
          f"({s['countries']} countries, {s['liquors']} liquors, {int(s['era_spread'])}yr span)")

# most adventurous (obscure/modern cocktails)
print("\nMost Adventurous (modern/custom cocktails):")
for host in sorted(hosts):
    host_df = df[df['host'] == host]
    modern = sum(host_df['year_invented'] >= 2000)
    pct = (modern / len(host_df)) * 100
    print(f"  {host}: {modern}/{len(host_df)} ({pct:.0f}%) post-2000")

# most classic (old cocktails)
print("\nMost Classic (pre-1900 cocktails):")
for host in sorted(hosts):
    host_df = df[df['host'] == host]
    classic = sum(host_df['year_invented'] < 1900)
    pct = (classic / len(host_df)) * 100 if len(host_df) > 0 else 0
    print(f"  {host}: {classic}/{len(host_df)} ({pct:.0f}%) pre-1900")

# most international
print("\nMost International (non-USA cocktails):")
for host in sorted(hosts):
    host_df = df[df['host'] == host]
    non_usa = sum(host_df['country_of_origin'] != 'USA')
    pct = (non_usa / len(host_df)) * 100
    print(f"  {host}: {non_usa}/{len(host_df)} ({pct:.0f}%) non-USA")

print("\n" + "=" * 60)
