from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics import recall_score, precision_score

class Avaliador:
    
    def __init__(self):
        """Inicializa o avaliador"""
        pass

    def avaliar_accuracy(self, model, X_test, Y_test):
        """ Faz uma predição e avalia o modelo. Poderia parametrizar o tipo de
        avaliação, entre outros.
        """
        predicoes = model.predict(X_test)
        
        # Caso o seu problema tenha mais do que duas classes, altere o parâmetro average
        return accuracy_score(Y_test, predicoes)
    
    def avaliar_f1(self, model, X_test, Y_test):
        """ Avalia o modelo com a métrica F1 Score.
        """
        predicoes = model.predict(X_test)
        
        # Caso o seu problema tenha mais do que duas classes, altere o parâmetro average
        return f1_score(Y_test, predicoes, average='macro')
    
    def avaliar_recall(self, model, X_test, Y_test):
        """ Avalia o modelo com a métrica Recall.
        """
        predicoes = model.predict(X_test)
        
        # Caso o seu problema tenha mais do que duas classes, altere o parâmetro average
        return recall_score(Y_test, predicoes, average='macro')
    
    def avaliar_precision(self, model, X_test, Y_test):
        """ Avalia o modelo com a métrica Precision.
        """
        predicoes = model.predict(X_test)
        
        # Caso o seu problema tenha mais do que duas classes, altere o parâmetro average
        return precision_score(Y_test, predicoes, average='macro')
                
