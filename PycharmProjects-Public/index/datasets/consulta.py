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

sql = '''

'''
