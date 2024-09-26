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

__
## Run app with Docker

Before proceeding, it is important to have Docker installed.

### Building the image
Open the terminal in the root .movies-and-series-catalogue-back-end. The Dockerfile and requirements.txt are there.
Execute the following command:

```
docker build . -t movies-and-series-catalogue-back-end
```

If everything succeds, an image named movies-and-series-catalogue-back-end will be created. To check it, run the following in the same terminal:

```
docker images
````

A similar response should be seen in a good scenario:
```
REPOSITORY                             TAG       IMAGE ID       CREATED          SIZE
movies-and-series-catalogue-back-end   latest    7bf0cba0ae33   31 minutes ago   1.19GB
```

### Run a container from the image
Now, execute the following to create a container from the image

```
docker run --name msc-back-end -dp 5001:5001 movies-and-series-catalogue-back-end
```

It creates a container named msc-back-end, which binds the port 5001 of the container to the port 5001 of the host.

Whenever it is necessary to stop the container, do the following command:

```
docker stop msc-back-end
```

Now, there is no need to create again another container. To run the same one, just do:

```
docker start msc-back-end
```



