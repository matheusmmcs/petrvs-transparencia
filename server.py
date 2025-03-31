
import os
from fastapi import FastAPI, Query, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do banco
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "database")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# Carregar consulta SQL do arquivo
SQL_FILE_PLANOS = "querybox/planos.sql"
SQL_FILE_ENTREGAS = "querybox/entregas.sql"

def load_sql_query(path: str):
    """Carrega a consulta SQL do arquivo e substitui {DB_NAME} pelo valor parametrizado."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            sql_query = file.read()
            return sql_query.replace("{DB_NAME}", DB_NAME)
    except FileNotFoundError:
        raise RuntimeError(f"Arquivo {path} não encontrado")
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar a consulta SQL: {e}")

@app.get("/transparencia-api/planos")
def get_planos(data_inicio: str = Query(...), data_fim: str = Query(...)):
    try:
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
        db = SessionLocal()

        print(f"Data Início: {data_inicio}, Data Fim: {data_fim}")

        sql = load_sql_query(SQL_FILE_PLANOS)

        result = db.execute(text(sql), {"data_inicio": data_inicio, "data_fim": data_fim})
        planos = [dict(row) for row in result.mappings()]

        return planos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/transparencia-api/entregas")
def get_planos(cpf: str = Query(...)):
    try:
        db = SessionLocal()

        print(f"CPF: {cpf}")

        sql = load_sql_query(SQL_FILE_ENTREGAS)

        result = db.execute(text(sql), {"cpf": cpf})
        entregas = [dict(row) for row in result.mappings()]

        return entregas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()