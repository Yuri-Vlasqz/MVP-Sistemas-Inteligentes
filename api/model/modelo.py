import pickle

class Model:
    
    def __init__(self):
        """Inicializa o modelo"""
        self.model = None
    
    def carrega_modelo(self, path):
        """Carregamento do modelo pré-treinado a partir de um arquivo pickle.
        """
        
        if path.endswith('.pkl'):
            with open(path, 'rb') as file:
                self.model = pickle.load(file)
        else:
            raise Exception('Formato de arquivo não suportado')
        return self.model
    
    def preditor(self, X_input):
        """Realiza a predição de risco de dengue com base em valores climáticos no modelo treinado.
        """
        if self.model is None:
            raise Exception('Modelo não foi carregado. Use carrega_modelo() primeiro.')
        risco_dengue = self.model.predict(X_input)
        return risco_dengue