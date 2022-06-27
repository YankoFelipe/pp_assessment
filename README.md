# Peter Park code challenge

This repository contains the Python code that implements an API requested by Peter Park. The Framework used is Flask/SQLAlquemy.

## Installation
Create a `.env` file with the desired port, e.g.
```
FLASK_RUN_PORT=<PORT_TO_USE>
```
Build the image
```
docker build --tag python-docker .
```
## Run tests
```
python -m unittest discover test
```
## Run
Run the container
```
docker run -p <PORT_TO_USE>:<PORT_TO_USE> -v $(pwd)/test.db:/tmp/test.db --env-file ~/PATH/TO/YOUR/.env <IMAGE_ID>
```
## Endpoints

### POST /plate
#### body
##### plate={str}
#### Returns
* *200*: List with the plate and timestamp of all the stored licence plates.
* *400*: Invalid body.
* *422*: Invalid plate.
### GET /plate
#### Returns
* *200*: List with the plate and timestamp of all the stored licence plates.
### GET /search-plate
#### Query params
* *key={str}*: String to search similar plates.
* *levenshtein={int}*: Maximal [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) to consider similar plates.

## Considerations
* As the database format is not specified, a database in disk is used in `./test.db`.
* The sanity checks the plate consistency of `key` during GET /search-plate are being skipped intentionaly.
* The Levenshtein distance is being processed by the interpreter using `python-Levenshtein`. In a real case scenario and if an optimization is needed, [fuzzystrmatch](https://www.postgresql.org/docs/current/fuzzystrmatch.html) would be used.
