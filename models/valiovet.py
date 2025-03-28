from pydantic import BaseModel

class Valiovi(BaseModel):
    korkeus: int
    leveys: int
    turvalasi: bool
    valikarmi: bool
    salekaihtimet: bool