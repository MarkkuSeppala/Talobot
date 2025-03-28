from dataclasses import dataclass, asdict

@dataclass
class IkkunaRaaka:
    koko: str
    kpl: int
    turvalasi: bool
    välikarmi: bool
    sälekaihtimet: bool

@dataclass
class Ikkuna:
    koko: str
    mm_koko: str
    turvalasi: bool
    välikarmi: bool
    sälekaihtimet: bool

@dataclass
class UlkoOvi:
    """
    Edustaa ulko-ovea ja sen ominaisuuksia.  Käyttää dataclass-koristetta.
    """
    malli: str
    paloluokitus_EI_15: bool
    lukko: str
    maara: int
    
    