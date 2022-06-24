# Peter Park code challenge

This repository contains the Python code that implements an API requested by Peter Park. The Framework used is Flask/SQLAlquemy

## Instalation

TBA

## Run
TBA

## Endpoints

### POST /plate
#### body
##### plate={str}
#### Returns
* $200$: List with the plate and timestamp of all the stored licence plates.
* $400$: Invalid body.
* $422$: Invalid plate.
### GET /plate
#### Returns
* $200$: List with the plate and timestamp of all the stored licence plates.
### GET /search-plate
#### Query params
* $key={str}$: 
* $levenshtein={int}$:

## Considerations
* As the database format is not specified, a database in memory is used.
* The sanity checks the plate consistency of `key` during GET /search-plate are being skipped intentionaly.
* The Levenshtein distance is being processed by the interperter using `python-Levenshtein`. In a real case scenario and if an optimization is needed, [fuzzystrmatch](https://www.postgresql.org/docs/current/fuzzystrmatch.html) would be used.
