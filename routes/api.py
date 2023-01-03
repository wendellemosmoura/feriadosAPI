from flask import Blueprint
import pandas as pd
import requests
import json

api_bp = Blueprint('api', __name__)


@api_bp.route('/')
def api_home():
    return 'Preencha a URL com o parâmetro "/ano" ou "/ano/mês" para filtrar os feriados por mês.'


@api_bp.route(f'/<ano>/')
def feriados(ano):
    ano = str.strip(ano)
    if ano.isdigit() is False or ano is None or int(ano) < 1:
        return 'Insira um mês válido'
    try:
        # Response
        page = requests.get(f"https://www.anbima.com.br/feriados/fer_nacionais/{str.strip(ano)}.asp")
        # Dataframe gerado a partir do html da página.
        df_feriados = pd.read_html(page.text, match='Data', index_col=None, header=0)
        df_feriados = df_feriados[2]
        # Usando pandas.to_datetime() para converter de string para datetime64
        df_feriados["Data"] = pd.to_datetime(df_feriados["Data"], format="%d/%m/%y")
        # Formatando a data no formato DD/MM/YYYY
        df_feriados["Data"] = df_feriados["Data"].dt.strftime('%d/%m/%Y')
        result = df_feriados.to_json(orient="index")
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4)
    except Exception as e:
        print(e)
        return 'Sem dados para exibição'


@api_bp.route(f'/<ano>/<mes>')
def feriados_ano_mes(ano, mes):
    mes = str.strip(mes)
    if mes.isdigit() is False or mes is None or int(mes) < 1 or int(mes) > 12:
        return 'Insira um mês válido'
    try:
        # Response
        page = requests.get(f"https://www.anbima.com.br/feriados/fer_nacionais/{ano}.asp")
        # Dataframe gerado a partir do html da página.
        df_feriados = pd.read_html(page.text, match='Data', index_col=None, header=0)
        df_feriados = df_feriados[2]
        # Usando pandas.to_datetime() para converter de string para datetime64
        df_feriados["Data"] = pd.to_datetime(df_feriados["Data"], format="%d/%m/%y")
        # Filtrando por mês
        df = df_feriados[df_feriados['Data'].dt.month == int(mes)]
        # Formatando a data no formato DD/MM/YYYY
        df["Data"] = df["Data"].dt.strftime('%d/%m/%Y')
        result = df.to_json(orient="index")
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4)
    except Exception as e:
        print(e)
        return 'Sem dados para exibição'
