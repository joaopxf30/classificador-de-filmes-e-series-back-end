from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine, event
import os

# Importando os elementos definidos no modelo
from model.base import MoviesAndSeriesBase
from model.model import Audiovisual, Rating


db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
    # Então cria o diretorio
    os.makedirs(db_path)

# Url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = "sqlite:///%sdb.sqlite3" % db_path

# Cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Habilita a restrição de integridade referencial no sqlite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# Cria o banco se ele não existir
if not database_exists(engine.url):
    create_database(engine.url)

# Cria as tabelas do banco, caso não existam
MoviesAndSeriesBase.metadata.create_all(engine)
