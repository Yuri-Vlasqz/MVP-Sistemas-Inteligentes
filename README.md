# Sistema de Classificação de Risco de Dengue **(WIP)**
MVP da Sprint: Qualidade de Software, Segurança e Sistemas Inteligentes

Sistema inteligente para classificação de risco de incidência de dengue baseado em dados climáticos históricos. Este projeto utiliza machine learning para analisar condições meteorológicas e prever o risco de dengue em municípios brasileiros.

## 🎯 Objetivo

Desenvolver uma ferramenta que auxilie na prevenção e controle da dengue através da análise de dados climáticos, fornecendo classificações de risco (baixo, médio, alto) para diferentes regiões.

## ✨ Funcionalidades

- **Consulta de Clima Histórico**: Integração com WeatherAPI para obter dados dos últimos 7 dias
- **Classificação Inteligente**: Modelo de machine learning (KNN) treinado para classificar risco de dengue


## 🔧 Tecnologias Utilizadas

### Backend
- **Python 3.12.9**
- **Flask** - Framework web
- **Flask-OpenAPI3** - Documentação automática da API com Swagger-UI
- **Scikit-learn** - Biblioteca de treinamento de modelo Machine learning
- **Pandas** - Manipulação de dados
- **Requests** - Chamadas HTTP para API externa do WeatherAPI

### Frontend
- **HTML5/CSS3/JavaScript** para iterface responsiva
- **API Fetch** para comunicação com backend

### APIs Externas
- **WeatherAPI** - Dados climáticos históricos
    - Chave de API gratuita


## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/MVP-Sistemas-Inteligentes.git
cd MVP-Sistemas-Inteligentes
```

### 2. Configure o ambiente virtual
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r api\requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do repositório:
```
WEATHERAPI_KEY=sua_chave_da_weatherapi_aqui
```

Para obter uma chave gratuita da WeatherAPI:
1. Acesse [WeatherAPI](https://www.weatherapi.com/)
2. Crie uma conta gratuita
3. Copie sua API Key

## 📖 Como Usar

### 1. Iniciar o servidor
```bash
cd api
python app.py
```

### 2. Acesse a aplicação
- **Frontend**: http://localhost:5000
- **Documentação da API**: http://localhost:5000/docs

### 3. Fluxo de uso da aplicação

#### Etapa 1: Consulta de Clima
1. Digite o nome do município (ex: "Rio de Janeiro")
2. Clique em "Consultar Clima"
3. O sistema buscará dados dos últimos 7 dias

#### Etapa 2: Dados Climáticos
1. Visualize os dados coletados
2. Confirme os parâmetros preenchidos automaticamente
3. Clique em "Classificar Risco"

#### Etapa 3: Resultado
1. Visualize a classificação de risco
2. Analise os dados utilizados
3. Inicie uma nova consulta se necessário


## 📁 Estrutura do Projeto

```
MVP-Sistemas-Inteligentes/
├── api/                    # Backend Flask
│   ├── app.py                  # Aplicação principal
│   ├── schemas/                # Esquemas Pydantic
│   ├── model/                  # Classes do modelo ML
│   ├── MachineLearning/        # Modelos treinados
│   └── requirements.txt        # Dependências Python
├── front/                  # Frontend
│   ├── index.html              # Página principal
│   ├── script.js               # Lógica JavaScript
│   └── styles.css              # Estilos CSS
├── .env                    # arquivo com chave de API (deve ser criado)
└── README.md               # Documentação
```

## Modelo de Machine Learning

- **Algoritmo**: K-Nearest Neighbors (KNN)
- **Técnica de Balanceamento**: SMOTE
- **Features**: Dados climáticos semanais
- **Classes**: Risco Baixo (0), Médio (1), Alto (2)

### Parâmetros de Entrada
- Semana do ano
- Temperatura mínima, média e máxima
- Precipitação média
- Umidade média
- Faixa térmica
- Dias chuvosos


## 🧪 Testes

Para testar a API, utilize a documentação interativa em `/docs`
