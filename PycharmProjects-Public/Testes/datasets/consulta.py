import psycopg2
import pandas as pd
import datetime
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from app import app

# BANCO DE DADOS
db_host ="192.168.0.110"
db_name = "dadosadv"
db_port = "5432"
db_user = "postgres"
db_pass = "CTMGethohF3eechoTIcme"

# CONEXAO
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host)

# SQL
sql_fat = '''
WITH TAB AS (

SELECT D2_DOC         AS NUM_NF,
       D2_PEDIDO      AS NUM_PED,
       D2_SERIE       AS SERIE_NF,
       D2_CLIENTE     AS COD_CLIENTE,
       A1.A1_NOME     AS NOME_CLI,
       A1.A1_EST      AS UF,
       D2_TOTAL       AS VAL_TOT,
       D2_EMISSAO     AS DT_EMISSAO,
       CAST(EXTRACT( YEAR FROM (TO_DATE(D2_EMISSAO,'YYYYMMDD')))AS INT) AS ANO
  FROM SD2010 SD2
       INNER JOIN SA1010 A1  ON A1.A1_COD = SD2.D2_CLIENTE AND A1.A1_LOJA = SD2.D2_LOJA
   WHERE 1 = 1
     AND D2_CLIENTE NOT IN ('33516290','CLIGEN001')
     AND SD2.D_E_L_E_T_ = ''
     AND A1.D_E_L_E_T_ = ''
     AND (D2_FILIAL = '01BRQ01'OR D2_FILIAL = '01BRQ05')
     AND D2_EMISSAO >= '20190101'
     AND (D2_SERIE = '001' OR D2_SERIE = 'D')
     AND D2_TIPO = 'N'
     AND (D2_CF = '5101 '
      OR D2_CF = '6101 '
      OR D2_CF = '5102 '
      OR D2_CF = '6102 '
      OR D2_CF = '5405 '
      OR D2_CF = '6405 '
      OR D2_CF = '5113 '
      OR D2_CF = '6113 '
      OR D2_CF = '5401 '
      OR D2_CF = '6401 '
      OR D2_CF = '5109 '
      OR D2_CF = '6109 '
      OR D2_CF = '5110 '
      OR D2_CF = '6110 '
      OR D2_CF = '5403 '
      OR D2_CF = '6403 '
      OR D2_CF = '5402 '
      OR D2_CF = '6402 '
      OR D2_CF = '6118 '
      OR D2_CF = '6107 '
      OR D2_CF = '6108 '
      OR D2_CF = '6404 '
      OR D2_CF = '5404 '
      OR D2_CF = '7101 '
      OR D2_CF = '7102 ') 
      ) 
          SELECT * FROM TAB
'''
