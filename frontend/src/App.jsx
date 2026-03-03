import { useState, useEffect } from 'react'
import { 
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, 
  Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell 
} from 'recharts'
import { 
  TrendingUp, TrendingDown, AlertTriangle, Brain, 
  DollarSign, Users, Activity, ArrowUpRight, ArrowDownRight 
} from 'lucide-react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

function App() {
  const [dashboard, setDashboard] = useState(null)
  const [alerts, setAlerts] = useState([])
  const [insights, setInsights] = useState([])
  const [channels, setChannels] = useState([])
  const [loading, setLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState(new Date())

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 300000) // Atualiza a cada 5 min
    return () => clearInterval(interval)
  }, [])

  const fetchData = async () => {
    try {
      const [dashboardRes, alertsRes, insightsRes, channelsRes] = await Promise.all([
        axios.get(`${API_URL}/api/dashboard`),
        axios.get(`${API_URL}/api/alerts`),
        axios.get(`${API_URL}/api/insights`),
        axios.get(`${API_URL}/api/channels/performance`)
      ])

      setDashboard(dashboardRes.data)
      setAlerts(alertsRes.data.slice(0, 5))
      setInsights(insightsRes.data.slice(0, 3))
      setChannels(channelsRes.data)
      setLoading(false)
      setLastUpdate(new Date())
    } catch (error) {
      console.error('Erro ao buscar dados:', error)
      setLoading(false)
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return '#ef4444'
      case 'high': return '#f97316'
      case 'medium': return '#eab308'
      default: return '#6b7280'
    }
  }

  const getChannelStatus = (roas) => {
    if (roas >= 4) return { color: '#22c55e', label: 'Excelente' }
    if (roas >= 2.5) return { color: '#eab308', label: 'Bom' }
    return { color: '#ef4444', label: 'Crítico' }
  }

  if (loading) {
    return (
      <div style={styles.loading}>
        <Activity size={48} color="#3b82f6" />
        <h2>Carregando CMO 360°...</h2>
      </div>
    )
  }

  return (
    <div style={styles.container}>
      {/* Header */}
      <header style={styles.header}>
        <div>
          <h1 style={styles.title}>🎯 CMO 360° — Command Center</h1>
          <p style={styles.subtitle}>
            Última atualização: {lastUpdate.toLocaleTimeString('pt-BR')}
          </p>
        </div>
        <button onClick={fetchData} style={styles.refreshButton}>
          🔄 Atualizar
        </button>
      </header>

      {/* KPIs */}
      <div style={styles.kpisGrid}>
        <KpiCard
          icon={DollarSign}
          title="Receita Hoje"
          value={`R$ ${dashboard?.kpis.revenue_today.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
          change={dashboard?.kpis.revenue_change}
          color="#22c55e"
        />
        <KpiCard
          icon={Users}
          title="CAC Médio"
          value={`R$ ${dashboard?.kpis.cac_average.toFixed(2)}`}
          change={dashboard?.kpis.cac_change}
          color="#ef4444"
        />
        <KpiCard
          icon={TrendingUp}
          title="ROAS Médio"
          value={`${dashboard?.kpis.roas_average.toFixed(1)}x`}
          change={dashboard?.kpis.roas_change}
          color="#3b82f6"
        />
        <KpiCard
          icon={Activity}
          title="NPS"
          value={dashboard?.kpis.nps_average.toString()}
          change={dashboard?.kpis.nps_change}
          color="#8b5cf6"
        />
      </div>

      {/* Alertas e Insights */}
      <div style={styles.contentGrid}>
        {/* Alertas */}
        <div style={styles.card}>
          <div style={styles.cardHeader}>
            <h2 style={styles.cardTitle}>
              <AlertTriangle size={20} color="#ef4444" />
              🚨 Alertas Críticos ({alerts.length})
            </h2>
          </div>
          <div style={styles.alertsList}>
            {alerts.length === 0 ? (
              <p style={styles.emptyState}>✅ Nenhum alerta crítico</p>
            ) : (
              alerts.map(alert => (
                <div key={alert.id} style={styles.alertItem}>
                  <div style={styles.alertHeader}>
                    <span style={styles.alertSeverity}>
                      🔴 {alert.metric_key.replace('_', ' ').title()}
                    </span>
                    <span style={styles.alertTenant}>{alert.tenant_name}</span>
                  </div>
                  <div style={styles.alertBody}>
                    <span>Valor: <strong>{alert.metric_value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</strong></span>
                    {alert.expected_value && (
                      <span>Esperado: <strong>{alert.expected_value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</strong></span>
                    )}
                    {alert.z_score && (
                      <span>Z-Score: <strong>{alert.z_score.toFixed(2)}</strong></span>
                    )}
                  </div>
                  <div style={styles.alertFooter}>
                    <span style={styles.alertTime}>
                      {new Date(alert.detected_at).toLocaleString('pt-BR')}
                    </span>
                    <button style={styles.alertAction}>Ver Detalhes</button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Insights */}
        <div style={styles.card}>
          <div style={styles.cardHeader}>
            <h2 style={styles.cardTitle}>
              <Brain size={20} color="#8b5cf6" />
              🤖 Insights da IA ({insights.length})
            </h2>
          </div>
          <div style={styles.insightsList}>
            {insights.length === 0 ? (
              <p style={styles.emptyState}>✅ Sem insights novos</p>
            ) : (
              insights.map(insight => (
                <div key={insight.id} style={styles.insightItem}>
                  <div style={styles.insightHeader}>
                    <span style={styles.insightTenant}>{insight.tenant_name}</span>
                    {insight.confidence_score && (
                      <span style={styles.confidence}>
                        {(insight.confidence_score * 100).toFixed(0)}% confiança
                      </span>
                    )}
                  </div>
                  <p style={styles.insightContext}>{insight.context}</p>
                  <div style={styles.insightFooter}>
                    <span style={styles.insightTime}>
                      {new Date(insight.created_at).toLocaleString('pt-BR')}
                    </span>
                    <button style={styles.insightAction}>Ver Análise</button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Performance por Canal */}
      <div style={styles.card}>
        <div style={styles.cardHeader}>
          <h2 style={styles.cardTitle}>
            <TrendingUp size={20} color="#3b82f6" />
            📈 Performance por Canal
          </h2>
        </div>
        <div style={styles.tableContainer}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>Canal</th>
                <th style={styles.th}>Spend</th>
                <th style={styles.th}>Receita</th>
                <th style={styles.th}>ROAS</th>
                <th style={styles.th}>CTR</th>
                <th style={styles.th}>Status</th>
              </tr>
            </thead>
            <tbody>
              {channels.map((channel, index) => {
                const status = getChannelStatus(channel.roas)
                return (
                  <tr key={index}>
                    <td style={styles.td}>{channel.channel}</td>
                    <td style={styles.td}>R$ {channel.spend.toLocaleString('pt-BR')}</td>
                    <td style={styles.td}>R$ {channel.revenue.toLocaleString('pt-BR')}</td>
                    <td style={styles.td}>{channel.roas.toFixed(2)}x</td>
                    <td style={styles.td}>{channel.ctr.toFixed(2)}%</td>
                    <td style={styles.td}>
                      <span style={{ ...styles.statusBadge, backgroundColor: status.color }}>
                        {status.label}
                      </span>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Footer */}
      <footer style={styles.footer}>
        <p>CMO 360° Platform v1.0.0 • Powered by FastAPI + React</p>
      </footer>
    </div>
  )
}

// KPI Card Component
function KpiCard({ icon: Icon, title, value, change, color }) {
  const isPositive = change >= 0
  return (
    <div style={{ ...styles.kpiCard, borderLeft: `4px solid ${color}` }}>
      <div style={styles.kpiHeader}>
        <Icon size={24} color={color} />
        <span style={styles.kpiTitle}>{title}</span>
      </div>
      <div style={styles.kpiValue}>{value}</div>
      <div style={styles.kpiChange}>
        {isPositive ? (
          <ArrowUpRight size={16} color="#22c55e" />
        ) : (
          <ArrowDownRight size={16} color="#ef4444" />
        )}
        <span style={{ color: isPositive ? '#22c55e' : '#ef4444' }}>
          {change >= 0 ? '+' : ''}{change.toFixed(1)}%
        </span>
      </div>
    </div>
  )
}

// Styles
const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#f8fafc',
    padding: '20px'
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '30px',
    padding: '20px',
    backgroundColor: 'white',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
  },
  title: {
    fontSize: '28px',
    fontWeight: 'bold',
    color: '#1e293b',
    margin: '0 0 5px 0'
  },
  subtitle: {
    fontSize: '14px',
    color: '#64748b',
    margin: 0
  },
  refreshButton: {
    padding: '10px 20px',
    backgroundColor: '#3b82f6',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '500'
  },
  kpisGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
    marginBottom: '30px'
  },
  kpiCard: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
  },
  kpiHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    marginBottom: '10px'
  },
  kpiTitle: {
    fontSize: '14px',
    color: '#64748b',
    fontWeight: '500'
  },
  kpiValue: {
    fontSize: '28px',
    fontWeight: 'bold',
    color: '#1e293b',
    marginBottom: '5px'
  },
  kpiChange: {
    display: 'flex',
    alignItems: 'center',
    gap: '5px',
    fontSize: '14px',
    fontWeight: '500'
  },
  contentGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
    gap: '20px',
    marginBottom: '30px'
  },
  card: {
    backgroundColor: 'white',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    overflow: 'hidden'
  },
  cardHeader: {
    padding: '20px',
    borderBottom: '1px solid #e2e8f0'
  },
  cardTitle: {
    fontSize: '18px',
    fontWeight: '600',
    color: '#1e293b',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    margin: 0
  },
  alertsList: {
    padding: '20px'
  },
  alertItem: {
    padding: '15px',
    backgroundColor: '#fef2f2',
    borderRadius: '8px',
    marginBottom: '10px',
    border: '1px solid #fecaca'
  },
  alertHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '10px'
  },
  alertSeverity: {
    fontWeight: '600',
    color: '#ef4444'
  },
  alertTenant: {
    fontSize: '13px',
    color: '#64748b'
  },
  alertBody: {
    display: 'flex',
    gap: '20px',
    fontSize: '14px',
    color: '#475569',
    marginBottom: '10px'
  },
  alertFooter: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  },
  alertTime: {
    fontSize: '12px',
    color: '#94a3b8'
  },
  alertAction: {
    padding: '6px 12px',
    backgroundColor: '#ef4444',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '13px'
  },
  insightsList: {
    padding: '20px'
  },
  insightItem: {
    padding: '15px',
    backgroundColor: '#f5f3ff',
    borderRadius: '8px',
    marginBottom: '10px',
    border: '1px solid #ddd6fe'
  },
  insightHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '10px'
  },
  insightTenant: {
    fontWeight: '600',
    color: '#7c3aed'
  },
  confidence: {
    fontSize: '12px',
    color: '#9333ea',
    backgroundColor: '#f3e8ff',
    padding: '4px 8px',
    borderRadius: '4px'
  },
  insightContext: {
    fontSize: '14px',
    color: '#475569',
    marginBottom: '10px',
    lineHeight: '1.5'
  },
  insightFooter: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  },
  insightTime: {
    fontSize: '12px',
    color: '#94a3b8'
  },
  insightAction: {
    padding: '6px 12px',
    backgroundColor: '#8b5cf6',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '13px'
  },
  emptyState: {
    textAlign: 'center',
    color: '#64748b',
    padding: '40px 20px'
  },
  tableContainer: {
    overflowX: 'auto',
    padding: '20px'
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse'
  },
  th: {
    textAlign: 'left',
    padding: '12px',
    backgroundColor: '#f8fafc',
    fontWeight: '600',
    color: '#475569',
    borderBottom: '2px solid #e2e8f0'
  },
  td: {
    padding: '12px',
    borderBottom: '1px solid #e2e8f0',
    color: '#1e293b'
  },
  statusBadge: {
    padding: '4px 12px',
    borderRadius: '12px',
    fontSize: '12px',
    fontWeight: '500',
    color: 'white'
  },
  footer: {
    textAlign: 'center',
    padding: '20px',
    color: '#94a3b8',
    fontSize: '14px'
  },
  loading: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    gap: '20px'
  }
}

export default App
