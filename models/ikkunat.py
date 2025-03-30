from pydantic import BaseModel

class Ikkuna(BaseModel):
    korkeus: int
    leveys: int
    turvalasi: bool
    valikarmi: bool
    salekaihtimet: bool
    karmi: bool
