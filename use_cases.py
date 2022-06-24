import re
import json
from typing import Dict, Tuple


from entities.plate import Plate
from repositories.memory.plate import PlateRepository


def search_plate_fn(args: Dict, plate_repo: PlateRepository):
    key = args.get("key")
    if not isinstance(key, str):
        return 422, "Missing key to search"
    # Unhypening... just in case
    key = key.replace("-", "")
    levenshtein = args.get("levenshtein")
    if not isinstance(levenshtein, str) or not levenshtein.isnumeric():
        return 422, "Invalid levenshtein, must be a number"
    levenshtein = int(levenshtein)
    all_plates = plate_repo.get_all()

    def is_close(k):
        return lambda x: x.levenshtein_distance(k) <= levenshtein

    return json.dumps([p.serialize() for p in filter(is_close(key), all_plates)])


def post_plate(plate_data: Dict, plate_repository: PlateRepository) -> Tuple[str, int]:
    plate_name = plate_data.get("plate", None)
    if plate_name is None:
        return "Malformed request, it must contain the key 'plate'", 400
    if not is_valid_plate(plate_name):
        return "Key 'plate' must be a valid german plate", 422
    return plate_repository.save(Plate(plate_name))


def get_plate(plate_repo: PlateRepository) -> str:
    serialized_plates = [p.serialize() for p in plate_repo.get_all()]
    return json.dumps(serialized_plates)


def is_valid_plate(plate_name: str) -> bool:
    if not isinstance(plate_name, str):
        return False
    by_hypen = plate_name.split('-')
    if len(by_hypen) != 2:
        return False
    if len(by_hypen[0]) == 0 or len(by_hypen[0]) > 3:
        return False
    split_post_hypen = re.split(r'(\d+|\s+)', by_hypen[1])
    if not isinstance(split_post_hypen, list) or len(split_post_hypen) != 3:
        return False
    if len(split_post_hypen[0]) not in [1, 2]:
        return False
    if len(split_post_hypen[1]) > 4 or split_post_hypen[1][0] == '0':
        return False
    return True
