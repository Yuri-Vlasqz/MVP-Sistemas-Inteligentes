from sklearn.model_selection import train_test_split
import pickle
import pandas as pd
import numpy as np

class PreProcessador:

    def __init__(self):
        """Inicializa o preprocessador"""
        pass

    def separa_teste_treino(self, dataset, percentual_teste, seed=7):
        """ Cuida de todo o pré-processamento. """
        # limpeza dos dados e eliminação de outliers

        # feature selection

        # divisão em treino e teste
        X_train, X_test, Y_train, Y_test = self.__preparar_holdout(dataset,
                                                                  percentual_teste,
                                                                  seed)
        # normalização/padronização
        
        return (X_train, X_test, Y_train, Y_test)
    
    def __preparar_holdout(self, dataset, percentual_teste, seed):
        """ Divide os dados em treino e teste usando o método holdout.
        Assume que a variável target está na última coluna.
        O parâmetro test_size é o percentual de dados de teste.
        """
        dados = dataset.values
        X = dados[:, 0:-1]
        Y = dados[:, -1]
        return train_test_split(X, Y, test_size=percentual_teste, random_state=seed)
    
    def preparar_form(self, form):
        """ Preparação dos dados climáticos recebidos do front para serem usados no modelo.
        """
        # X_input = np.array([form.semana,
        #                     form.temp_min,
        #                     form.temp_med,
        #                     form.temp_max,
        #                     form.precip_med,
        #                     form.umidade_med,
        #                     form.faixa_termica,
        #                     form.dias_chuvosos 
        #                 ])
        # X_input = X_input.reshape(1, -1)
        # Definir os mesmos nomes e ordem das features do treinamento para evitar warning:
        # > UserWarning: X does not have valid feature names, but KNeighborsClassifier was fitted with feature names.
        X_input = pd.DataFrame({
            "week": [form.semana],
            "temp_min": [form.temp_min],
            "temp_med": [form.temp_med],
            "temp_max": [form.temp_max],
            "precip_med": [form.precip_med],
            "rel_humid_med": [form.umidade_med],
            "thermal_range": [form.faixa_termica],
            "rainy_days": [form.dias_chuvosos]
        })
        return X_input
