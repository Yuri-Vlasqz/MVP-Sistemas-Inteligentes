from model import *

# Comando de teste: pytest -s -v test_modelos.py

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
def test_modelo_knn(score=0.85):
    """Testa o modelo KNN e verifica a score minimo das métricas.
    """
    print(f"\nScore mínimo das métricas: {score}")
    # Importando modelo de KNN
    knn_path = './MachineLearning/models/dengue_knn_model_smote_min.pkl'
    print(f"importando modelo KNN em: {knn_path}")
    modelo_knn = modelo.carrega_modelo(knn_path)

    # Obtendo as métricas do KNN
    acuracia_knn = avaliador.avaliar_accuracy(modelo_knn, X, y)
    print(f"- Acurácia:\t{acuracia_knn:.3f}")
    recall_knn = avaliador.avaliar_recall(modelo_knn, X, y)
    print(f"- Recall:\t{recall_knn:.3f}")
    precisao_knn = avaliador.avaliar_precision(modelo_knn, X, y)
    print(f"- Precisão:\t{precisao_knn:.3f}")
    f1_knn = avaliador.avaliar_f1(modelo_knn, X, y)
    print(f"- F1-Score:\t{f1_knn:.3f}")

    # Testando as métricas do KNN
    assert acuracia_knn >= score
    assert recall_knn >= score 
    assert precisao_knn >= score
    assert f1_knn >= score

