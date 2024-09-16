# PY-CALENDAR
## Descrição
Esse repositório contém a resolução para o desafio da vaga de Desenvolvedor Python da WLC Soluções.

O desafio foi definido para a criação de tarefas com o uso do google calendar, porém na minha pesquisa acabei não encontrando como fazer Tasks do google com a API do google calendar disponibilizada no PDF, portanto eu usei data e horas padrão para "replicar" o funcionamento das tarefas na criação de eventos no calendário.

## Tecnologias usadas
1. Python
2. Django & Django Rest Framework
3. Google Calendar API
4. Google OAuth
   
## Como replicar e rodar o app
1. Clone o repositório
2. Crie um ambiente virtual python com `py -m venv venv`
3. Ative o ambiente virtual (Esse comando pode mudar a depender do seu sistema operacional):
```.\venv\Scripts\activate```
4. Instale as dependencias do projeto `pip install -r requirements.txt`
5. Crie um arquivo .env em `./challange_py_google_calendar` com as variáveis:
```
SECRET_KEY=
DEBUG=
DB_NAME=
DB_PASSWORD=
DB_USER=
DB_HOST=
DB_PORT=
DEFAULT_HOUR_FORMAT=Formato de hora padrão para os eventos, quando não for definido uma hora na criação da tarefa. (%H:%M:%S ou outro formato)
DEFAULT_HOUR=Horário padrão para a hora de inicio de um evento, usado quando não for definido uma hora na criação da tarefa (deve seguir o formato definido anteriormente)
DEFAULT_CALENDAR_ID=ID do calendário que será usado na aplicação, "primary" é o padrão para a conta do google.
```
> [!NOTE]
> Banco de dados utilizado foi MySQL

6. Rode as migrations com o comando `python manage.py migrate`
7. Adicione o arquivo credentials.json do Google OAuth no diretório `./calendar_challange` (Um que pode ser usado foi enviado por e-mail para não deixar público a credencial, ou você pode utilizar um de sua preferência).
8. Rode o servidor Django `python manage.py runserver`

## Endpoints e funcionalidades
1. POST
ENDPOINT: `/api/evento/`

Parametros:

```
titulo: String, obrigatório
descricao: String, opcional
data: String, formato YYYY-MM-DD, opcional
horario: String, formato HH:MM, opcional
```
> [!NOTE]
> Por padrão, a API do google para o calendário requer data de início e data de fim do evento, portanto se não for informado data de início o sistema irá usar a data atual, e o horário será definido pela variável de ambiente DEFAULT_HOUR.
> A data de fim sempre será a mesma de início.

2. GET (Listagem)
   
ENDPOINT: `/api/evento/`

Irá listar com paginação os eventos cadastrados.

Os filtros são definidos como queryparams. Filtros:

```
titulo: String
data_inicio: String, formato YYYY-MM-DD ou DD/MM/YYYY, início do RANGE de data a se filtrar
data_fim: String, formato YYYY-MM-DD ou DD/MM/YYYY, fim do RANGE de data a se filtrar
idevento: String, idevento no banco de dados (não confundir com o ID do evento da API do Google Calendar)
```

3. GET (Único)
   
ENDPOINT: `/api/evento/idevento/`

Irá retornar o evento com o ID (do banco de dados) informado, não confundir com o ID do evento da API do Google Calendar.

4. DELETE
   
ENDPOINT: `/api/evento/idevento/`

Irá deletar o evento com o ID (do banco de dados) informado, não confundir com o ID do evento da API do Google Calendar. Caso ocorra algum problema na deleção do evento do calendário, irá retornar o erro dado pela API do Google Calendar, mas irá deletar no banco de dados.

5. PATCH e PUT

ENDPOINT: `/api/evento/idevento/`

Os mesmos parâmetros informados no POST podem ser usados.
