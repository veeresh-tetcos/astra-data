#!/usr/bin/env python3
"""
Download all ESA WorldCover tiles for Japan.

Japan geographic extent (approximate):
- Latitude: 24°N to 48°N
- Longitude: 122°E to 156°E

Usage:
    python utilities/download_japan_tiles.py
"""

import sys
from pathlib import Path

# Add astra-ui-app and astra-shared to path for imports
base = Path(__file__).parent.parent
sys.path.insert(0, str(base / "astra-ui-app"))
sys.path.insert(0, str(base / "astra-shared"))

from astra_shared.worldcover import ensure_worldcover_tile, get_tile_name

WORLDCOVER_DIR = Path(__file__).parent.parent / "astra-data" / "data" / "worldcover"


def main():
    """Download all Japan tiles."""
    WORLDCOVER_DIR.mkdir(parents=True, exist_ok=True)

    # Japan coverage (approx): 24°N-48°N, 122°E-156°E
    tiles_to_download = []
    for lat in range(24, 49, 3):
        for lon in range(122, 157, 3):
            tiles_to_download.append((lat, lon))

    total = len(tiles_to_download)
    success = 0
    skipped = 0
    failed = []

    print(f"Downloading {total} tiles for Japan coverage...")
    print("Estimated size: ~0.5-2.0 GB depending on coverage\n")

    for i, (lat, lon) in enumerate(tiles_to_download, 1):
        tile_name = get_tile_name(lat, lon)
        tile_path = WORLDCOVER_DIR / tile_name

        # Also check for old directory format: tile_name_Map/tile_name_Map.tif
        dir_name = tile_name.replace(".tif", "")
        tile_path_in_dir = WORLDCOVER_DIR / dir_name / tile_name

        # Check both flat file and directory formats
        if (tile_path.exists() and tile_path.stat().st_size > 0) or \
           (tile_path_in_dir.exists() and tile_path_in_dir.stat().st_size > 0):
            print(f"[{i}/{total}] {tile_name} - already exists, skipping")
            success += 1
            skipped += 1
            continue

        print(f"[{i}/{total}] Downloading {tile_name}...")
        try:
            ensure_worldcover_tile(lat, lon, WORLDCOVER_DIR)
            success += 1
        except RuntimeError as e:
            if "404" in str(e):
                print("  -> No data for this tile (ocean/no coverage)")
                skipped += 1
            else:
                print(f"  -> Failed: {e}")
                failed.append(tile_name)

    print(f"\n{'='*50}")
    print("Download complete!")
    print(f"  Success: {success}/{total} tiles")
    print(f"  Skipped (already exist or no data): {skipped}")
    if failed:
        print(f"  Failed: {len(failed)} tiles")
        print(f"  Failed tiles: {', '.join(failed)}")


if __name__ == "__main__":
    main()
