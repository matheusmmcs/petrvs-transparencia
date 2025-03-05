# PETRVS - Transparência API (PGD)

Como executar o projeto API Transparência em ambiente de desenvolvimento (docker):


## 💻 1 -  Desenvolvimento

Basta configurar os arquivos:

 - .env, conforme .env-sample (conexão com o banco do Petrvs read-only):
 
 ```ini
DB_USER=user
DB_PASSWORD="pass"
DB_HOST=1.2.3.4
DB_PORT=3306
DB_NAME=petrvs_tenant
```

- caso seja necessário adaptar a consulta da API, alterar o script em querybox/planos.sql;

Em seguida executar o comando:

```sh
docker-compose up --build
```

A API ficará disponível em **[http://0.0.0.0:8880](http://0.0.0.0:8880)**! 🚀