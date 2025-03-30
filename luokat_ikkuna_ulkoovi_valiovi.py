from pydantic import BaseModel

class IkkunaRaaka(BaseModel):
    koko: str
    kpl: int
    turvalasi: bool
    välikarmi: bool
    sälekaihtimet: bool

class Ikkuna(BaseModel):
    leveys_mm: int
    korkeus_mm: int
    turvalasi: bool
    välikarmi: bool
    sälekaihtimet: bool

class UlkoOvi(BaseModel):

    malli: str
    paloluokitus_EI_15: bool
    lukko: str
    maara: int
    
    