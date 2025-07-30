# API de Consulta de Clima (Weather API)

API RESTful construída com Django e Django REST Framework para consultar o clima atual de uma cidade, utilizando a OpenWeatherMap API. O projeto inclui cache, histórico de buscas e está totalmente containerizado com Docker.

## Funcionalidades Principais

-   ✅ Endpoint para buscar o clima atual por cidade.
-   ✅ Cache de 10 minutos para as respostas, utilizando Redis.
-   ✅ Histórico das últimas 10 consultas salvas em um banco de dados PostgreSQL.
-   ✅ Rate Limiting para evitar abuso da API.
-   ✅ Logs estruturados em JSON para ambiente de produção.
-   ✅ Tarefas assíncronas com Celery para salvar o histórico sem impactar a latência.
-   ✅ Documentação interativa da API com Swagger/OpenAPI.

## Tecnologias Utilizadas

-   **Backend:** Python, Django, Django REST Framework
-   **Banco de Dados:** PostgreSQL
-   **Cache & Message Broker:** Redis
-   **Tarefas Assíncronas:** Celery
-   **DevOps:** Docker, Docker Compose
-   **Documentação:** drf-spectacular (Swagger UI)

## Como Rodar Localmente

**Pré-requisitos:** Docker e Docker Compose instalados.

1.  **Clone o repositório:**
    `git clone https://github.com/seu-usuario/seu-repositorio.git`
    `cd seu-repositorio`

2.  **Configure as variáveis de ambiente:**
    `cp .env.example .env`
    *Edite o arquivo `.env` e preencha com suas chaves.*

3.  **Suba os contêineres e rode as migrações:**
    `docker-compose up --build -d`
    `docker-compose exec web python manage.py migrate`

4.  **Crie um superusuário e um token de acesso:**
    `docker-compose exec web python manage.py createsuperuser`
    `docker-compose exec web python manage.py drf_create_token seu-usuario`

5.  **Acesse a aplicação:**
    -   **API:** `http://localhost:8000/api/weather/?city=London`
    -   **Documentação (Swagger):** `http://localhost:8000/api/docs/`

## Endpoints da API

* `GET /api/weather/?city=<nome_da_cidade>`
* `GET /api/history/`

**Exemplo de uso com cURL:**
`curl -H "Authorization: Token SEU_TOKEN_AQUI" http://localhost:8000/api/weather/?city=Lisbon`

## Decisões Técnicas Principais

1.  **Service Layer:** A lógica da API externa foi isolada em `OpenWeatherService` para desacoplar o código e facilitar testes.
2.  **Celery para Histórico:** A escrita no banco foi movida para uma tarefa assíncrona para não impactar a latência da API.
3.  **Logs Estruturados:** `structlog` foi usado para garantir logs em formato JSON, prontos para plataformas de observabilidade.

## O que faria com mais tempo

-   Implementar CI/CD (GitHub Actions) para automatizar testes e deploy.
-   Refinar a limpeza do histórico para rodar periodicamente (Celery Beat).
-   Adicionar testes de carga (Locust) para validar o comportamento sob estresse.