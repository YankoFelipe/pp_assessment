from typing import List, Tuple, Union, Dict

from flask import g

from entities.plate import Plate


class PlateRepository:
    def get_all(self) -> List[Plate]:
        return g.session.query(Plate).all()

    def save(self, plate: Plate) -> Tuple[Union[str, Dict], int]:
        if g.session.query(Plate).filter(Plate.name == plate.name).first():
            return "Plate already exists", 422
        g.session.add(plate)
        g.session.commit()
        return plate.serialize(), 200
