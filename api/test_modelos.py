from model import *

# To run: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()
pipeline = Pipeline()

# Parâmetros    
url_dados = "./MachineLearning/data/test_dataset_dengue.csv"
# colunas precisam ser o mesmo nome e ordem do treinamento para evitar warning no pytest:
# > UserWarning: X does not have valid feature names, but KNeighborsClassifier was fitted with feature names.
colunas = ['week', 'temp_min', 'temp_med', 'temp_max', 'precip_med', 'rel_humid_med', 'thermal_range', 'rainy_days', 'risco_dengue']

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)
array = dataset.values

X = dataset.iloc[:,0:-1]
y = dataset.iloc[:,-1]


# Método para testar modelo KNN a partir do arquivo correspondente
# O nome do método a ser testado necessita começar com "test_"
def test_modelo_knn():
    # Importando modelo de KNN
    knn_path = './MachineLearning/models/dengue_knn_model_smote_min.pkl'
    modelo_knn = modelo.carrega_modelo(knn_path)

    # Obtendo as métricas do KNN
    acuracia_knn = avaliador.avaliar(modelo_knn, X, y)
    
    # Testando as métricas do KNN
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_knn >= 0.85
    # assert recall_knn >= 0.5 
    # assert precisao_knn >= 0.5 
    # assert f1_knn >= 0.5 
