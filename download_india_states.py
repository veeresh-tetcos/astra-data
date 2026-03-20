#!/usr/bin/env python3
"""
download_india_states.py

Download Indian state/UT GeoJSON boundary files from GitHub.
Source: https://github.com/udit-001/india-maps-data
"""

import json
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# Base URL for raw GeoJSON files
BASE_URL = "https://raw.githubusercontent.com/udit-001/india-maps-data/main/geojson/states"

# Output directory (relative to project root)
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "boundaries" / "india"

# All Indian states and union territories with their file names
# Format: (file_name_on_github, local_file_name)
STATES_AND_UTS = [
    # States (28)
    ("andhra-pradesh.geojson", "andhra_pradesh.geojson"),
    ("arunachal-pradesh.geojson", "arunachal_pradesh.geojson"),
    ("assam.geojson", "assam.geojson"),
    ("bihar.geojson", "bihar.geojson"),
    ("chhattisgarh.geojson", "chhattisgarh.geojson"),
    ("goa.geojson", "goa.geojson"),
    ("gujarat.geojson", "gujarat.geojson"),
    ("haryana.geojson", "haryana.geojson"),
    ("himachal-pradesh.geojson", "himachal_pradesh.geojson"),
    ("jharkhand.geojson", "jharkhand.geojson"),
    ("karnataka.geojson", "karnataka.geojson"),
    ("kerala.geojson", "kerala.geojson"),
    ("madhya-pradesh.geojson", "madhya_pradesh.geojson"),
    ("maharashtra.geojson", "maharashtra.geojson"),
    ("manipur.geojson", "manipur.geojson"),
    ("meghalaya.geojson", "meghalaya.geojson"),
    ("mizoram.geojson", "mizoram.geojson"),
    ("nagaland.geojson", "nagaland.geojson"),
    ("odisha.geojson", "odisha.geojson"),
    ("punjab.geojson", "punjab.geojson"),
    ("rajasthan.geojson", "rajasthan.geojson"),
    ("sikkim.geojson", "sikkim.geojson"),
    ("tamil-nadu.geojson", "tamil_nadu.geojson"),
    ("telangana.geojson", "telangana.geojson"),
    ("tripura.geojson", "tripura.geojson"),
    ("uttar-pradesh.geojson", "uttar_pradesh.geojson"),
    ("uttarakhand.geojson", "uttarakhand.geojson"),
    ("west-bengal.geojson", "west_bengal.geojson"),
    # Union Territories (8)
    ("andaman-and-nicobar-islands.geojson", "andaman_and_nicobar_islands.geojson"),
    ("chandigarh.geojson", "chandigarh.geojson"),
    ("dnh-and-dd.geojson", "dadra_nagar_haveli_daman_diu.geojson"),
    ("delhi.geojson", "delhi.geojson"),
    ("jammu-and-kashmir.geojson", "jammu_and_kashmir.geojson"),
    ("ladakh.geojson", "ladakh.geojson"),
    ("lakshadweep.geojson", "lakshadweep.geojson"),
    ("puducherry.geojson", "puducherry.geojson"),
]


def download_file(url: str, output_path: Path, timeout: int = 30) -> bool:
    """Download a file from URL to output path."""
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=timeout) as response:
            content = response.read()
            # Validate JSON
            json.loads(content)
            # Write to file
            output_path.write_bytes(content)
            return True
    except HTTPError as e:
        print(f"  HTTP Error {e.code}: {e.reason}")
        return False
    except URLError as e:
        print(f"  URL Error: {e.reason}")
        return False
    except json.JSONDecodeError:
        print("  Invalid JSON content")
        return False
    except Exception as e:
        print(f"  Error: {e}")
        return False


def main():
    """Download all Indian state/UT GeoJSON files."""
    print("=" * 60)
    print("Downloading Indian State/UT GeoJSON Boundaries")
    print("Source: github.com/udit-001/india-maps-data")
    print("=" * 60)
    print()

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    success_count = 0
    fail_count = 0
    skip_count = 0

    for remote_name, local_name in STATES_AND_UTS:
        output_path = OUTPUT_DIR / local_name
        state_name = local_name.replace(".geojson", "").replace("_", " ").title()

        # Check if already exists
        if output_path.exists():
            print(f"[SKIP] {state_name} (already exists)")
            skip_count += 1
            continue

        url = f"{BASE_URL}/{remote_name}"
        print(f"[DOWNLOAD] {state_name}...", end=" ", flush=True)

        if download_file(url, output_path):
            size_kb = output_path.stat().st_size / 1024
            print(f"OK ({size_kb:.1f} KB)")
            success_count += 1
        else:
            fail_count += 1

        # Small delay to be nice to the server
        time.sleep(0.2)

    print()
    print("=" * 60)
    print(f"Summary: {success_count} downloaded, {skip_count} skipped, {fail_count} failed")
    print(f"Total files in {OUTPUT_DIR}: {len(list(OUTPUT_DIR.glob('*.geojson')))}")
    print("=" * 60)

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
