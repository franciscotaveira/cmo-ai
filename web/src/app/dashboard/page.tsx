"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import {
    TrendingUp,
    Target,
    BarChart3,
    Zap,
    ArrowUpRight,
    MousePointer2,
    DollarSign
} from "lucide-react";
import { GlassCard } from "@/components/ui/GlassCard";
import { MetricBadge } from "@/components/ui/MetricBadge";
import { AIInsightCard } from "@/components/ui/AIInsightCard";

interface Metric {
    metric_key: string;
    metric_value: number;
}

interface Insight {
    id: string;
    ai_response: string;
    created_at: string;
}

export default function OverviewPage() {
    const [metrics, setMetrics] = useState<Record<string, number>>({});
    const [insights, setInsights] = useState<Insight[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function loadData() {
            const { data: mData } = await supabase.from("business_metrics").select("metric_key, metric_value").order("date_ref", { ascending: false }).limit(50);
            const { data: iData } = await supabase.from("strategic_insights").select("*").order("created_at", { ascending: false }).limit(2);

            if (mData) {
                const aggregated = mData.reduce((acc, curr) => {
                    if (!acc[curr.metric_key]) acc[curr.metric_key] = curr.metric_value;
                    return acc;
                }, {} as Record<string, number>);
                setMetrics(aggregated);
            }
            if (iData) setInsights(iData);
            setLoading(false);
        }
        loadData();
    }, []);

    return (
        <div className="space-y-10">
            <header>
                <h2 className="text-5xl font-black italic tracking-tighter uppercase text-gradient">Overview</h2>
                <p className="text-zinc-500 font-bold uppercase text-[10px] tracking-[0.2em] mt-2">Marketing Intelligence Hub</p>
            </header>

            {/* Top Level KPIs */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KPICard
                    title="ROAS MÉDIO"
                    value={`${(metrics['roas'] || 8.4).toFixed(1)}x`}
                    trend="+12.4%"
                    trendDir="up"
                    icon={<Zap className="text-primary" size={20} />}
                />
                <KPICard
                    title="CAC MÉDIO"
                    value={`R$ ${(metrics['cac'] || 42).toFixed(2)}`}
                    trend="-8.2%"
                    trendDir="up" // Up because decrease in CAC is good
                    icon={<Target className="text-emerald-500" size={20} />}
                />
                <KPICard
                    title="RECONHECIMENTO"
                    value="82%"
                    trend="+5.1%"
                    trendDir="up"
                    icon={<TrendingUp className="text-indigo-500" size={20} />}
                />
                <KPICard
                    title="INVESTIMENTO"
                    value={`R$ ${(metrics['spend_total'] || 12400).toLocaleString()}`}
                    trend="+2.0%"
                    trendDir="neutral"
                    icon={<DollarSign className="text-amber-500" size={20} />}
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Main Performance Column */}
                <div className="lg:col-span-2 space-y-8">
                    <GlassCard className="h-[400px] flex flex-col">
                        <div className="flex justify-between items-center mb-10">
                            <div>
                                <h3 className="text-lg font-black italic uppercase italic leading-none">Crescimento de Canais</h3>
                                <span className="text-[10px] font-bold opacity-30 uppercase tracking-widest">Performance Semanal</span>
                            </div>
                            <div className="flex gap-4">
                                <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest opacity-60">
                                    <div className="w-2 h-2 rounded-full bg-primary" /> Meta
                                </div>
                                <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest opacity-60">
                                    <div className="w-2 h-2 rounded-full bg-indigo-500" /> Google
                                </div>
                            </div>
                        </div>

                        <div className="flex-1 flex items-end justify-between gap-4 px-4 pb-4">
                            {[60, 45, 80, 55, 90, 70, 85, 40, 75, 95, 65, 88].map((h, i) => (
                                <div key={i} className="flex-1 group relative flex flex-col items-center">
                                    <div className="absolute -top-8 bg-zinc-900 border border-border px-2 py-1 rounded text-[10px] font-black opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10 italic">
                                        {h}% +
                                    </div>
                                    <div className="w-full h-full bg-white/[0.02] rounded-t-lg group-hover:bg-white/[0.05] transition-colors relative overflow-hidden flex flex-col justify-end">
                                        <div className="w-full bg-primary/40 rounded-t-sm transition-all duration-700 delay-100" style={{ height: `${h}%` }} />
                                        <div className="w-full bg-indigo-500/40 rounded-t-sm absolute bottom-0 transition-all duration-700" style={{ height: `${h * 0.7}%` }} />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </GlassCard>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <GlassCard className="bg-emerald-500/[0.02] border-emerald-500/10">
                            <div className="flex justify-between items-start mb-6">
                                <h4 className="font-black italic uppercase text-xs tracking-widest text-emerald-500">Oportunidade SEO</h4>
                                <MousePointer2 className="text-emerald-500 opacity-40" />
                            </div>
                            <p className="text-3xl font-black italic tracking-tighter">+42% v</p>
                            <p className="text-[10px] font-bold opacity-40 uppercase tracking-widest mt-2">Aumento em acessos orgânicos</p>
                        </GlassCard>
                        <GlassCard className="bg-amber-500/[0.02] border-amber-500/10">
                            <div className="flex justify-between items-start mb-6">
                                <h4 className="font-black italic uppercase text-xs tracking-widest text-amber-500">Custo de Conversão</h4>
                                <TrendingUp className="text-amber-500 opacity-40 rotate-180" />
                            </div>
                            <p className="text-3xl font-black italic tracking-tighter">R$ 4.25</p>
                            <p className="text-[10px] font-bold opacity-40 uppercase tracking-widest mt-2">Menor valor registrado no mês</p>
                        </GlassCard>
                    </div>
                </div>

                {/* AI Column */}
                <div className="space-y-6">
                    <div className="flex items-center justify-between px-2">
                        <h3 className="font-black italic uppercase text-sm italic tracking-widest">AI Insights</h3>
                        <div className="px-2 py-0.5 rounded-full bg-primary/20 text-primary text-[8px] font-black uppercase">Alpha 1.0</div>
                    </div>

                    <div className="space-y-4">
                        {insights.map(insight => (
                            <AIInsightCard
                                key={insight.id}
                                content={insight.ai_response}
                                timestamp={new Date(insight.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                type={insight.ai_response.toLowerCase().includes('atenção') ? 'warning' : 'opportunity'}
                            />
                        ))}

                        {insights.length === 0 && (
                            <div className="p-10 text-center glass rounded-3xl opacity-20 italic text-sm">
                                Aguardando sinal do motor de IA...
                            </div>
                        )}
                    </div>

                    <GlassCard className="bg-primary/5 border-primary/20 p-8 text-center space-y-4 relative overflow-hidden group hover:scale-[1.02] transition-transform">
                        <div className="absolute top-0 right-0 w-32 h-32 bg-primary/20 blur-[100px] rounded-full group-hover:bg-primary/40 transition-colors" />
                        <BarChart3 className="mx-auto text-primary animate-pulse" />
                        <h4 className="font-black italic uppercase text-sm italic tracking-tighter">Gerar Relatório v1.0</h4>
                        <p className="text-[10px] font-bold opacity-40 uppercase tracking-widest">Integrar dados de Meta e Google para análise profunda.</p>
                        <button className="w-full py-3 bg-primary text-primary-foreground text-[10px] font-black uppercase italic rounded-xl shadow-xl shadow-primary/20 hover:scale-105 transition-transform">
                            Iniciar Smart Routing
                        </button>
                    </GlassCard>
                </div>
            </div>
        </div>
    );
}

function KPICard({ title, value, trend, trendDir, icon }: { title: string, value: string, trend: string, trendDir: "up" | "down" | "neutral", icon: any }) {
    return (
        <GlassCard className="space-y-4 relative overflow-hidden flex flex-col justify-between group">
            <div className="flex justify-between items-start">
                <h4 className="text-[10px] font-black uppercase tracking-[0.2em] opacity-30">{title}</h4>
                <div className="p-2 bg-white/5 rounded-xl border border-white/10 group-hover:scale-110 transition-transform">
                    {icon}
                </div>
            </div>
            <div className="space-y-1">
                <p className="text-4xl font-black italic tracking-tighter lowercase">{value}</p>
                <div className="flex items-center gap-2">
                    <MetricBadge value={trend} trend={trendDir} />
                    <span className="text-[8px] font-bold opacity-20 uppercase tracking-widest">vs. 30d anterior</span>
                </div>
            </div>
        </GlassCard>
    );
}
