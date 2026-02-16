#!/usr/bin/env python3
"""
Regenerate all album visualizations from the current data.
Run this script after updating Music/Data/vcl_albums.json
"""
import subprocess
import sys

scripts = [
    'create_album_timeline.py',
    'create_album_decade_breakdown.py',
    'create_presenter_decade_breakdown.py'
]

print("=" * 70)
print("REGENERATING ALL ALBUM VISUALIZATIONS")
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
    print("   - Music/Viz/album_timeline_full_dates.html")
    print("   - Music/Viz/album_decade_breakdown.html")
    print("   - Music/Viz/presenter_decade_breakdown.html")
print("=" * 70)
