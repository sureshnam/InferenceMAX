import json
import os
from pathlib import Path
from datetime import datetime

# Collect all results
all_results = []

artifacts_dir = Path('artifacts')
if artifacts_dir.exists():
    for run_dir in artifacts_dir.iterdir():
        if run_dir.is_dir():
            # Look for agg_*.json files
            for json_file in run_dir.rglob('agg_*.json'):
                print(f"Processing {json_file}")
                try:
                    with open(json_file) as f:
                        result = json.load(f)
                    
                    # Add metadata
                    result['timestamp'] = result.get('timestamp', datetime.now().isoformat())
                    result['source_file'] = str(json_file)
                    
                    all_results.append(result)
                    print(f"  ✓ Added result: {result.get('hw')} TP{result.get('tp')} C{result.get('conc')} {result.get('precision')}")
                
                except Exception as e:
                    print(f"  ✗ Error: {e}")

# Sort by timestamp
all_results.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

# Save to results.json
with open('results.json', 'w') as f:
    json.dump(all_results, f, indent=2)

print(f"\n✅ Collected {len(all_results)} benchmark results!")
