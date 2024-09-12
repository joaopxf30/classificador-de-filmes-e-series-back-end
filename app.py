import logging

from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from model import Session
import model.audiovisual as model

from omdb_api import OMDbApi

from sqlalchemy.exc import IntegrityError

from schema import (
    POSTAudiovisual, 
    Audiovisual,
    return_audiovisual_view
)

from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

LOG = logging.getLogger()


AUDIOVISUAL_TAG = Tag(
    name="Esportista", 
    description="Adição, visualização e remoção de esportista da base"
)
# TREINO_TAG = Tag(
#     name="Treino",
#     description="Adição, visulização e remoção de treino da base"
# )
HOME_TAG = Tag(
    name="Documentação", 
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc"
)


@app.get(
    "/", 
    tags=[HOME_TAG]
)
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect("/openapi")


@app.get(
    "/audiovisuals", 
    tags=[AUDIOVISUAL_TAG],
    responses={
        # "200": schema.Audiovisual, 
        # "404": ErrorSchema,
    }
)
def get_audiovisuals():
    """Get all previous movies or series from the collection

    """
    LOG.debug(f"Collecting movies and series")
    
    session = Session()

    if db_data := session.query(model.Audiovisual).all():
        LOG.debug("There are %d movies and series on the collection" % len(db_data))
        audiovisuals = list(
            map(
                lambda v: Audiovisual.model_validate(v),
                db_data
            )
        )
        return {
            "audiovisuals": [
                return_audiovisual_view(v) for v in audiovisuals
            ]
        }, 200
    
    return {"audiovisuals": []}, 200
    

@app.post(
    rule="/add_audiovisual", 
    tags=[AUDIOVISUAL_TAG],
    responses={
        "200": Audiovisual,
        # "400": ErrorSchema,
        # "409": ErrorSchema,
    }
)
def add_audiovisual(form: POSTAudiovisual):
    """Add a new movie or series to the collection

    """
    response = OMDbApi().get_audiovisual(**form.model_dump())
    audiovisual = Audiovisual.model_validate(response.json())
    serial = audiovisual.model_dump(exclude={"ratings"})
    db_data = model.Audiovisual(**serial)

    LOG.debug(f"Trying to add the movie or series {audiovisual.title} to the collection")

    try:
        session = Session()
        session.add(db_data)        
        session.commit()
        
        # return apresenta_esportista(esportista), 200

    except IntegrityError:
        # Unique constraint failed
        error_msg = f"The movie or series {audiovisual.title} has been already added"
        LOG.warning(error_msg)

        return {"message": error_msg}, 409

    except Exception:
        # Dealing with general exceptions
        error_msg = f"It was not possible to add the movie or series {audiovisual.title} to the collection"
        LOG.warning(error_msg)

        return {"message": error_msg}, 400
    

# @app.delete(
#     rule="/esportista", 
#     tags=[FILME_TAG],
#     responses={
#         "200": EsportistaDeletadoSchema, 
#         "404": ErrorSchema
#     }
# )
# def deleta_esportista(query: EsportistaBuscaSchema):
#     """Deleta um esportista a partir de seu nome.

#     O esportista é deletado do banco de dados. \
#     Consequentemente, os treinos associados a este \
#     esportista também são deletados. No final uma \
#     mensagem de confirmação da remoção é retornada.
#     """
#     esportista_nome = unquote(query.nome)
#     logger.debug(f"Deletando dados sobre esportista {esportista_nome}")
#     # Criando conexão com a base
#     session = Session()
#     # Fazendo a remoção do esportista e treinos associados
#     delecao = session.query(Esportista).filter(
#         Esportista.nome_completo == esportista_nome
#     ).delete()
#     # Efetivando o comando de remoção de esportista e treinos associados na tabela
#     session.commit()

#     if delecao:
#         logger.debug(f"Esportista {esportista_nome} deletado/a")
#         # Retorna a representação da mensagem de confirmação do delete
#         return {"message": "Esportista deletado/a", "nome": esportista_nome}, 200
#     else:
#         # Caso o esportista não for encontrado no banco de dados
#         error_msg = "Esportista não foi registrado!"
#         logger.warning(f"Erro ao deletar esportista {esportista_nome}. {error_msg}")
#         return {"message": error_msg}, 404
    

