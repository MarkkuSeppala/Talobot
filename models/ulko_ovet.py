from pydantic import BaseModel

class Ulko_ovi_tyypit(BaseModel):
    tyyppi: str
    malli: str
    lukko: str
    maara: int