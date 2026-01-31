from dataclasses import dataclass

from src.domain.enums.trainer_enums import Gender, Region


@dataclass
class Trainer:
    id: int | None
    name: str
    gender: Gender
    region: Region

    def __post_init__(self) -> None:
        if isinstance(self.gender, str):
            self.gender = Gender(self.gender)
        if isinstance(self.region, str):
            self.region = Region(self.region)
