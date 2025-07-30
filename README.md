# API de Consulta de Clima (Weather API)
API RESTful construída com Django e Django REST Framework para consultar o clima atual de uma cidade, utilizando a OpenWeatherMap API. O projeto inclui cache, histórico de buscas e está totalmente containerizado com Docker.

## Funcionalidades Principais
- ✅ Endpoint para buscar o clima atual por cidade.
- ✅ Cache de 10 minutos para as respostas, utilizando Redis.
- ✅ Histórico das últimas 10 consultas salvas em um banco de dados PostgreSQL.
- ✅ Rate Limiting para evitar abuso da API.
- ✅ Logs estruturados em JSON para ambiente de produção.
- ✅ Tarefas assíncronas com Celery para salvar o histórico sem impactar a latência.
- ✅ Documentação interativa da API com Swagger/OpenAPI.
- ✅ Autenticação segura com JSON Web Tokens (JWT) com tempo de vida limitado.
- ✅ Tarefa de manutenção agendada (com Celery Beat) para limpeza otimizada do histórico.
- ✅ Endpoint de Health Check (/health/) para monitoramento da saúde da aplicação.

## Tecnologias Utilizadas
- Backend: Python, Django, Django REST Framework
- Banco de Dados: PostgreSQL
- Cache & Message Broker: Redis
- Tarefas Assíncronas e Agendadas: Celery, Celery Beat
- DevOps: Docker, Docker Compose
- Documentação: drf-spectacular (Swagger UI)

# Como Rodar Localmente
Pré-requisitos: Docker e Docker Compose instalados.
1. Clone o repositório:
```
git clone https://github.com/SzCleiton/weather-api.git
cd seu-repositorio
```

2. Configure as variáveis de ambiente:
```
cp .env.example .env
```
Edite o arquivo .env e preencha com suas chaves.

3. Suba os contêineres e rode as migrações:
```
docker-compose up --build -d
docker-compose exec web python manage.py migrate
```

4. Crie um superusuário:
```
docker-compose exec web python manage.py createsuperuser
```

5. Obtenha seus tokens de acesso:
Use o Swagger UI, Insomnia, Postman ou cURL para fazer uma requisição POST para o endpoint /api/token/ com o usuário e senha que você acabou de criar.

Exemplo com cURL:
```
curl -X POST -H "Content-Type: application/json" -d '{"username": "seu-usuario", "password": "sua-senha"}' http://localhost:8000/api/token/
```
A resposta conterá seus tokens access e refresh.

6. Acesse a aplicação:

- API: http://localhost:8000/api/weather/?city=Hortolandia
- Documentação (Swagger): http://localhost:8000/api/docs/
- Health Check: http://localhost:8000/health/

## Endpoints da API
- GET /api/weather/?city=<nome_da_cidade>: Retorna o clima atual.
- GET /api/history/: Retorna as últimas 10 cidades pesquisadas.
- GET /health/: Verifica a saúde da aplicação e serviços conectados.
- POST /api/token/: Para obter o par de tokens de acesso e de atualização.
- POST /api/token/refresh/: Para obter um novo token de acesso usando um token de atualização.

### Exemplo de uso com cURL:

```
curl -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI" http://localhost:8000/api/weather/?city=Lisbon
```

# Decisões Técnicas Principais
1. Service Layer: A lógica da API externa foi isolada em OpenWeatherService para desacoplar o código e facilitar testes.
2. Logs Estruturados: structlog foi usado para garantir logs em formato JSON, prontos para plataformas de observabilidade.
3. Autenticação com JWT: Adoção de JWT por ser um padrão moderno e mais seguro que tokens estáticos, implementando tokens com tempo de vida limitado para mitigar riscos de vazamento.
4. Tarefas de Manutenção com Celery Beat: Uso do Celery Beat para tarefas periódicas, desacoplando a limpeza do histórico do fluxo de requisição da API e otimizando a performance do banco de dados.

## O que faria com mais tempo
- Implementar CI/CD (GitHub Actions) para automatizar testes e deploy.
- Adicionar testes de carga (com Locust, por exemplo) para validar o comportamento do cache e do rate limiting sob estresse.

### Mensagem ao dev
- Esse é um exemplo de readme que ja tinha pronto, fiz apenas umas alterações e coloquei aqui, quis fazer de uma forma mais bonita para voces estenderem certinho como foi desenvolvimento do projeto, espero qeu gostem

Com carinho e muita dedicação Cleiton.
Abraço.