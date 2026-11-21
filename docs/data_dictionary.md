# Data dictionary

The processed panel contains one record for each neighbourhood-year from 2016 through 2024. Values were reshaped from the supplied wide table without changing the underlying measurements. Units are stated only where they were explicit in the source documentation; fields with unresolved units should be confirmed before publication.

| Field | Description | Legacy source field |
| --- | --- | --- |
| `neighbourhood_id` | Stable numeric neighbourhood identifier | `UID` |
| `city` | Municipality/city name | `WADMKK` |
| `district` | District (`kecamatan`) name | `WADMKC` |
| `neighbourhood` | Neighbourhood (`kelurahan`) name | `WADMKD` |
| `year` | Observation year | column suffix |
| `object_id` | Source GIS feature identifier | `OBJECTID_1` |
| `elevation` | Topographic elevation indicator | `Topo` |
| `distance_to_river` | Distance to the nearest river | `DistRv` |
| `building_age` | Building-age indicator | `BldgAge` |
| `building_area` | Building-area indicator | `BldgAr` |
| `drainage_capacity` | Drainage-system capacity indicator | `DrnSys` |
| `pump_capacity` | Pump location/capacity indicator in the legacy table | `PumpsLc` |
| `distance_to_coast` | Distance-to-coast indicator | `DTC` |
| `rainfall` | Annual rainfall indicator | `RainYY` |
| `built_up_rate` | Built/non-built development rate | `BldRateYY` |
| `population_density` | Population-density indicator | `PopDensYY` |
| `vegetation_cover` | Vegetation-cover indicator | `VegCovYY` |
| `night_light` | Night-time-light indicator | `NightLtYY` |
| `ndwi` | Normalised Difference Water Index / blue-area indicator | `BlueArYY` |
| `land_surface_temperature` | Land-surface-temperature indicator | `LSTempYY` |
| `ndbi` | Normalised Difference Built-up Index | `NDBIYY` |
| `flood_occurrence` | Flood occurrence/frequency indicator | `FloodYY` |
| `flood_depth` | Flood-depth/severity indicator | `FloDepthYY` |
| `young_population` | Population aged under 14 | `AgeY{YY}` |
| `older_population` | Population aged over 65 | `AgeOYY` |
| `female_population` | Female-population indicator | `FemaleYY` |
| `low_education_population` | Low-education population indicator | `LowEduYY` |
| `age_index` | Combined age-vulnerability indicator | `AgeYY` |
| `flood_vulnerability_index` | Composite Flood Vulnerability Index (FVI) | `FVIYY` |
| `hazard_index` | Composite flood-hazard indicator | `HazardYY` |
| `flood_risk_index` | Composite Flood Risk Index (FRI) | `FRIYY` |
| `poverty` | Poverty indicator | `PovertyYY` |
| `land_subsidence_index` | Annual land-subsidence indicator | `LandSubNYY` |

`YY` denotes the two-digit year. The forecast table contains `neighbourhood`, `year`, and `predicted_flood_risk_index` for 2025–2045.

The shapefiles use EPSG:32748 (WGS 84 / UTM zone 48S), as recorded in their `.prj` files.
