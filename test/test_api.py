import unittest
from unittest.mock import MagicMock

from use_cases import is_valid_plate, get_plate, search_plate_fn, post_plate
from repositories.memory.plate import PlateRepository
from entities.plate import Plate


class TestApi(unittest.TestCase):
    def setUp(self):
        self.existing_plate_name = "O-LD1234"
        self.new_plate_name = "N-EW5678"
        self.close_search = "O-LD1235"
        self.far_search = "I-MX0581"
        self.existing_plate = Plate(self.existing_plate_name)
        self.new_plate = Plate(self.new_plate_name)
        self.plate_repo = PlateRepository()
        self.plate_repo.get_all = MagicMock(return_value=[self.existing_plate])
        self.plate_repo.save = MagicMock(return_value=(self.new_plate.serialize(), 200))

    def test_get_plate(self):
        serialized_plates = get_plate(plate_repo=self.plate_repo)
        self.assertEqual(len(serialized_plates), 67)
        self.assertEqual(serialized_plates.split(",")[0], '[{"plate": ' + f'"{self.existing_plate_name}"')

    def test_post_plate(self):
        saved, code = post_plate({"plate": self.new_plate_name}, plate_repository=self.plate_repo)
        self.assertEqual(code, 200)
        self.assertEqual(saved['plate'], self.new_plate.name)

    def test_get_search_plate_close(self):
        search = search_plate_fn({"key": self.close_search, "levenshtein": "1"}, self.plate_repo)
        self.assertEqual(len(search), 67)
        self.assertEqual(search.split(",")[0], '[{"plate": ' + f'"{self.existing_plate_name}"')

    def test_get_search_plate_far(self):
        search = search_plate_fn({"key": self.far_search, "levenshtein": "2"}, self.plate_repo)
        self.assertEqual(len(search), 2)  # "[]"

    def test_valid_plate(self):
        not_string = 2
        hypen_missing = "asdfg1234"
        double_hypen = "as-dfg-1234"
        long_pre_hypen = "asdf-g1234"
        long_letters_post_hypen = "as-dfg1234"
        too_many_numbers = "asd-fg123456"
        pre_hypen_missing = "-fg1234"
        post_hypen_letters_missing = "asd-1234"
        correct = "asd-fg1234"
        self.assertFalse(is_valid_plate(not_string))
        self.assertFalse(is_valid_plate(hypen_missing))
        self.assertFalse(is_valid_plate(double_hypen))
        self.assertFalse(is_valid_plate(long_pre_hypen))
        self.assertFalse(is_valid_plate(long_letters_post_hypen))
        self.assertFalse(is_valid_plate(too_many_numbers))
        self.assertFalse(is_valid_plate(pre_hypen_missing))
        self.assertFalse(is_valid_plate(post_hypen_letters_missing))
        self.assertTrue(is_valid_plate(correct))


if __name__ == '__main__':
    unittest.main()
