/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * APP — CMO 360° Command Center (COM BGPattern)
 * ═══════════════════════════════════════════════════════════════════════════════
 * Aplicação principal do CMO 360° Frontend
 * Conectado com API Backend em http://localhost:8088
 * Com BGPattern para backgrounds decorativos
 */

import { useState } from 'react';
import {
  TrendingUp,
  AlertTriangle,
  Brain,
  DollarSign,
  Users,
  Activity,
  RefreshCw,
  XCircle,
  CheckCircle,
  Wifi,
  WifiOff,
  TrendingDown,
} from 'lucide-react';
import { useDashboard } from './hooks/useDashboard';
import { KPICard } from './components/KPICard';
import { BGPattern } from './components/ui/bg-pattern';
import './index.css';
// Assuming 'cn' utility is imported or defined elsewhere, e.g., from 'lib/utils'
import { cn } from '@/lib/utils';

// ═══════════════════════════════════════════════════════════════════════════════
// APP COMPONENT
// ═══════════════════════════════════════════════════════════════════════════════

function App() {
  const {
    dashboard,
    alerts,
    insights,
    channels,
    loading,
    error,
    lastUpdate,
    refresh,
    acknowledgeAlert,
    wsConnected,
  } = useDashboard(300000);

  const [acknowledging, setAcknowledging] = useState(null);

  // ═════════════════════════════════════════════════════════════════════════════
  // HANDLERS
  // ═════════════════════════════════════════════════════════════════════════════

  const handleAcknowledge = async (alertId) => {
    setAcknowledging(alertId);
    try {
      await acknowledgeAlert(alertId);
    } catch (err) {
      console.error('❌ Erro ao reconhecer alerta:', err);
    } finally {
      setAcknowledging(null);
    }
  };

  // ═════════════════════════════════════════════════════════════════════════════
  // HELPERS
  // ═════════════════════════════════════════════════════════════════════════════

  const formatCurrency = (val) =>
    val === 0 ? '--' : new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);

  const formatNumber = (val) => val === 0 ? '--' : val?.toLocaleString('pt-BR');

  // ═════════════════════════════════════════════════════════════════════════════
  // LOADING / ERROR RENDER (Simplified)
  // ═════════════════════════════════════════════════════════════════════════════

  if (loading && !dashboard) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="text-center animate-in fade-in duration-700">
          <Activity size={48} className="mx-auto mb-4 animate-pulse text-primary" />
          <h2 className="text-xl font-semibold opacity-70">Sincronizando Métrica Real...</h2>
        </div>
      </div>
    );
  }

  // ═════════════════════════════════════════════════════════════════════════════
  // MAIN RENDER
  // ═════════════════════════════════════════════════════════════════════════════

  const kpis = dashboard?.kpis || {};

  return (
    <div className="relative min-h-screen bg-background selection:bg-primary/20">
      <BGPattern
        variant="grid"
        mask="fade-y"
        size={24}
        fill="#b89b76"
        className="opacity-[0.05]"
      />

      {/* HEADER PREMIUM */}
      <header className="sticky top-0 z-50 border-b border-border/40 bg-background/80 backdrop-blur-xl">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="relative">
                <div className="absolute -inset-1 rounded-full bg-primary/20 blur animate-pulse" />
                <Brain className="relative text-primary" size={32} />
              </div>
              <div>
                <h1 className="text-2xl font-bold tracking-tight text-foreground font-serif">
                  CMO 360° <span className="text-primary/60 text-sm font-sans font-medium px-2 py-0.5 rounded-full border border-primary/20 ml-2">v7.0</span>
                </h1>
                <div className="flex items-center gap-2 text-[10px] uppercase tracking-widest text-muted-foreground mt-0.5">
                  <div className={`h-1.5 w-1.5 rounded-full ${wsConnected ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]' : 'bg-red-500'}`} />
                  {wsConnected ? 'Conectado em Tempo Real' : 'Conexão Offline'} •
                  Última: {lastUpdate?.toLocaleTimeString('pt-BR')}
                </div>
              </div>
            </div>

            <div className="flex items-center gap-4">
              {dashboard?.is_demo && (
                <div className="hidden md:flex items-center gap-2 px-3 py-1 bg-yellow-500/10 border border-yellow-500/20 rounded-lg text-yellow-600 text-xs font-semibold">
                  <AlertTriangle size={14} /> Modo Demonstração
                </div>
              )}
              <button
                onClick={refresh}
                className="flex items-center gap-2 rounded-full bg-primary/10 border border-primary/20 px-5 py-2 text-sm font-semibold text-primary transition-all hover:bg-primary hover:text-white"
              >
                <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
                {loading ? 'Sincronizando...' : 'Atualizar'}
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="relative z-10 container mx-auto px-6 py-10 space-y-12">

        {/* KPI GRID */}
        <section className="animate-in slide-in-from-bottom-4 duration-500">
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            <KPICard
              title="Receita Atribuída"
              value={formatCurrency(kpis.revenue?.value || 0)}
              change={kpis.revenue?.trend || 0}
              icon={DollarSign}
              color="#22c55e"
              lineage={kpis.revenue?.lineage}
            />
            <KPICard
              title="Ad Spend (Google/Meta)"
              value={formatCurrency(kpis.spend?.value || 0)}
              change={kpis.spend?.trend || 0}
              icon={Activity}
              color="#3b82f6"
              lineage={kpis.spend?.lineage}
            />
            <KPICard
              title="ROAS Geral"
              value={`${(kpis.roas?.value || 0).toFixed(2)}x`}
              change={kpis.roas?.trend || 0}
              icon={TrendingUp}
              color="#8b5cf6"
              lineage={kpis.roas?.lineage}
            />
            <KPICard
              title="CAC Médio"
              value={formatCurrency(kpis.cac?.value || 0)}
              change={kpis.cac?.trend || 0}
              icon={Users}
              color="#f43f5e"
              lineage={kpis.cac?.lineage}
            />
          </div>
        </section>

        {/* ALERTS & INSIGHTS */}
        <section className="grid gap-8 lg:grid-cols-5">
          <div className="lg:col-span-2 space-y-6">
            <h2 className="text-xs font-black uppercase tracking-[0.2em] text-muted-foreground flex items-center gap-2">
              <span className="h-1 w-1 bg-red-500 rounded-full" /> Auditoria de Saúde
            </h2>
            <div className="space-y-4">
              {alerts?.length > 0 ? alerts.map(alert => (
                <div key={alert.id} className="relative group overflow-hidden bg-card border border-border/40 p-4 rounded-2xl hover:border-red-500/50 transition-all duration-300 shadow-sm">
                  <div className="absolute top-0 right-0 p-2 opacity-10 group-hover:opacity-100 transition-opacity">
                    <button onClick={() => handleAcknowledge(alert.id)} className="text-xs font-bold text-red-500 hover:underline">Resolver</button>
                  </div>
                  <div className="flex gap-4">
                    <div className="flex-shrink-0 w-10 h-10 rounded-full bg-red-500/10 flex items-center justify-center text-red-500">
                      <AlertTriangle size={20} />
                    </div>
                    <div className="space-y-1">
                      <h3 className="text-sm font-bold text-foreground">Anomalia detectada: {alert.metric_key?.toUpperCase()}</h3>
                      <p className="text-xs text-muted-foreground leading-relaxed">{alert.message || 'Desvio estatístico identificado no comportamento do canal.'}</p>
                      <div className="pt-2 flex items-center gap-3 text-[10px] text-muted-foreground">
                        <span className="font-mono bg-secondary font-bold px-1.5 py-0.5 rounded">Z-Score: {alert.z_score?.toFixed(2)}</span>
                        <span>Há {Math.round((new Date() - new Date(alert.detected_at)) / 60000)}m atrás</span>
                      </div>
                    </div>
                  </div>
                </div>
              )) : (
                <div className="py-20 text-center border border-dashed border-border/60 rounded-2xl">
                  <CheckCircle className="mx-auto text-green-500 mb-2 opacity-50" size={32} />
                  <p className="text-xs text-muted-foreground font-medium italic">Todos os sistemas em regime de conformidade.</p>
                </div>
              )}
            </div>
          </div>

          <div className="lg:col-span-3 space-y-6">
            <h2 className="text-xs font-black uppercase tracking-[0.2em] text-muted-foreground flex items-center gap-2">
              <span className="h-1 w-1 bg-primary rounded-full" /> Copiloto Estratégico
            </h2>
            <div className="grid gap-4 sm:grid-cols-1">
              {insights?.length > 0 ? insights.map(insight => (
                <div key={insight.id} className="relative group bg-primary/5 border border-primary/20 p-6 rounded-2xl hover:bg-primary/10 transition-all duration-300">
                  <div className="flex items-start gap-5">
                    <div className="flex-shrink-0 w-12 h-12 bg-white rounded-xl shadow-sm flex items-center justify-center text-primary border border-primary/10">
                      <Brain size={24} />
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] font-black uppercase tracking-widest text-primary/60">Análise Predictiva</span>
                        <span className="text-[10px] font-bold bg-primary/10 text-primary px-2 py-0.5 rounded-full">Score: {(insight.confidence_score * 100).toFixed(0)}%</span>
                      </div>
                      <p className="text-sm font-semibold text-foreground leading-normal">{insight.context}</p>
                      <p className="text-xs text-muted-foreground/80 leading-relaxed italic border-l-2 border-primary/20 pl-3">"{insight.ai_response?.substring(0, 150)}..."</p>
                    </div>
                  </div>
                </div>
              )) : (
                <div className="py-20 text-center bg-card/40 border border-border/40 rounded-2xl">
                  <RefreshCw className="mx-auto text-muted-foreground mb-2 opacity-30 animate-spin-slow" size={32} />
                  <p className="text-xs text-muted-foreground font-medium italic">Aguardando novos sinais de mercado para análise.</p>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* CHANNEL TABLE PREMIUM */}
        <section className="space-y-6">
          <h2 className="text-xs font-black uppercase tracking-[0.2em] text-muted-foreground flex items-center gap-2">
            <span className="h-1 w-1 bg-blue-500 rounded-full" /> Eficiência por Canal
          </h2>
          <div className="overflow-hidden bg-card border border-border/40 rounded-3xl shadow-sm">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-secondary/30">
                  <th className="px-8 py-5 text-[10px] font-black uppercase tracking-widest text-muted-foreground">Canal de Aquisição</th>
                  <th className="px-8 py-5 text-[10px] font-black uppercase tracking-widest text-muted-foreground text-right">Spend Total</th>
                  <th className="px-8 py-5 text-[10px] font-black uppercase tracking-widest text-muted-foreground text-right">Receita Direta</th>
                  <th className="px-8 py-5 text-[10px] font-black uppercase tracking-widest text-muted-foreground text-right">ROAS</th>
                  <th className="px-8 py-5 text-[10px] font-black uppercase tracking-widest text-muted-foreground text-center">Benchmark</th>
                </tr>
              </thead>
              <tbody>
                {channels?.length > 0 ? channels.map((ch, idx) => (
                  <tr key={idx} className="border-t border-border/30 hover:bg-primary/[0.02] transition-colors group">
                    <td className="px-8 py-5">
                      <div className="flex items-center gap-3">
                        <div className="w-2 h-2 rounded-full bg-primary/40 group-hover:scale-150 transition-transform" />
                        <span className="text-sm font-bold text-foreground">{ch.channel}</span>
                      </div>
                    </td>
                    <td className="px-8 py-5 text-right text-sm font-mono text-muted-foreground">{formatCurrency(ch.spend)}</td>
                    <td className="px-8 py-5 text-right text-sm font-bold text-foreground">{formatCurrency(ch.revenue)}</td>
                    <td className="px-8 py-5 text-right">
                      <span className={cn(
                        "text-xs font-black px-3 py-1 rounded-full",
                        ch.roas >= 4 ? "bg-green-500/10 text-green-600" : ch.roas >= 2.5 ? "bg-yellow-500/10 text-yellow-600" : "bg-red-500/10 text-red-600"
                      )}>
                        {ch.roas?.toFixed(2)}x
                      </span>
                    </td>
                    <td className="px-8 py-5 text-center">
                      <div className="flex justify-center">
                        <div className="w-24 h-1.5 bg-secondary rounded-full overflow-hidden">
                          <div className="h-full bg-primary transition-all duration-1000" style={{ width: `${Math.min(ch.roas * 20, 100)}%` }} />
                        </div>
                      </div>
                    </td>
                  </tr>
                )) : (
                  <tr>
                    <td colSpan="5" className="px-8 py-20 text-center italic text-muted-foreground text-xs font-medium">Sincronizando canais de mídia...</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>

      </main>

      <footer className="border-t border-border/40 py-12 bg-card/30">
        <div className="container mx-auto px-8 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="text-[10px] font-black uppercase tracking-[0.3em] text-muted-foreground/60">
            &copy; 2026 CMO 360° • MCT LTDA • All rights reserved
          </div>
          <div className="flex gap-8 text-[10px] font-bold uppercase tracking-widest">
            <a href="#" className="text-muted-foreground hover:text-primary transition-colors">Audit Trail</a>
            <a href="#" className="text-muted-foreground hover:text-primary transition-colors">Gov Portal</a>
            <a href="#" className="text-muted-foreground hover:text-primary transition-colors">API Docs</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════════════════════
// HELPER FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════════

function getChannelStatus(roas) {
  if (roas >= 4) return { color: '#22c55e', label: 'Excelente' };
  if (roas >= 2.5) return { color: '#eab308', label: 'Bom' };
  return { color: '#ef4444', label: 'Crítico' };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT DEFAULT
// ═══════════════════════════════════════════════════════════════════════════════

export default App;
