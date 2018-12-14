Used to mark chat dialogs by a set of topics / subtopics for later usage as a training set for neural network classifier.
App itself starts with docker-compose and consists of django app itself (ran by gunicorn) and nginx as reverse proxy.
It requires external PostgreSQL 10+ and Elasticsearch 5.6 + Kibana 5.6.
Optionally you can add Consul 1.2.3 and Logstash 5.6.

### Requirements:
docker
django 2.0+
psycopg2 2.7.5

### External services used:
1) PostgreSQL 10+
2) Consul 1.2.3 (Optional. Used only as KV, can be replaced by setting ENV)
3) Elasticsearch 5.6
4) Kibana 5.6
5) Logstash 5.6 with postgres plugin (Optional)

### Запуск
1-a) Fill consul KV with settings
* DB_HOST=<postgres_host>
* DB_PORT=5432
* DB_NAME=bots
* DB_USER=<username>
* DB_PASS=<password>
* ELASTIC_URL=<host:port ELASTIC>  - using this path collection dialogs will be created
 
fill app.env with:
* CONSUL_URL=<full URL to consul's http API, including folders>

if any of settings is not loaded from consul, app wil try to find all the settings in ENV
#### OR
1-b) Fill app.env with variables from 1-a

2) `docker-compose up -d`
3) `docker exec dialog_marker_app python manage.py collectstatic`


