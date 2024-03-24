import json
from io import StringIO

import pandas as pd
import requests
from bs4 import XMLParsedAsHTMLWarning
from flask import Blueprint, make_response
import warnings

api_bp = Blueprint('api', __name__)

# Ignorando o XMLParsedAsHTMLWarning, pois é feita a análise de um HTML e não de um XML
warnings.simplefilter(action='ignore', category=XMLParsedAsHTMLWarning)


@api_bp.route('/')
def api_home():
    return 'Preencha a URL com o parâmetro "/ano" ou "/ano/mês" para filtrar os feriados por mês.'


@api_bp.route(f'/<ano>/')
def feriados(ano):
    ano = str.strip(ano)
    if ano.isdigit() is False or ano is None or int(ano) < 1:
        return make_response('Insira um ano válido', 400)
    try:
        # Response
        page = requests.get(f"https://www.anbima.com.br/feriados/fer_nacionais/{str.strip(ano)}.asp")

        # Criando um objeto que simula um arquivo
        page_buffer = StringIO(page.text)

        # Dataframe gerado a partir do html da página.
        df_feriados_ano = pd.read_html(page_buffer, match='Data', index_col=None, header=0)
        df_feriados_ano = df_feriados_ano[2]

        # Usando pandas.to_datetime() para converter de string para datetime64
        df_feriados_ano["Data"] = pd.to_datetime(df_feriados_ano["Data"], format="%d/%m/%y")

        # Formatando a data no formato DD/MM/YYYY
        df_feriados_ano["Data"] = df_feriados_ano["Data"].dt.strftime('%d/%m/%Y')
        result = df_feriados_ano.to_json(orient="index")
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4), 200
    except ValueError as e:
        print(e)
        return make_response('Sem dados para exibição', 400)


@api_bp.route(f'/<ano>/<mes>')
def feriados_ano_mes(ano, mes):
    mes = str.strip(mes)
    if mes.isdigit() is False or mes is None or int(mes) < 1 or int(mes) > 12:
        return make_response('Insira um mês válido', 400)
    try:
        # Response
        page = requests.get(f"https://www.anbima.com.br/feriados/fer_nacionais/{ano}.asp")

        # Criando um objeto que simula um arquivo
        page_buffer = StringIO(page.text)

        # Dataframe gerado a partir do html da página.
        df_feriados_mes = pd.read_html(page_buffer, match='Data', index_col=None, header=0)
        df_feriados_mes = df_feriados_mes[2]

        # Usando pandas.to_datetime() para converter de string para datetime64
        df_feriados_mes["Data"] = pd.to_datetime(df_feriados_mes["Data"], format="%d/%m/%y")

        # Filtrando por mês e usando .copy() para evitar o aviso "SettingWithCopyWarning"
        df = df_feriados_mes[df_feriados_mes['Data'].dt.month == int(mes)].copy()

        # Formatando a data no formato DD/MM/YYYY
        df["Data"] = df["Data"].dt.strftime('%d/%m/%Y')

        result = df.to_json(orient="index")
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4), 200
    except ValueError as e:
        print(e)
        return make_response('Sem dados para exibição', 400)
