// Estado da aplicação
let currentStep = 1;
let climaData = null;
let map = null; // Adicionar variável do mapa

// Base URL da API
const API_BASE_URL = window.location.origin;

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Event listeners
    document.getElementById('climaForm').addEventListener('submit', consultarClima);
    document.getElementById('dengueForm').addEventListener('submit', classificarRisco);
    
    // Definir semana atual do ano
    const currentWeek = getCurrentWeek();
    document.getElementById('semana').value = currentWeek;
}

function getCurrentWeek() {
    const now = new Date();
    const start = new Date(now.getFullYear(), 0, 1);
    const diff = now - start + (start.getTimezoneOffset() - now.getTimezoneOffset()) * 60 * 1000;
    const oneWeek = 1000 * 60 * 60 * 24 * 7;
    return Math.floor(diff / oneWeek) + 1;
}

async function consultarClima(event) {
    event.preventDefault();
    
    const municipio = document.getElementById('municipio').value.trim();
    if (!municipio) {
        showError('Por favor, digite o nome do município.', 'climaError');
        return;
    }

    hideError('climaError');
    showLoading('climaLoading');
    
    try {
        const response = await fetch(`${API_BASE_URL}/clima-historico?nome=${encodeURIComponent(municipio)}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Erro ao consultar clima');
        }

        climaData = data;
        processarDadosClima(data);
        avancarEtapa(2);

    } catch (error) {
        console.error('Erro ao consultar clima:', error);
        showError(`Erro ao consultar clima: ${error.message}`, 'climaError');
    } finally {
        hideLoading('climaLoading');
    }
}

// Processar dados do clima e preencher formulário
function processarDadosClima(data) {
    // Exibir informações do clima
    const climaInfo = document.getElementById('climaInfo');
    climaInfo.innerHTML = `
        <div class="clima-summary">
            <h4>📍 ${data.municipio}, ${data.regiao} - ${data.pais}</h4>
            <p><strong>Período:</strong> ${formatDate(data.data_inicio)} a ${formatDate(data.data_fim)}</p>
            
            <div class="clima-details">
                <div class="clima-item">
                    <div class="value">${data.media_temp_min}°C</div>
                    <div class="label">Temp. Mín. Média</div>
                </div>
                <div class="clima-item">
                    <div class="value">${data.media_temp_max}°C</div>
                    <div class="label">Temp. Máx. Média</div>
                </div>
                <div class="clima-item">
                    <div class="value">${data.media_precip_total}mm</div>
                    <div class="label">Precip. Média</div>
                </div>
                <div class="clima-item">
                    <div class="value">${data.media_umidade_med}%</div>
                    <div class="label">Umidade Média</div>
                </div>
                <div class="clima-item">
                    <div class="value">${data.dias_chuvosos}</div>
                    <div class="label">Dias Chuvosos</div>
                </div>
            </div>
        </div>
    `;

    // Calcular faixa térmica (diferença entre máxima e mínima)
    const faixa_termica = (data.media_temp_max - data.media_temp_min).toFixed(2);

    // Preencher formulário automaticamente e tornar campos editáveis
    document.getElementById('temp_min').value = data.media_temp_min;
    document.getElementById('temp_min').removeAttribute('readonly');
    
    document.getElementById('temp_med').value = data.media_temp_med;
    document.getElementById('temp_med').removeAttribute('readonly');
    
    document.getElementById('temp_max').value = data.media_temp_max;
    document.getElementById('temp_max').removeAttribute('readonly');
    
    document.getElementById('precip_med').value = data.media_precip_total;
    document.getElementById('precip_med').removeAttribute('readonly');
    
    document.getElementById('umidade_med').value = data.media_umidade_med;
    document.getElementById('umidade_med').removeAttribute('readonly');
    
    document.getElementById('faixa_termica').value = faixa_termica;
    
    document.getElementById('dias_chuvosos').value = data.dias_chuvosos;
    document.getElementById('dias_chuvosos').removeAttribute('readonly');

    // Inicializar mapa com a localização usando coordenadas da API
    initializeMap(data.municipio, data.regiao, data.pais, data.latitude, data.longitude);
    
    // Adicionar listeners para recalcular faixa térmica automaticamente
    setupFaixaTermicaListeners();
}

// Função para inicializar o mapa
async function initializeMap(municipio, regiao, pais, latitude = null, longitude = null) {
    try {
        let coords;
        
        // Se já temos coordenadas da API, usar diretamente
        if (latitude !== null && longitude !== null) {
            coords = { lat: latitude, lon: longitude };
        } else {
            // Fallback: buscar coordenadas usando geocodificação
            coords = await getCoordinates(`${municipio}, ${regiao}, ${pais}`);
        }
        
        // Destruir mapa existente se houver
        if (map) {
            map.remove();
        }

        // Criar novo mapa
        map = L.map('map').setView([coords.lat, coords.lon], 10);

        // Adicionar camada do mapa
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Adicionar marcador
        const marker = L.marker([coords.lat, coords.lon]).addTo(map);
        
        // Popup personalizado compacto
        marker.bindPopup(`
            <div class="custom-popup">
                <h5>📍 ${municipio}</h5>
                <small>Lat:${coords.lat.toFixed(3)}, Long:${coords.lon.toFixed(3)}</small>
            </div>
        `, {
            maxWidth: 200,
            className: 'compact-popup'
        });

        // Ajustar visualização
        setTimeout(() => {
            map.invalidateSize();
        }, 100);

    } catch (error) {
        console.error('Erro ao carregar mapa:', error);
        // Fallback: mapa centralizado no Brasil
        if (map) {
            map.remove();
        }
        map = L.map('map').setView([-14.235004, -51.92528], 4);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
        
        // Adicionar marcador genérico
        L.marker([-14.235004, -51.92528]).addTo(map)
            .bindPopup(`
                <div class="custom-popup">
                    <h5>📍 ${municipio}</h5>
                    <small>Localização aproximada</small>
                </div>
            `, {
                maxWidth: 200,
                className: 'compact-popup'
            });
    }
}

// Função para obter coordenadas usando Nominatim (OpenStreetMap)
async function getCoordinates(location) {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(location)}&limit=1`;
    
    try {
        const response = await fetch(url);
        const data = await response.json();
        
        if (data && data.length > 0) {
            return {
                lat: parseFloat(data[0].lat),
                lon: parseFloat(data[0].lon)
            };
        } else {
            throw new Error('Localização não encontrada');
        }
    } catch (error) {
        console.error('Erro ao buscar coordenadas:', error);
        // Coordenadas padrão do Brasil
        return { lat: -14.235004, lon: -51.92528 };
    }
}

// Função para classificar risco de dengue
async function classificarRisco(event) {
    event.preventDefault();

    hideError('classificacaoError');
    showLoading('classificacaoLoading');

    const formData = new FormData(document.getElementById('dengueForm'));
    const url = `${API_BASE_URL}/classificador-dengue`;
    const options = {
        method: 'POST',
        body: formData,
    };

    try {
        console.log('Dados enviados para classificação:', formData);
        const response = await fetch(url, options);
        const data = await response.json();

        if (!response.ok) {
            console.error('Erro na resposta da API:', data);
            throw new Error(data.message || 'Erro ao classificar risco');
        }

        exibirResultado(data);
        avancarEtapa(3);

    } catch (error) {
        console.error('Erro ao classificar risco:', error);
        showError(`Erro ao classificar risco: ${error.message}`, 'classificacaoError');
    } finally {
        hideLoading('classificacaoLoading');
    }
}

// Exibir resultado da classificação
function exibirResultado(data) {
    const resultado = document.getElementById('resultadoClassificacao');
    
    let riscoClass = '';
    let riscoIcon = '';
    let riscoNivel = '';
    
    switch (data.risco_dengue) {
        case 0:
            riscoClass = 'baixo';
            riscoIcon = '✅';
            riscoNivel = 'Baixo';
            break;
        case 1:
            riscoClass = 'medio';
            riscoIcon = '⚠️';
            riscoNivel = 'Médio';
            break;
        case 2:
            riscoClass = 'alto';
            riscoIcon = '🚨';
            riscoNivel = 'Alto';
            break;
        default:
            riscoClass = 'erro';
            riscoIcon = '❌';
            riscoNivel = 'Erro';
    }

    resultado.innerHTML = `
        <div class="resultado-risco ${riscoClass}">
            <div class="risco-icone">${riscoIcon}</div>
            <div class="risco-nivel">Risco ${riscoNivel}</div>
            <div class="risco-descricao">${data.descricao}</div>
        </div>
        
        <div class="clima-summary">
            <h4>📊 Dados Utilizados na Classificação em ${climaData.municipio}, ${climaData.regiao}, ${climaData.regiao, climaData.pais}</h4>
            <div class="clima-details">
                <div class="clima-item">
                    <div class="value">Sem. ${document.getElementById('semana').value}</div>
                    <div class="label">Semana do Ano</div>
                </div>
                <div class="clima-item">
                    <div class="value">${document.getElementById('temp_min').value}°C</div>
                    <div class="label">Temp. Mínima</div>
                </div>
                <div class="clima-item">
                    <div class="value">${document.getElementById('temp_med').value}°C</div>
                    <div class="label">Temp. Média</div>
                </div>
                <div class="clima-item">
                    <div class="value">${document.getElementById('temp_max').value}°C</div>
                    <div class="label">Temp. Máxima</div>
                </div>
                <div class="clima-item">
                    <div class="value">${document.getElementById('precip_med').value}mm</div>
                    <div class="label">Precipitação</div>
                </div>
                <div class="clima-item">
                    <div class="value">${document.getElementById('umidade_med').value}%</div>
                    <div class="label">Umidade</div>
                </div>
                <div class="clima-item">
                    <div class="value">${document.getElementById('faixa_termica').value}°C</div>
                    <div class="label">Faixa Térmica</div>
                </div>
                <div class="clima-item">
                    <div class="value">${document.getElementById('dias_chuvosos').value}</div>
                    <div class="label">Dias Chuvosos</div>
                </div>
            </div>
        </div>
    `;
}

// Navegação entre etapas
function avancarEtapa(step) {
    // Ocultar etapa atual
    document.getElementById(`step${currentStep}`).style.display = 'none';
    
    // Atualizar progress bar
    document.querySelector(`[data-step="${currentStep}"]`).classList.remove('active');
    document.querySelector(`[data-step="${currentStep}"]`).classList.add('completed');
    
    // Mostrar nova etapa
    currentStep = step;
    document.getElementById(`step${currentStep}`).style.display = 'block';
    document.querySelector(`[data-step="${currentStep}"]`).classList.add('active');
    
    // Redimensionar mapa se estivermos na etapa 2
    if (step === 2 && map) {
        setTimeout(() => {
            map.invalidateSize();
        }, 100);
    }
    
    // Scroll para o topo
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function voltarEtapa(step) {
    // Ocultar etapa atual
    document.getElementById(`step${currentStep}`).style.display = 'none';
    document.querySelector(`[data-step="${currentStep}"]`).classList.remove('active');
    
    // Mostrar etapa anterior
    currentStep = step;
    document.getElementById(`step${currentStep}`).style.display = 'block';
    document.querySelector(`[data-step="${currentStep}"]`).classList.add('active');
    
    // Atualizar progress bar - remover completed das etapas posteriores
    for (let i = step + 1; i <= 3; i++) {
        document.querySelector(`[data-step="${i}"]`).classList.remove('completed');
    }
    
    // Redimensionar mapa se estivermos voltando para a etapa 2
    if (step === 2 && map) {
        setTimeout(() => {
            map.invalidateSize();
        }, 100);
    }
    
    // Scroll para o topo
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function novaConsulta() {
    // Reset do formulário
    document.getElementById('climaForm').reset();
    document.getElementById('dengueForm').reset();
    
    // Reset das variáveis
    climaData = null;
    
    // Limpar conteúdo
    document.getElementById('climaInfo').innerHTML = '';
    document.getElementById('resultadoClassificacao').innerHTML = '';
    
    // Restaurar atributo readonly nos campos
    document.getElementById('temp_min').setAttribute('readonly', 'readonly');
    document.getElementById('temp_med').setAttribute('readonly', 'readonly');
    document.getElementById('temp_max').setAttribute('readonly', 'readonly');
    document.getElementById('precip_med').setAttribute('readonly', 'readonly');
    document.getElementById('umidade_med').setAttribute('readonly', 'readonly');
    document.getElementById('faixa_termica').setAttribute('readonly', 'readonly');
    document.getElementById('dias_chuvosos').setAttribute('readonly', 'readonly');
    
    // Destruir mapa
    if (map) {
        map.remove();
        map = null;
    }
    
    // Reset dos erros e loading
    hideError('climaError');
    hideError('classificacaoError');
    hideLoading('climaLoading');
    hideLoading('classificacaoLoading');
    
    // Definir semana atual novamente
    const currentWeek = getCurrentWeek();
    document.getElementById('semana').value = currentWeek;
    
    // Voltar para etapa 1
    voltarEtapa(1);
    
    // Reset progress bar
    document.querySelectorAll('.progress-step').forEach(step => {
        step.classList.remove('active', 'completed');
    });
    document.querySelector('[data-step="1"]').classList.add('active');
}

// Funções auxiliares
function showLoading(elementId) {
    document.getElementById(elementId).style.display = 'block';
}

function hideLoading(elementId) {
    document.getElementById(elementId).style.display = 'none';
}

function showError(message, elementId) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

function hideError(elementId) {
    document.getElementById(elementId).style.display = 'none';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

// Função para validar formulário antes do envio
function validateForm(formData) {
    for (const [key, value] of Object.entries(formData)) {
        if (value === null || value === undefined || value === '') {
            throw new Error(`Campo ${key} é obrigatório`);
        }
        if (isNaN(value)) {
            throw new Error(`Campo ${key} deve ser um número válido`);
        }
    }
    return true;
}

// Função para configurar listeners de recálculo da faixa térmica
function setupFaixaTermicaListeners() {
    const tempMinInput = document.getElementById('temp_min');
    const tempMaxInput = document.getElementById('temp_max');
    const faixaTermicaInput = document.getElementById('faixa_termica');
    
    function recalcularFaixaTermica() {
        const tempMin = parseFloat(tempMinInput.value) || 0;
        const tempMax = parseFloat(tempMaxInput.value) || 0;
        const faixaTermica = (tempMax - tempMin).toFixed(2);
        faixaTermicaInput.value = faixaTermica;
    }
    
    tempMinInput.addEventListener('input', recalcularFaixaTermica);
    tempMaxInput.addEventListener('input', recalcularFaixaTermica);
}
