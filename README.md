# MVP Sistemas Inteligentes - Classificação de Risco de Dengue
Este repositório contém a implementação do MVP (Minimum Viable Product) da Sprint de Qualidade de Software, Segurança e Sistemas Inteligentes do Curso de Engenharia de Software da PUC-Rio.

> No contexto da dificuldade em prever de forma prática, em qual local pode estar em maior risco de incidência de dengue, foi criado esse sistema inteligente para classificar o risco de dengue em 3 patamares (`Baixo`, `Médio` e `Alto`), baseado na análise de dados climáticos históricos durante a última semana e o número da semana no ano.

<br>

## Funcionalidades de rotas

- `GET /clima-historico` - **Consulta de Clima Histórico**: Integração com WeatherAPI para obter dados dos últimos 7 dias
- `POST /classificador-dengue` **Classificação Inteligente**: Modelo de machine learning (KNN) treinado para classificar risco de dengue

<br>

## Principais Tecnologias

### Backend
- **Python 3.12**
- **Flask-OpenAPI3** - Framework web com documentação automática da API com Swagger-UI
- **Pandas e Scikit-learn** - Manipulação de dados e treinamento de modelo Machine learning
- **Requests** - Chamadas HTTP para API externa do WeatherAPI


### Frontend
- **HTML5/CSS3/JavaScript** para iterface responsiva
- **Leaflet e OpenStreetMap**: para mapas interativos e dados cartográficos.


### APIs Externas
![weatherapi_logo](https://cdn.weatherapi.com/v4/images/weatherapi_logo.png)
- **[WeatherAPI](https://www.weatherapi.com/)** - Serviço de dados meteorológicos que possibilita integração de dados sobre clima e geolocalização (Chave de API gratuita)

<br>

## Modelo de Machine Learning utilizado

- **Algoritmo**: K-Nearest Neighbors ([KNN](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html))
- **Técnica de Preprocessamento para treino**: [SMOTE](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html) (Sobreamostragem para equilibrar conjuntos de dados de classes minoritárias, criando exemplos interpolados entre vizinhos da própria classe.)
- **Features**: Dados climáticos semanais
- **Classes**: Risco Baixo (0), Médio (1), Alto (2)

### Parâmetros de entrada para classificação
- Semana do ano
- Temperatura mínima, média e máxima
- Precipitação média
- Umidade média
- Faixa térmica
- Dias chuvosos

<br>

## Estrutura do Projeto

```
MVP-Sistemas-Inteligentes/
├── api/                    # Backend Flask
│   ├── app.py                  # Aplicação e rotas Flask
│   ├── schemas/                # schemas de rotas
│   ├── model/                  # Classes do modelo ML
│   ├── MachineLearning/        # datasets, Modelos treinados e notebooks
│   └── requirements.txt        # Dependências Python
│
├── front/                  # Frontend
│   ├── index.html              # Página principal
│   ├── script.js               # Lógica JavaScript
│   └── styles.css              # Estilos CSS
│
├── .env                    # arquivo com chave de API (deve ser criado)
└── README.md               # Documentação
```

<br>

## Instalação

### 1. Clone o repositório pela URL

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
2. Crie uma conta e obtenha um chave gratuita ao se [registrar](https://www.weatherapi.com/signup.aspx)
3. Copie sua API Key do seu [dashboard](https://www.weatherapi.com/my/)

<br>

## Como Usar
### 1. Acesse o diretorio da API (se estiver na raiz do repositório)
```bash
cd api
```

### 2. Execute a API
```
flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
flask run --host 0.0.0.0 --port 5000 --reload
```

### 3. Acesse a aplicação
- **Frontend**: http://localhost:5000
- **Documentação da API**: http://localhost:5000/docs

<br>

## Fluxo de uso da aplicação pela inteface/frontend

### Etapa 1: Consulta Climática
1. Digite o nome do município (ex: "Rio de Janeiro")
2. Clique em "Consultar Clima"
3. O sistema buscará dados dos últimos 7 dias
<div align="center">
    <img src="assets/etapa_1.png" alt="Etapa 1" width="600">
</div>

### Etapa 2: Análise dos Dados
1. Visualize o mapa e edite os dados coletados
2. Confirme os parâmetros preenchidos automaticamente
3. Clique em "Classificar Risco"
<div align="center">
    <img src="assets/etapa_2.png" alt="Etapa 2" width="600">
</div>

### Etapa 3: Classificação de risco
1. Visualize o resultado em patamares `Baixo`, `Médio` e `Alto`
2. Revise os dados utilizados
3. Inicie uma nova consulta se necessário
<div align="center">
    <img src="assets/etapa_3.png" alt="Etapa 3" width="600">
</div>

<br>

### ⚠️ **Aviso:**
> Este sistema é uma ferramenta de apoio à decisão baseada em dados climáticos de escopo simplificado. Para decisões de saúde pública, consulte sempre órgãos oficiais competentes.