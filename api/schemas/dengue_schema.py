from pydantic import BaseModel


class DenguePredictSchema(BaseModel):
    """ Define os parâmetros de entrada para a predição de risco de dengue
    """
    semana: int #= 15
    temp_min: float #= 18.065386
    temp_med: float #= 21.480171
    temp_max: float #= 25.546371
    precip_med: float #= 12.292
    umidade_med: float #= 80.052214
    faixa_termica: float #= 7.480986
    dias_chuvosos: int #= 7


class DengueViewSchema(BaseModel):
    """ Define como o risco de dengue será representado na resposta
    """
    risco_dengue: int
    descricao: str = "Risco de dengue (baixo, médio ou alto)."


def apresenta_risco_dengue(risco_dengue: int):
    """ Formata a resposta de risco de dengue entre 0=baixo, 1=médio e 2=alto.
    """
    if risco_dengue == 0:
        descricao = "Risco baixo de incidência de dengue."
    elif risco_dengue == 1:
        descricao = "Risco médio de incidência dengue."
    elif risco_dengue == 2:
        descricao = "Risco alto de incidência dengue."
    else:
        descricao = "Erro ao classificar o risco de dengue."
    
    return {
        "risco_dengue": risco_dengue,
        "descricao": descricao
    }
    