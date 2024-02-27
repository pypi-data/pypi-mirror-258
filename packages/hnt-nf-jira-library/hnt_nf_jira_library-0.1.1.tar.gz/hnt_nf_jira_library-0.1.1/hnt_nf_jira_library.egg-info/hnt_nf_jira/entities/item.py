from pydantic import BaseModel

class Item(BaseModel):
    centro: str
    centro_custo: str
    cod_impost: str
    valor_bruto: float