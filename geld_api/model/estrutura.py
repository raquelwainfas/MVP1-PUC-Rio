from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from typing import Union

from model.base import Base

class Estrutura(Base):
    __tablename__ = 'estrutura'

    id = Column("pk_estrutura", Integer, primary_key=True)
    referencia= Column(String(30))
    nome = Column(String(140))
    valor = Column(Float)
    data_pgto = Column(DateTime, default=(datetime.now()).date())

    def __init__(self, referencia:str, nome:str, valor:float,
                 data_pgto:Union[DateTime, None] = None):
        
        self.referencia = referencia
        self.nome = nome
        self.valor = valor
        
        if data_pgto:
            self.data_pgto = data_pgto