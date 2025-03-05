
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

def load_sql_query():
    """Carrega a consulta SQL do arquivo e substitui {DB_NAME} pelo valor parametrizado."""
    try:
        with open(SQL_FILE_PLANOS, "r", encoding="utf-8") as file:
            sql_query = file.read()
            return sql_query.replace("{DB_NAME}", DB_NAME)
    except FileNotFoundError:
        raise RuntimeError(f"Arquivo {SQL_FILE_PLANOS} não encontrado")
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar a consulta SQL: {e}")

SQL_QUERY = load_sql_query()

@app.get("/transparencia-api/planos")
def get_planos(data_inicio: str = Query(...), data_fim: str = Query(...)):
    try:
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
        db = SessionLocal()

        print(f"Data Início: {data_inicio}, Data Fim: {data_fim}")

        result = db.execute(text(SQL_QUERY), {"data_inicio": data_inicio, "data_fim": data_fim})
        planos = [dict(row) for row in result.mappings()]

        return planos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()