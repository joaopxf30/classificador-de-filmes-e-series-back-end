import pdb

import logging

from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session

from omdb_api import OMDbApi

from schema import (
    POSTAudiovisual, 
    Audiovisual,
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


# @app.get(
#     "/movies", 
#     tags=[AUDIOVISUAL_TAG],
#     responses={
#         "200": schema.Movie, 
#         "404": ErrorSchema,
#     }
# )
# def get_movies():
#     """Get all previous movies from the collection
#     """
#     logger.debug(f"Collecting movies")
#     # Criando conexão com a base
#     session = Session()
#     # Fazendo a busca por todos esportistas
#     movies = session.query(model.Movie).all()
#     logger.debug(f"Obtendo esportistas")
#     if not esportistas:
#         # Caso em que não há esportistas registrados
#         return {"esportistas": []}, 200
#     else:
#         logger.debug(f"%d esportistas já registrados" % len(esportistas))
#         # Retorna a serialização da visualização de esportistas
#         return apresenta_esportistas(esportistas), 200


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

    LOG.debug(print(response.json()))

    pdb.set_trace()

    audiovisual = Audiovisual.model_validate(obj=response.json())

    LOG.debug(audiovisual)

    # logger.debug(f"Tentativa de adicionar o/a esportista {esportista.nome_completo}")

    # try:
    #     session = Session()
    #     session.add(movie)
    #     session.commit()
    #     logger.debug(f"Adicionado o/a esportista: {esportista.nome_completo}")
    #     # Retorna a serialização da visualização de um esportista
    #     return apresenta_esportista(esportista), 200

    # except IntegrityError:
    #     # O nome é uma chave primária, logo não pode haver mais tuplas com essa característica
    #     error_msg = f"O/A esportista {esportista.nome_completo} já existe na base"
    #     logger.warning(f"Erro ao adicionar o/a esportista {esportista.nome_completo}. {error_msg}")
    #     return {"message": error_msg}, 409

    # except Exception:
    #     # Caso de um erro fora do previsto
    #     error_msg = f"Não foi possível cadastrar o/a esportista {esportista.nome_completo}"
    #     logger.warning(f"Erro ao adicionar o/a esportista {esportista.nome_completo}. {error_msg}")
    #     return {"message": error_msg}, 400
    

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