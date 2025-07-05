from pydantic import BaseModel
from statistics import mean

class MunicipioSchema(BaseModel):
    """ Define como o município será representado na resposta.
    """
    nome: str = "Rio de Janeiro"


class CondicaoSchema(BaseModel):
    """ Define como a condição climática será representada.
    """
    text: str
    icon: str
    code: int


class ClimaDiaSchema(BaseModel):
    """ Define como resumo dos dados climáticos de um dia serão representados.
    """
    data: str
    temp_min: float
    temp_max: float
    precip_total: float
    umidade_med: float
    condicao: CondicaoSchema

class ClimaHistoricoSchema(BaseModel):
    """ Define como os dados climáticos históricos serão representados
    """
    municipio: str
    regiao: str
    pais: str
    data_inicio: str
    data_fim: str
    media_temp_min: float
    media_temp_med: float
    media_temp_max: float
    media_precip_total: float
    media_umidade_med: float
    dias_chuvosos: int
    dias: list[ClimaDiaSchema]


def apresenta_clima_historico(response_wheather_api: dict):
    """ Formata a resposta de clima histórico da WeatherAPI (médias e dias individuais).
    """
    forecast_days = response_wheather_api['forecast']['forecastday']

    temp_min_lista = []
    temp_med_lista = []
    temp_max_lista = []
    precip_total_lista = []
    umidade_med_lista = []
    dias_chuvosos = 0
    dias = []

    for day in forecast_days:

        # Dados de médias semanais
        temp_min_lista.append(day['day']['mintemp_c'])
        temp_med_lista.append(day['day']['avgtemp_c'])
        temp_max_lista.append(day['day']['maxtemp_c'])
        precip_total_lista.append(day['day']['totalprecip_mm'])
        umidade_med_lista.append(day['day']['avghumidity'])
        dias_chuvosos += day['day']['daily_will_it_rain']
        
        # Dados de dias individuais
        dias.append({
            'data': day['date'],
            'temp_min': day['day']['mintemp_c'],
            'temp_med': day['day']['avgtemp_c'],
            'temp_max': day['day']['maxtemp_c'],
            'precip_total': day['day']['totalprecip_mm'],
            'umidade_med': day['day']['avghumidity'],
            'condicao': day['day']['condition']
        })

    return {
        'latitude': response_wheather_api['location']['lat'],
        'longitude': response_wheather_api['location']['lon'],
        'municipio': response_wheather_api['location']['name'],
        'regiao': response_wheather_api['location']['region'],
        'pais': response_wheather_api['location']['country'],
        'data_inicio': forecast_days[0]['date'],
        'data_fim': forecast_days[-1]['date'],
        'media_temp_min': round(mean(temp_min_lista), 2),
        'media_temp_med': round(mean(temp_med_lista), 2),
        'media_temp_max': round(mean(temp_max_lista), 2),
        'media_precip_total': round(mean(precip_total_lista), 2),
        'media_umidade_med': round(mean(umidade_med_lista), 2),
        'dias_chuvosos': dias_chuvosos,
        'dias': dias
    }