import pytest
import json
from app import app
from model import Session, Paciente

# To run: pytest -v test_api.py

@pytest.fixture
def client():
    """Configura o cliente de teste para a aplicação Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_patient_data():
    """Dados de exemplo para teste de paciente"""
    return {
        "name": "João Silva",
        "preg": 2,
        "plas": 120,
        "pres": 80,
        "skin": 35,
        "test": 180,
        "mass": 25.5,
        "pedi": 0.5,
        "age": 35
    }

def test_home_redirect(client):
    """Testa se a rota home redireciona para o frontend"""
    response = client.get('/')
    assert response.status_code == 302
    assert '/front/index.html' in response.location

def test_docs_redirect(client):
    """Testa se a rota docs redireciona para openapi"""
    response = client.get('/docs')
    assert response.status_code == 302
    assert '/openapi' in response.location


def test_prediction_edge_cases(client):
    """Testa casos extremos para predição"""
    # Teste com valores mínimos
    min_data = {
        "name": "Paciente Minimo",
        "preg": 0,
        "plas": 0,
        "pres": 0,
        "skin": 0,
        "test": 0,
        "mass": 0.0,
        "pedi": 0.0,
        "age": 21
    }
    
    response = client.post('/paciente', 
                          data=json.dumps(min_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'outcome' in data
    
    # Teste com valores máximos típicos
    max_data = {
        "name": "Paciente Maximo",
        "preg": 17,
        "plas": 199,
        "pres": 122,
        "skin": 99,
        "test": 846,
        "mass": 67.1,
        "pedi": 2.42,
        "age": 81
    }
    
    response = client.post('/paciente', 
                          data=json.dumps(max_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'outcome' in data
