from flask import Blueprint
import pandas as pd
import requests
import json

api_bp = Blueprint('api', __name__)


@api_bp.route('/')
def api_home():
    return 'Preencha a URL com o parâmetro "/ano".'


@api_bp.route(f'/<ano>/')
def feriados(ano):
    try:
        # Response
        page = requests.get(f"https://www.anbima.com.br/feriados/fer_nacionais/{ano}.asp")
        # Dataframe gerado a partir do html da página.
        df_feriados = pd.read_html(page.text, match='Data', index_col=None, header=0)
        df_feriados = df_feriados[2]
        result = df_feriados.to_json(orient="index")
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4)
    except Exception as e:
        print(e)
        return 'Sem dados para exibição'
