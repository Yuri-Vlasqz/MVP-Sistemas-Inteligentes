from dotenv import load_dotenv
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_cors import CORS
import requests

from model import *
from logger import logger
from schemas import *

from datetime import datetime, timedelta
import os


# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(
    __name__, info=info, static_folder="../front", static_url_path="/front"
)
CORS(app)

# Carregar variáveis de ambiente
load_dotenv()
# Configuração da API Key
WEATHERAPI_KEY = os.getenv('WEATHERAPI_KEY')
WEATHERAPI_BASE_URL = "http://api.weatherapi.com/v1/history.json"


def obter_clima_historico(municipio, data_inicio, data_fim):
    """
    Faz a chamada para a WeatherAPI para obter dados históricos
    
    Args:
        municipio (str): Nome do município
        data_inicio (str): Data de início no formato YYYY-MM-DD
        data_fim (str): Data de fim no formato YYYY-MM-DD
        
    Returns:
        dict: Resposta da API ou None em caso de erro
    """
    try:
        params = {
            'key': WEATHERAPI_KEY,
            'q': municipio,
            'dt': data_inicio,
            'end_dt': data_fim
        }

        response = requests.get(WEATHERAPI_BASE_URL, params=params)
        
        return response.json()
        
    except Exception as e:
        return None


# Definindo tags para agrupamento das rotas
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
clima_tag = Tag(
    name="Clima-Historico",
    description="Rota para consulta de clima via WheatherAPI em uma cidade específica",
)
classificador_tag = Tag(
    name="Classificador-Dengue",
    description="Rota para classificação de risco de incidência de dengue em um local por meio de dados de climáticos, usando um modelo de machine learning.",
)


# Rota home - redireciona para o frontend
@app.get("/", tags=[home_tag])
def home():
    """Redireciona para o index.html do frontend."""
    return redirect("/front/index.html")


# Rota para documentação OpenAPI
@app.get("/docs", tags=[home_tag])
def docs():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


# Rota de para consulta de clima histórico (7 dias) em um município.
@app.get(
    "/clima-historico",
    tags=[clima_tag],
    responses={"200": ClimaHistoricoSchema, "400": ErrorSchema, "500": ErrorSchema},
)
def clima_historico(query: MunicipioSchema):
    """Consulta o clima histórico de um município pelo serviço externo WheatherAPI.
    """

    if not WEATHERAPI_KEY:
        return {"message": "Configure a variável WEATHERAPI_KEY no arquivo .env"}, 500
    
    # Datas dos últimos 7 dias (6 + hoje)
    data_fim = datetime.now().date()
    data_inicio = data_fim - timedelta(days=6)
    data_inicio_str = data_inicio.strftime('%Y-%m-%d')
    data_fim_str = data_fim.strftime('%Y-%m-%d')
    
    try:
        # Requisição na WeatherAPI
        dados_wheater_api = obter_clima_historico(query.nome, data_inicio_str, data_fim_str)
        
        if not dados_wheater_api:
            return {"message": f"Erro interno na requisição ao WeatherAPI buscar clima em {query.nome}"}, 500
        
        if 'error' in dados_wheater_api:
            return {"message": f"Erro na WeatherAPI ao buscar clima em {query.nome}: {dados_wheater_api['error']['message']}"}, 400
        
        return apresenta_clima_historico(dados_wheater_api), 200
        
    except Exception as e:
        return {"message": f"Erro ao buscar clima do município {query.nome}"} , 500 


@app.post(
    "/classificador-dengue", 
    tags=[classificador_tag],
    responses={
        "200": DengueViewSchema,
        "400": ErrorSchema,
    },
)
def predict_dengue(form: DenguePredictSchema):
    """Classifica o risco de incidência de dengue em um município a partir de dados climáticos.
    """
    # Instanciando classes
    preprocessador = PreProcessador()
    classificador = Model()
    try:
        # Preparando os dados para o modelo
        X_input = preprocessador.preparar_form(form)
        # Carregando modelo
        model_path = "./MachineLearning/models/dengue_knn_model_smote_min.pkl"
        classificador.carrega_modelo(model_path)
        # Realizando a predição
        risco_dengue = int(classificador.preditor(X_input)[0])

    except Exception as e:
        logger.error(f"Erro ao realizar predição: {e}")
        return {"message": "Erro ao processar os dados de entrada."}, 400

    return apresenta_risco_dengue(risco_dengue), 200


if __name__ == "__main__":
    logger.info("Acesse a documentação em: http://localhost:5000/docs")
    app.run(debug=True)
