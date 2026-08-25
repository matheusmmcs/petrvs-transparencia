# Guia de Desenvolvimento e Manutenção - PETRVS Transparência API (Backend)

Este documento serve como guia simplificado de arquitetura, banco de dados, endpoints e boas práticas para apoiar desenvolvedores e agentes de IA na manutenção da API Backend do PETRVS Transparência.

---

## 📌 1. Visão Geral

- **Tecnologias**: Python 3.11+, FastAPI, SQLAlchemy, PyMySQL, Uvicorn, Docker.
- **Objetivo**: Fornecer endpoints REST otimizados de consulta de dados do Programa de Gestão e Desempenho (PGD) a partir de uma réplica de leitura do banco de dados relacional MySQL do PETRVS.

---

## 🏛️ 2. Estrutura do Projeto

```text
petrvs-transparencia/
├── querybox/
│   ├── planos.sql        # Consulta SQL otimizada para recuperação de planos de trabalho
│   └── entregas.sql      # Consulta SQL para entregas de planos por CPF
├── server.py             # Aplicação FastAPI, configuração do SQLAlchemy e endpoints
├── requirements.txt      # Dependências Python (fastapi, uvicorn, sqlalchemy, pymysql, python-dotenv)
├── Dockerfile            # Imagem Docker da API
├── docker-compose.yml    # Execução local da API na porta 8880
└── README.md             # Instruções de setup
```

---

## 🔌 3. Endpoints da API

### `GET /transparencia-api/planos`
- **Parâmetros**:
  - `data_inicio` (string `YYYY-MM-DD`, obrigatório): Início do período (ex: `2026-01-01`).
  - `data_fim` (string `YYYY-MM-DD`, obrigatório): Fim do período (ex: `2027-01-01`).
- **Comportamento**: Carrega a query em [querybox/planos.sql](querybox/planos.sql), substitui o tenant `{DB_NAME}` e executa com os parâmetros fornecidos. Retorna lista com planos, servidores (com CPF mascarado), unidades, programas e modalidades.

### `GET /transparencia-api/entregas`
- **Parâmetros**:
  - `cpf` (string, obrigatório): CPF do servidor.
- **Comportamento**: Carrega [querybox/entregas.sql](querybox/entregas.sql) e retorna as entregas associadas aos planos de trabalho do servidor.

---

## ⚙️ 4. Variáveis de Ambiente (`.env`)

```ini
DB_USER=user
DB_PASSWORD=password
DB_HOST=1.2.3.4
DB_PORT=3306
DB_NAME=petrvs_database
```

---

## 🚀 5. Comandos de Execução

### Com Docker Compose (Recomendado)
```sh
docker compose up --build
```
Disponível em: `http://localhost:8880`

### Execução Local (Python)
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8880 --reload
```

---

## 🛡️ 6. Boas Práticas e Segurança

1. **Privacidade de Dados**: CPFs devem sempre ser mascarados no formato `123.***.***-**` e e-mails institucionais filtrados conforme regra no SQL.
2. **Consultas SQL em `querybox/`**: Qualquer alteração nas projeções de colunas ou joins deve ser feita diretamente nos arquivos SQL correspondentes em `querybox/`.
3. **Parâmetros com Bind**: Nunca concatenar valores diretamente no SQL; sempre utilizar os parâmetros com bind do SQLAlchemy (`:data_inicio`, `:data_fim`, `:cpf`).
