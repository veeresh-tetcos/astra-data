# astra-data

Public dataset repository for NetSim Astra — satellite planning & RF coverage studio.

Contains only legally redistributable datasets. All content is public domain or open-licensed.

---

## Contents

### `data/boundaries/`

Administrative boundary GeoJSON files used for coverage region selection in the Astra UI.

| File / Directory | Region | Source | License |
|-----------------|--------|--------|---------|
| `india.geojson` | India (national outline) | [Datameet](https://github.com/datameet/maps) | ODBL / Public Domain |
| `india/` | 28 Indian states (individual files) | [Datameet](https://github.com/datameet/maps) | ODBL / Public Domain |
| `japan.geojson` | Japan (national outline) | [Natural Earth](https://www.naturalearthdata.com/) | Public Domain |
| `usa.geojson` | USA (national outline) | [Natural Earth](https://www.naturalearthdata.com/) | Public Domain |
| `usa/` | 50 US states (individual files) | [Natural Earth](https://www.naturalearthdata.com/) | Public Domain |

### Download Scripts

| Script | Purpose |
|--------|---------|
| `download_india_tiles.py` | Download ESA WorldCover raster tiles covering India |
| `download_india_states.py` | Download/refresh Indian state boundary files |

---

## What is NOT in this repo

### CesiumJS

The Cesium 3D globe library (340 MB) is **not** stored here. It is a third-party
library and should be obtained via:

- **CDN** (recommended for production): `https://cesium.com/downloads/cesiumjs/`
- **npm**: `npm install cesium`
- **Manual download**: [cesium.com/downloads](https://cesium.com/downloads/)

Place the `Build/Cesium/` directory at `Cesium/Build/Cesium/` relative to
`satellite_planner.py`, or update `settings.py` → `CESIUM_BUILD_PATH`.

### WorldCover Raster Tiles

ESA WorldCover clutter tiles (~GB scale) are downloaded on demand using
`download_india_tiles.py`. They are not stored in git.

---

## Usage

```bash
# Clone this repo into your astra-ui-app working directory
git clone https://github.com/NetsimAstra/astra-data data-repo

# Or copy boundary files directly
cp -r data-repo/data/boundaries <astra-ui-app>/data/boundaries
```
