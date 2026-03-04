/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * API CONFIGURATION — Axios HTTP Client
 * ═══════════════════════════════════════════════════════════════════════════════
 * Configuração centralizada do Axios para consumir API do Backend
 */

import axios from 'axios';

// URL da API Backend
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8088';

// Criar instância do Axios
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 segundos
  withCredentials: false, // Mudar para true quando implementar autenticação
});

// ═══════════════════════════════════════════════════════════════════════════════
// INTERCEPTORS
// ═══════════════════════════════════════════════════════════════════════════════

// Interceptor para Requests (antes de enviar)
api.interceptors.request.use(
  (config) => {
    // Future: Adicionar token de autenticação
    // const token = localStorage.getItem('auth_token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }

    // Log de requests (debug)
    console.log(`📡 API Request: ${config.method?.toUpperCase()} ${config.url}`);

    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Interceptor para Responses (depois de receber)
api.interceptors.response.use(
  (response) => {
    // Log de response (debug)
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response.data;
  },
  (error) => {
    // Error handling centralizado
    const errorMessage = error.response?.data?.detail || error.message || 'Erro desconhecido';

    console.error('❌ API Error:', {
      url: error.config?.url,
      status: error.response?.status,
      message: errorMessage,
    });

    // Error codes
    if (error.response?.status === 401) {
      console.error('🔒 Não autorizado - fazer login');
      // Future: Redirecionar para login
      // localStorage.removeItem('auth_token');
      // window.location.href = '/login';
    }

    if (error.response?.status === 403) {
      console.error('🚫 Acesso proibido');
    }

    if (error.response?.status === 404) {
      console.error('🔍 Recurso não encontrado');
    }

    if (error.response?.status === 500) {
      console.error('💥 Erro interno do servidor');
    }

    if (error.code === 'ECONNREFUSED') {
      console.error('🔌 Backend não está rodando em', API_URL);
    }

    if (error.code === 'ECONNABORTED') {
      console.error('⏱️ Request timeout (30s)');
    }

    return Promise.reject(new Error(errorMessage));
  }
);

// ═══════════════════════════════════════════════════════════════════════════════
// HEALTH CHECK
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Verifica se a API está online
 * @returns {Promise<Object>} Status da API
 */
export async function checkHealth() {
  try {
    const response = await axios.get(`${API_URL}/health`, {
      timeout: 5000,
    });
    return { online: true, data: response.data };
  } catch (error) {
    return { online: false, error: error.message };
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export default api;
