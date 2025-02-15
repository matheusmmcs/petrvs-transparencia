
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

SQL_QUERY = """
    SELECT 
      pt.id as plano_trablho_id,
      pt.numero as plano_trabalho_numero,
      pt.data_inicio as plano_trabalho_data_inicio,
      pt.data_fim as plano_trabalho_data_fim,
      pt.status as plano_trabalho_status,
      u.apelido as usuario_apelido,
      u.nome as usuario_nome,
      CONCAT(SUBSTRING(u.cpf, 1, 3), '.***.***-**') AS usuario_cpf_mascarado,
      u.telefone as usuario_telefone,
        CASE 
            WHEN LOCATE('petrvs.gov.br', u.email) = 0 THEN u.email 
            ELSE NULL 
        END AS usuario_email_filtrado,
      un.nome as unidade_nome,
      un.sigla as unidade_sigla,
      un.codigo as unidade_codigoo,
      tm.nome as modalidade_nome
      #documento
    from petrvs_ufpi.planos_trabalhos pt 
    inner join petrvs_ufpi.usuarios u on pt.usuario_id = u.id 
    inner join petrvs_ufpi.unidades un on pt.unidade_id = un.id 
    inner join petrvs_ufpi.tipos_modalidades tm on pt.tipo_modalidade_id = tm.id
    #inner join petrvs_ufpi.documentos d on pt.documento_id = d.id   
    where 
    u.cod_jornada < 99
    AND pt.status in (
      'ATIVO',
      'AGUARDANDO_ASSINATURA',
      'CONCLUIDO',
      'INCLUIDO'
    )
    AND pt.data_inicio >= :data_inicio 
    AND pt.data_fim < :data_fim
    ORDER BY u.nome, pt.created_at DESC;
"""

@app.get("/planos")
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