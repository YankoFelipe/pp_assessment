from typing import List, Tuple

from flask import g

from db import db, get_session

from entities.plate import Plate

class PlateRepository:
    def get_all(self) -> List[Plate]:
        #session = get_session()
        #print('session: ', session)
        return g.session.query(Plate).all()

    def save(self, plate: Plate) -> Tuple[int, str]:
        g.session.add(plate)
        g.session.commit()
        return plate.serialize()
