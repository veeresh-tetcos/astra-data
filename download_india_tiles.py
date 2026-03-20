#!/usr/bin/env python3
"""
Download all ESA WorldCover tiles for India.

India geographic extent:
- Latitude: 6°N to 37°N
- Longitude: 66°E to 97°E

Usage:
    python utilities/download_india_tiles.py
"""

import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from worldcover import ensure_worldcover_tile, get_tile_name

WORLDCOVER_DIR = Path(__file__).parent.parent / "data" / "worldcover"


def main():
    """Download all India tiles."""
    WORLDCOVER_DIR.mkdir(parents=True, exist_ok=True)

    # India coverage: 6°N-37°N, 66°E-97°E
    tiles_to_download = []
    for lat in range(6, 39, 3):  # N06, N09, N12, N15, N18, N21, N24, N27, N30, N33, N36
        for lon in range(66, 99, 3):  # E066, E069, E072, E075, E078, E081, E084, E087, E090, E093, E096
            tiles_to_download.append((lat, lon))

    total = len(tiles_to_download)
    success = 0
    skipped = 0
    failed = []

    print(f"Downloading {total} tiles for India coverage...")
    print("Estimated size: 1.2-1.5 GB\n")

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
