# Transparência - PGD (Petrvs)

Como executar o projeto em ambiente de desenvolvimento (docker):


## 💻 1 -  Desenvolvimento

Basta configurar os arquivos:

 - .env (conexão com o banco do Petrvs read-only):
 
 ```ini
DB_USER=user
DB_PASSWORD="pass"
DB_HOST=1.2.3.4
DB_PORT=3306
DB_NAME=petrvs_tenant
```

 Em seguida executar o comando:

```sh
docker-compose up --build
```

OBS: ao testar, abrir um navegador com CORS desabilitado. No MacOS pode-se utilizar o seguinte comando:

```sh
open -n -a /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --args --user-data-dir="/tmp/chrome_dev_test" --disable-web-security
```

### 1.2 - Limpar imagens antigas:

Para realizar a limpeza de lixo do docker:

```sh
docker ps -a | grep 'petrvs-transparencia' | awk '{print $1}' | xargs docker rm -f
docker images | grep 'petrvs-transparencia' | awk '{print $3}' | xargs docker rmi -f
docker volume prune -f

```


## 🚀 2 - Deploy em Produção

O processo de deploy do sistema **Vue (PrimeVue + Vite) + API Python** utilizando **Docker** e **Nginx** com suporte a **SSL** possui alguns passos a mais.

----------

### 🚧 2.1. Preparar o Servidor

#### 2.1.1. Instalar Docker e Docker Compose

Se ainda não tem Docker instalado, execute:

```sh
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose

```

Adicione o usuário ao grupo do Docker:

```sh
sudo usermod -aG docker $USER
newgrp docker

```

Verifique se o Docker está rodando:

```sh
docker --version
docker-compose --version

```

----------

### 📂 2.2. Clonar o Projeto no Servidor

Se o código-fonte está no **GitHub/GitLab**, clone o repositório:

```sh
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo

```

Se o código já estiver no servidor, vá até a pasta onde estão os arquivos do **`docker-compose.prod.yml`**.

----------

### 🔐 2.3. Configurar Certificados SSL

Se ainda não fez isso, crie a pasta **ssl/** no diretório do projeto e adicione os arquivos:

```sh
mkdir ssl
mv fullchain.pem ssl/
mv privkey.pem ssl/

```

Se quiser usar **Let's Encrypt**, gere o certificado com:

```sh
docker run --rm -it \
  -v /etc/letsencrypt:/etc/letsencrypt \
  -v /var/lib/letsencrypt:/var/lib/letsencrypt \
  certbot/certbot certonly --standalone -d seu-dominio.com

```

Depois, edite o `nginx.conf` e modifique os caminhos do certificado:

```nginx
ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;

```

OBS: caso queira testar o build de produção, mas sem SSL, há um nginx-no-ssl.conf que deve alterar o front-end/Dockerfile.prod no trecho:

```nginx
...
COPY nginx/nginx-no-ssl.conf /etc/nginx/conf.d/default.conf
...

```

----------

### ⚙️ 2.4. Criar Arquivo `.env`

Crie um arquivo `.env` no diretório do projeto e adicione as variáveis de ambiente:

```ini
DB_USER=user
DB_PASSWORD="pass"
DB_HOST=1.2.3.4
DB_PORT=3306
DB_NAME=petrvs_tenant
```

Em seguida crie o `./front-end/.env` :

```ini
VITE_API_URL=http://localhost:8880
VITE_HEADER_TITLE=Transparência PGD - Órgão
VITE_FOOTER_TEXT=STI e CPGD / UFPI © 2025
```

----------

### 🚀 2.5. Rodar o Deploy

Agora, execute:

```sh
docker-compose -f docker-compose.prod.yml build
docker images
docker-compose -f docker-compose.prod.yml up -d

```

Se quiser verificar os logs:

```sh
docker-compose -f docker-compose.prod.yml logs -f

```

----------

### 🔎 2.6. Testar a Aplicação

Agora, acesse seu front-end via **HTTPS**:

-   **[https://seu-dominio.com:8188](https://seu-dominio.com:8188/)** (pode configurar as portas no docker-compose.prod.yml);
-   O redirecionamento de HTTP para HTTPS já estará funcionando.

Para reiniciar o ambiente:

```sh
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

```

Caso precise atualizar o código, faça o **pull do repositório**, rebuild e reinicie:

```sh
git pull origin main  # Atualiza o código do repositório
docker-compose -f docker-compose.prod.yml down # para e remove containers anteriores do projeto
docker-compose -f docker-compose.prod.yml up --build -d  # Rebuild e restart

```

Agora seu **deploy de produção está pronto**! 🚀