# @app.get(
#     "/treinos", 
#     tags=[TREINO_TAG],
#     responses={
#         "200": ListagemTreinosSchema, 
#         "404": ErrorSchema,
#     }
# )
# def obtem_lista_treinos():
#     """Faz a busca por todos os treinos registrados no banco de dados.
    
#     Retorna uma representação desta listagem de treinos.
#     """
#     logger.debug("Coletando treinos")
#     # Criando conexão com a base
#     session = Session()
#     # Fazendo a busca
#     treinos = session.query(Treino).all()
#     logger.debug("Obtendo treinos")
#     if not treinos:
#         # Caso em que não há treinos registrados
#         return {"treinos": []}, 200
#     else:
#         logger.debug(f"%d treinos já registrados" % len(treinos))
#         # Retorna a serialização da visualização de treinos
#         return apresenta_treinos(treinos), 200


# @app.post(
#     rule="/adiciona_treino",
#     tags=[TREINO_TAG],
#     responses={
#         "200": TreinoViewSchema,
#         "400": ErrorSchema,
#         "409": ErrorSchema,
#     }
# )
# def cria_um_treino(form: TreinoSchema):
#     """Adiciona um treino para um esportista já cadastrado.
    
#     Retorna uma representação do treino.
#     """
#     treino = Treino(**form.model_dump(by_alias=True))
#     logger.debug(f"Tentativa de adicionar novo treino")

#     try:
#         # Criando conexão com a base
#         session = Session()
#         # Adiciona treino na respectiva tabela no banco de dados
#         session.add(treino)
#         # Efetivando o comando de adição de novo treino na tabela
#         session.commit()
#         logger.debug(f"Adicionado treino do esportista: {treino.esportista}")
#         # Retorna a serialização da visualização de treino
#         return apresenta_treino(treino), 200
    
#     except IntegrityError as e:
#         propriedades_do_erro = e.orig.__dict__
#         nome_do_erro = propriedades_do_erro["sqlite_errorname"]
#         if nome_do_erro == "SQLITE_CONSTRAINT_PRIMARYKEY":
#             # A tripla nome, data e esporte é uma chave primária, logo não pode haver 
#             # mais tuplas com essa característica
#             error_msg = f"Já existe um treino para {form.nome_esportista} de {form.esporte} registrado em {form.data_treino}"
#         else:
#             # Cenário em que o esportista não foi registrado previamente, não respeitando
#             # a integridade referencial
#             error_msg = f"O/A esportista {form.nome_esportista} não foi registrado previamente."
#         logger.warning(f"Erro ao adicionar o treino. {error_msg}")
#         return {"message": error_msg}, 409

#     except Exception:
#         # Casos de erro não esperados
#         error_msg = f"Não foi possível cadastrar o treino de {form.nome_esportista}."
#         logger.warning(f"{error_msg}")
#         return {"message": error_msg}, 400


# @app.delete(
#     rule="/treino", 
#     tags=[TREINO_TAG],
#     responses={
#         "200": EsportistaDeletadoSchema, 
#         "404": ErrorSchema
#     }
# )
# def deleta_treino(query: TreinoBuscaSchema):
#     """Deleta um treino a partir da composição \
#     dada pelo nome do esportista, a data do \
#     treino e a modalidade praticada. 
    
    
#     Retorna uma mensagem de confirmação da remoção.
#     """
#     nome_esportista = unquote(query.nome)
#     data_treino = unquote(query.data)
#     esporte = unquote(query.esporte)
#     logger.debug(
#         f"Deletando o treino de {nome_esportista} de {esporte} do dia {data_treino}"
#     )
#     # Criando conexão com a base
#     session = Session()
#     # Fazendo a remoção do treino
#     delecao = session.query(Treino).filter(
#         Treino.nome_esportista == nome_esportista,
#         Treino.data_treino == data_treino,
#         Treino.esporte == esporte
#     ).delete()
#     # Efetivando o comando de remoção de treino
#     session.commit()

#     if delecao:
#         # Retorna a representação da mensagem de confirmação do delete
#         logger.debug(f"Treino deletado/a")
#         return {"message": "Treino deletado"}, 200
#     else:
#         # Cenário em que um determinado treino foi registrado
#         error_msg = "Treino não foi registrado!"
#         logger.warning(f"Erro ao deletar treino")
#         return {"message": error_msg}, 404