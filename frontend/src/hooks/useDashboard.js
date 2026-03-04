/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * USE DASHBOARD — Custom React Hook
 * ═══════════════════════════════════════════════════════════════════════════════
 * Hook customizado para gerenciar estado do Dashboard com dados reais da API
 */

import { useState, useEffect, useCallback } from 'react';
import { dashboardService } from '../services/dashboardService';

// ═══════════════════════════════════════════════════════════════════════════════
// USE DASHBOARD HOOK
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Hook para buscar e gerenciar dados do Dashboard
 * @param {number} refreshInterval - Intervalo de refresh em ms (default: 300000 = 5 min)
 * @returns {Object} Estado e funções do dashboard
 * 
 * Usage:
 * const { dashboard, alerts, insights, channels, loading, error, lastUpdate, refresh, acknowledgeAlert } = useDashboard();
 */
export function useDashboard(refreshInterval = 300000) {
  // ═════════════════════════════════════════════════════════════════════════════
  // STATE
  // ═════════════════════════════════════════════════════════════════════════════

  const [dashboard, setDashboard] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [insights, setInsights] = useState([]);
  const [channels, setChannels] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);

  // WebSocket connection (opcional)
  const [wsConnected, setWsConnected] = useState(false);

  // ═════════════════════════════════════════════════════════════════════════════
  // FETCH DATA
  // ═════════════════════════════════════════════════════════════════════════════

  /**
   * Buscar todos os dados do dashboard
   */
  const fetchData = useCallback(async () => {
    try {
      console.log('🔄 Buscando dados do dashboard...');
      setLoading(true);
      setError(null);

      // Buscar todos os dados em paralelo (Promise.all)
      const [dashboardData, alertsData, insightsData, channelsData] = await Promise.all([
        dashboardService.getDashboard(),
        dashboardService.getAlerts(),
        dashboardService.getInsights(),
        dashboardService.getChannelsPerformance(),
      ]);

      // Atualizar estado com dados reais da API
      setDashboard(dashboardData);
      setAlerts(alertsData);
      setInsights(insightsData);
      setChannels(channelsData);
      setLastUpdate(new Date());

      console.log('✅ Dashboard atualizado:', {
        kpis: dashboardData?.kpis,
        alerts: alertsData?.length,
        insights: insightsData?.length,
        channels: channelsData?.length,
      });
    } catch (err) {
      console.error('❌ Erro ao buscar dados:', err);
      setError(err.message || 'Erro ao carregar dados do backend');
    } finally {
      setLoading(false);
    }
  }, []);

  // ═════════════════════════════════════════════════════════════════════════════
  // AUTO-REFRESH
  // ═════════════════════════════════════════════════════════════════════════════

  useEffect(() => {
    // Buscar dados imediatamente ao montar o componente
    fetchData();

    // Configurar auto-refresh
    const interval = setInterval(fetchData, refreshInterval);

    // Cleanup: limpar intervalo ao desmontar
    return () => {
      clearInterval(interval);
      console.log('🧹 Limpando intervalo de refresh');
    };
  }, [fetchData, refreshInterval]);

  // ═════════════════════════════════════════════════════════════════════════════
  // WEBSOCKET (OPCIONAL - TEMPO REAL)
  // ═════════════════════════════════════════════════════════════════════════════

  useEffect(() => {
    // Conectar WebSocket para notificações em tempo real
    let ws = null;

    try {
      ws = dashboardService.connectWebSocket((data) => {
        console.log('📨 Notificação em tempo real:', data);

        // Atualizar dados quando receber notificação
        if (data.type === 'new_alert') {
          setAlerts((prev) => [data.alert, ...prev]);
        }

        if (data.type === 'new_insight') {
          setInsights((prev) => [data.insight, ...prev]);
        }

        if (data.type === 'dashboard_updated') {
          setDashboard(data.dashboard);
        }
      });

      setWsConnected(true);
    } catch (err) {
      console.error('❌ Erro ao conectar WebSocket:', err);
      setWsConnected(false);
    }

    // Cleanup: desconectar WebSocket ao desmontar
    return () => {
      if (ws) {
        ws.close();
        console.log('🔌 WebSocket desconectado');
      }
    };
  }, []);

  // ═════════════════════════════════════════════════════════════════════════════
  // ACKNOWLEDGE ALERT
  // ═════════════════════════════════════════════════════════════════════════════

  /**
   * Reconhecer alerta (marcar como visualizado)
   * @param {string} alertId - ID do alerta
   */
  const acknowledgeAlert = async (alertId) => {
    try {
      console.log('✅ Reconhecendo alerta:', alertId);
      await dashboardService.acknowledgeAlert(alertId);

      // Remover alerta da lista localmente (otimista)
      setAlerts((prev) => prev.filter((a) => a.id !== alertId));

      console.log('✅ Alerta removido da lista:', alertId);
    } catch (err) {
      console.error('❌ Erro ao reconhecer alerta:', alertId, err);
      // Não remover da lista se falhou
      throw err;
    }
  };

  // ═════════════════════════════════════════════════════════════════════════════
  // RETURN
  // ═════════════════════════════════════════════════════════════════════════════

  return {
    // Dados
    dashboard,
    alerts,
    insights,
    channels,

    // Estado
    loading,
    error,
    lastUpdate,
    wsConnected,

    // Funções
    refresh: fetchData, // Refresh manual
    acknowledgeAlert, // Reconhecer alerta
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT DEFAULT
// ═══════════════════════════════════════════════════════════════════════════════

export default useDashboard;
