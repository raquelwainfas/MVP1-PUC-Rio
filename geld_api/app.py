from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Estrutura
from schemas import *
from flask_cors import CORS

info = Info(title="GELD API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
gerenciador_tag = Tag(name="Gerenciador Financeiro", description="Adição, visualização, alteração e remoção de itens do Gerenciador Financeiro à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/add_item', tags=[gerenciador_tag],
          responses={"200": AddItemViewSchema, "409": ErrorSchema, "400": ErrorSchema, "500": ErrorSchema})
def add_item(form: AddItemSchema):
    """Adiciona um novo item à base de dados
    Retorna uma representação dos itens.
    """

    item = Estrutura(
        referencia=form.referencia,
        nome=(form.nome).capitalize(),
        data_pgto=form.data,  ##Funcionamento Front
        # data_pgto=transforma_data(form.data),  ##Funcionamento Swagger
        valor=form.valor)
    try:
        # criando conexão com a base
        session = Session()
        # adicionando item
        session.add(item)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        return apresenta_item(item), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Esse item ja foi cadastrado"
        return {"mensagem": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item"
        return {"mensagem": error_msg}, 400
    
@app.get('/lista_tudo', tags=[gerenciador_tag],
         responses={"200": BuscaViewSchema, "404": ErrorSchema})
def get_tudo():
    """Retorna todos os itens do banco de dados
    """
    session = Session()

    # refs = session.query(Estrutura).filter(Estrutura.referencia == referencia).all()
    itens = session.query(Estrutura).filter(Estrutura.data_pgto).all()

    if not itens:
        # se o item não foi encontrado
        error_msg = "Nenhum dado encontrado na base"
        return {"mensagem": error_msg}, 404
    else:
        # retorna a representação de item
        # return lista_itens_mes(referencia, ano, mes_nome, itens), 200
        return lista_tudo(itens), 200
    
@app.get('/lista_itens', tags=[gerenciador_tag],
         responses={"200": BuscaViewSchema, "404": ErrorSchema})
def get_item(query: BuscaSchemaData):
    """Faz a busca por um item a partir do mes e ano de inserção
    Retorna uma representação de todos os itens de acordo com ano e mês inseridos.
    """
    # referencia = query.referencia
    ano = query.ano
    mes = query.mes
    # criando conexão com a base
    session = Session()

    # refs = session.query(Estrutura).filter(Estrutura.referencia == referencia).all()
    itens = session.query(Estrutura).filter(Estrutura.data_pgto).all()

    if not itens:
        # se o item não foi encontrado
        error_msg = "Nenhum dado encontrado na base"
        return {"mensagem": error_msg}, 404
    else:
        # retorna a representação de item
        # return lista_itens_mes(referencia, ano, mes_nome, itens), 200
        return lista_itens(itens, ano, mes), 200
    
@app.delete('/del_item', tags=[gerenciador_tag],
            responses={"200": MensagemSchema, "404": ErrorSchema})
def del_item(query: IDBuscaSchema):
    """Deleta um item a partir do id informado
    Retorna uma mensagem de confirmação da remoção.
    """

    id = query.id
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Estrutura).filter(Estrutura.id == id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mensagem": "Item removido", "id": id}
    else:
        # se o item não foi encontrado
        error_msg = "Item não encontrado na base"
        return {"mensagem": error_msg}, 404
    
@app.put('/atualiza_item/<id>', tags=[gerenciador_tag],
            responses={"200": MensagemSchema, "404": ErrorSchema})
def atualiza_item(query: IDAtualizaSchema):
    """Atualiza os dados de um item a partir do id informado
    Retorna uma mensagem de confirmação da atualização.
    """
    id_input = query.id
    ref = query.referencia
    nome = query.nome
    valor = query.valor
    data = query.data

    data_transformada = transforma_data(data)

    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    id_banco = session.query(Estrutura).filter_by(id= id_input).update(dict(referencia=ref, nome=nome, valor=valor, 
                                                                            data_pgto=data_transformada))

    session.commit()

    if id_banco:
        # retorna a representação da mensagem de confirmação
        return {"mensagem": "Item atualizado", "id": id_input}
    else:
        # se o item não foi encontrado
        error_msg = "Item não encontrado na base"
        return {"mensagem": error_msg}, 404