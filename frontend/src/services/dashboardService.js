/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * DASHBOARD SERVICE — API Calls para Dashboard
 * ═══════════════════════════════════════════════════════════════════════════════
 * Serviço para consumir endpoints do Dashboard da API Backend
 */

import api from './api';

// ═══════════════════════════════════════════════════════════════════════════════
// DASHBOARD SERVICE
// ═══════════════════════════════════════════════════════════════════════════════

export const dashboardService = {
  // ═════════════════════════════════════════════════════════════════════════════
  // GET /api/dashboard
  // ═════════════════════════════════════════════════════════════════════════════
  /**
   * Buscar dashboard executivo completo
   * @returns {Promise<Object>} Dashboard data com KPIs, alerts count, insights count
   * 
   * Response example:
   * {
   *   kpis: {
   *     revenue_today: 45200.00,
   *     revenue_change: 12.5,
   *     cac_average: 52.00,
   *     cac_change: -8.3,
   *     roas_average: 3.8,
   *     roas_change: 5.2,
   *     nps_average: 64,
   *     nps_change: 0.0
   *   },
   *   alerts_count: 3,
   *   insights_count: 5,
   *   tenants: [...]
   * }
   */
  async getDashboard() {
    try {
      console.log('📊 Buscando dashboard...');
      const response = await api.get('/api/dashboard');
      console.log('✅ Dashboard recebido:', response);
      return response;
    } catch (error) {
      console.error('❌ Erro ao buscar dashboard:', error);
      throw error;
    }
  },

  // ═════════════════════════════════════════════════════════════════════════════
  // GET /api/alerts
  // ═════════════════════════════════════════════════════════════════════════════
  /**
   * Buscar alertas críticos
   * @param {string|null} severity - Filtrar por severidade (critical, high, medium, low)
   * @param {number} limit - Limite de resultados (default: 20)
   * @returns {Promise<Array>} Lista de alertas
   * 
   * Response example:
   * [
   *   {
   *     id: "alert-001",
   *     tenant_name: "Empresa XYZ",
   *     metric_key: "cac",
   *     metric_value: 65.0,
   *     expected_value: 30.0,
   *     z_score: 3.5,
   *     severity: "critical",
   *     status: "new",
   *     detected_at: "2026-03-02T09:15:00"
   *   }
   * ]
   */
  async getAlerts(severity = null, limit = 20) {
    try {
      const params = { limit };
      if (severity) {
        params.severity = severity;
      }

      console.log('🚨 Buscando alertas...', { severity, limit });
      const response = await api.get('/api/alerts', { params });
      console.log('✅ Alertas recebidos:', response.length);
      return response;
    } catch (error) {
      console.error('❌ Erro ao buscar alertas:', error);
      throw error;
    }
  },

  // ═════════════════════════════════════════════════════════════════════════════
  // GET /api/insights
  // ═════════════════════════════════════════════════════════════════════════════
  /**
   * Buscar insights da IA
   * @param {number} limit - Limite de resultados (default: 10)
   * @returns {Promise<Array>} Lista de insights
   * 
   * Response example:
   * [
   *   {
   *     id: "insight-001",
   *     tenant_name: "Empresa XYZ",
   *     context: "CAC 120% acima do benchmark",
   *     ai_response: "Recomenda-se otimizar campanhas...",
   *     confidence_score: 0.87,
   *     source_model: "llama-3.1-70b",
   *     created_at: "2026-03-02T09:20:00"
   *   }
   * ]
   */
  async getInsights(limit = 10) {
    try {
      console.log('🤖 Buscando insights...', { limit });
      const response = await api.get('/api/insights', { params: { limit } });
      console.log('✅ Insights recebidos:', response.length);
      return response;
    } catch (error) {
      console.error('❌ Erro ao buscar insights:', error);
      throw error;
    }
  },

  // ═════════════════════════════════════════════════════════════════════════════
  // GET /api/channels/performance
  // ═════════════════════════════════════════════════════════════════════════════
  /**
   * Buscar performance por canal
   * @returns {Promise<Array>} Performance de canais
   * 
   * Response example:
   * [
   *   {
   *     channel: "Google Ads",
   *     spend: 5000,
   *     revenue: 26000,
   *     roas: 5.2,
   *     ctr: 4.5,
   *     status: "good"
   *   }
   * ]
   */
  async getChannelsPerformance() {
    try {
      console.log('📈 Buscando performance por canal...');
      const response = await api.get('/api/channels/performance');
      console.log('✅ Performance recebida:', response.length, 'canais');
      return response;
    } catch (error) {
      console.error('❌ Erro ao buscar performance:', error);
      throw error;
    }
  },

  // ═════════════════════════════════════════════════════════════════════════════
  // POST /api/alerts/{id}/acknowledge
  // ═════════════════════════════════════════════════════════════════════════════
  /**
   * Reconhecer alerta (marcar como visualizado)
   * @param {string} alertId - ID do alerta
   * @returns {Promise<Object>} Resultado da operação
   * 
   * Response example:
   * {
   *   status: "success",
   *   message: "Alert acknowledged"
   * }
   */
  async acknowledgeAlert(alertId) {
    try {
      console.log('✅ Reconhecendo alerta:', alertId);
      const response = await api.post(`/api/alerts/${alertId}/acknowledge`);
      console.log('✅ Alerta reconhecido:', alertId);
      return response;
    } catch (error) {
      console.error('❌ Erro ao reconhecer alerta:', alertId, error);
      throw error;
    }
  },

  // ═════════════════════════════════════════════════════════════════════════════
  // WEBSOCKET /ws/notifications (Future)
  // ═════════════════════════════════════════════════════════════════════════════
  /**
   * Conectar WebSocket para notificações em tempo real
   * @param {Function} onMessage - Callback para mensagens recebidas
   * @returns {WebSocket} WebSocket connection
   * 
   * Usage:
   * const ws = dashboardService.connectWebSocket((data) => {
   *   console.log('Nova notificação:', data);
   * });
   */
  connectWebSocket(onMessage) {
    const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8088/ws/notifications';

    console.log('🔌 Conectando WebSocket...', WS_URL);
    const ws = new WebSocket(WS_URL);

    ws.onopen = () => {
      console.log('✅ WebSocket conectado');
    };

    ws.onmessage = (event) => {
      console.log('📨 Mensagem recebida:', event.data);
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (error) {
        console.error('❌ Erro ao parsear mensagem:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('❌ WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('🔌 WebSocket desconectado');
      // Auto-reconnect after 5 seconds
      setTimeout(() => {
        console.log('🔄 Tentando reconectar...');
        this.connectWebSocket(onMessage);
      }, 5000);
    };

    return ws;
  },
};

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT DEFAULT
// ═══════════════════════════════════════════════════════════════════════════════

export default dashboardService;
