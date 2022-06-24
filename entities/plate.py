from typing import Dict
from datetime import datetime

from pytz import timezone
from Levenshtein import distance

from db import db

time_format = "%Y-%m-%dT%H:%M:%S%Z%z"


class Plate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(12), unique=True, nullable=False)
    timestamp = db.Column(db.TIMESTAMP(timezone=True), nullable=False)

    def __init__(self, name: str):
        self.name = name
        self.timestamp = datetime.now(timezone('UTC'))

    def serialize(self) -> Dict:
        return {
            "plate": self.name,
            "timestamp": self.timestamp.strftime(time_format)
        }

    def unhypen(self) -> str:
        return self.name.replace("-", "")

    def levenshtein_distance(self, other: str) -> int:
        return distance(self.unhypen(), other)
