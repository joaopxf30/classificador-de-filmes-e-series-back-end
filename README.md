# API do projeto de controlador de treinos

Este pequeno projeto, intitulado controlador de treinos, compõe o MVP desenvolvido para a sprint de **Desenvolvimento Full Stack Básico** do curso de pós-graduação em Desenvolvimento Full Stack. O controlador de treinos é uma aplicação web responsável por cadastrar esportistas e registrar treinos vinculados a cada esportista. O presente documento ressalta aspectos do desenvolvimento voltados ao back-end.


---
## Ambientes virtuais

É fortemente recomendado a utilização de ambientes virtuais. Para tal, execute no terminal a partir de um path desejado o seguinte comando de acordo com o sistema operacional:

**WINDOWS**:
```
python -m venv env
```

**OS/LINUX**:
```
python3 -m venv env
```

Para ativação do ambiente virutal, execute o seguinte comando de acordo com a platafoma:

**WINDOWS**:
```
<path>\env\Scripts\Activate.ps1
```

**POSIX**:
```
source <path>/env/bin/activate
```

O ambiente virtual será criado.

## Instalando dependências

Todas as dependências do projeto se encontram no arquivo `requirements.txt`. A obtenção é feita a partir da execução do seguinte comando na raiz do projeto:

```
pip install -r requirements.txt
```

As dependências são instaladas.

## APIs do projeto

Para utilizar as APIs direcionadas à funcionalidade do esportista ou do treino, assim como acessar a documentação dessas, é necessário executar previamente o seguinte comando na raiz do projeto:

```
flask run --host 0.0.0.0 --port 5001
```

### Documentação das APIs

A documentação das APIs se encontra disponibilizada no Swagger através do seguinte caminho: http://127.0.0.1:5001/openapi/swagger.

## Aspectos gerais

### Linguagem de programação

A linguagem utilizada no back-end é Python na versão 3.11.2.

### Banco de dados

O SGBD adotado é o SQLite e a interação entre o servidor de dados e o banco de dados é feita por ORM através do SQLAlchemy.
