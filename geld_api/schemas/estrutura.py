from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Literal
from model import *

class AddItemSchema(BaseModel):
    """ Define como um novo valor do gerenciador a ser inserido deve ser representado
    """
    referencia: Literal["Capital_giro", "Cartao_credito", "Despesas_fixas", "Despesas_extras"]
    nome: str
    valor: float
    data: Optional[str] = datetime.strftime((datetime.now().date()),'%d/%m/%Y')

class AddItemViewSchema(BaseModel):
    """ Define como um item será retornado.
    """
    referencia: str = "Capital_giro"
    nome: str = "Salario"
    valor: float = 3500.42
    data: str = "14/11/2023"

class BuscaSchemaData(BaseModel):
    # referencia: Literal["Capital_giro", "Cartao_credito", "Despesas_fixas", "Despesas_extras"]
    ano: Optional[int] = 2023
    mes: Optional[int] = 11

class BuscaViewSchema(BaseModel):
    """ Define como um item será retornado.
    """
    ano: dict = "2023"
    mes: dict = "11"
    id: int = 1
    referencia: dict = "Capital_giro"
    nome: str = "Salario"
    valor: float = 3500.42
    data: str = "14/11/2023"

class IDBuscaSchema(BaseModel):
    id: int

class MensagemSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção/atualização.
    """
    mensagem: str
    nome: str

class IDAtualizaSchema(BaseModel):
    id: int
    referencia: Literal["Capital_giro", "Cartao_credito", "Despesas_fixas", "Despesas_extras"]
    nome: str
    valor: float
    data: str

def transforma_data(data):
    try:
        data_transformada = datetime.strptime(data, '%d/%m/%Y')
    except:
        try:
            data_transformada = datetime.strptime(data, '%Y-%m-%d')
        except:
            data_transformada = datetime.strftime(data, '%d/%m/%Y')
    return data_transformada

def transforma_valor(valor):
    valor_transformado = f'R${format(valor*1, ".2f")}'
    return valor_transformado

def apresenta_item(item: Estrutura):
    """ Retorna uma representação do item seguindo o schema definido em
        CapitalViewSchema.
    """
    return {
        "id": item.id,
        "referencia": item.referencia,
        "nome": item.nome,
        "data": item.data_pgto,
        "valor": transforma_valor(item.valor)
    }

""" def lista_itens_data(itens: List[Estrutura], ano=((datetime.now()).year), mes=((datetime.now()).month)):

    referencias = {item.referencia:[] for item in itens }
    for item in itens:
        mesItem = (item.data_pgto).month
        anoItem = (item.data_pgto).year
        mes_nome = (calendar.month_name[mes])
        
        if mes == mesItem and ano == anoItem:
            referencias[item.referencia].append({"id": item.id, item.nome: item.valor, "data":transforma_data(item.data_pgto)})
    return {anoItem: {mes_nome : referencias}} """


def lista_itens(itens: List[Estrutura], ano=((datetime.now()).year), mes=((datetime.now()).month)):

    resultado = []
    for item in itens:
        mesItem = (item.data_pgto).month
        anoItem = (item.data_pgto).year
        
        if mes == mesItem and ano == anoItem:
            resultado.append({"referencia": item.referencia, 
                              "id": item.id, 
                              "nome": item.nome,
                              "valor": item.valor, 
                              "data":transforma_data(item.data_pgto)})
    return resultado

def lista_tudo(itens: List[Estrutura]):
    resultado = []
    for item in itens:
        resultado.append({"referencia": item.referencia, 
                              "id": item.id, 
                              "nome": item.nome,
                              "valor": item.valor, 
                              "data":transforma_data(item.data_pgto)})
    return resultado