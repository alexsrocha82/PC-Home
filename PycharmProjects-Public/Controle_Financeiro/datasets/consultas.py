import psycopg2
import pandas as pd
import datetime
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from app import app

# BANCO DE DADOS
db_host ="localhost"
db_name = "financeiro"
db_port = "5432"
db_user = "postgres"
db_pass = "user"

# CONEXAO
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host)

# SQL
# val_tot_receita
tot_receita = '''
        SELECT TO_CHAR(SUM(F.VALOR),'L999G999G990D99') AS TOT,
               ROUND(SUM(F.valor),2) AS VALOR
          FROM DW.FATO_DESPESA_DIA F
          WHERE 1=1
            AND F.TIPO = 'Receita'
'''

categoria_val = '''
    SELECT FATO_DESPESA_DIA.CATEGORIA,
           SUM(FATO_DESPESA_DIA.VALOR) AS TOTAL
      FROM DW.FATO_DESPESA_DIA
           GROUP BY FATO_DESPESA_DIA.CATEGORIA
           
           UNION 
           
   SELECT 'Gts Geral' AS CATEGORIA,
          SUM(FATO_DESPESA_DIA.VALOR) AS TOTAL
     FROM DW.FATO_DESPESA_DIA
'''