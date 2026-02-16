#!/usr/bin/env python3
"""
Regenerate all cocktail visualizations from the current data.
Run this script after updating Cocktail/Data/cocktail_history.json
"""
import subprocess
import sys

scripts = [
    'create_cocktail_timeline.py',
    'create_origin_map.py',
    'create_host_stacked_bars.py',
    'create_dashboard.py'
]

print("=" * 70)
print("REGENERATING ALL COCKTAIL VISUALIZATIONS")
print("=" * 70)

failed = []
for script in scripts:
    print(f"\n▶ Running {script}...")
    print("-" * 70)
    try:
        result = subprocess.run(['python3', script], capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR running {script}")
        print(e.stdout)
        print(e.stderr, file=sys.stderr)
        failed.append(script)

print("\n" + "=" * 70)
if failed:
    print(f"❌ FAILED: {len(failed)} script(s) failed:")
    for script in failed:
        print(f"   - {script}")
    sys.exit(1)
else:
    print("✅ SUCCESS: All visualizations regenerated!")
    print("\nUpdated files:")
    print("   - Cocktail/Viz/cocktail_timeline.html")
    print("   - Cocktail/Viz/cocktail_origin_map.html")
    print("   - Cocktail/Viz/cocktail_origin_map_us.html")
    print("   - Cocktail/Viz/cocktails_by_host_stacked.html")
    print("   - Cocktail/Viz/vcl_cocktail_dashboard.html")
print("=" * 70)
