from pydantic import BaseModel

from typing import List

from entities.sintese_itens import SinteseItens
from entities.anexo import Anexo

class NotaPedido(BaseModel):
    tipo: str
    org_compras: str
    grp_compradores: str
    empresa: str
    cod_fornecedor: str
    sintese_itens: List[SinteseItens]
    anexo: Anexo