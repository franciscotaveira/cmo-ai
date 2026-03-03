"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import {
    BarChart3,
    TrendingUp,
    Activity,
    Filter,
    Layers,
    Search
} from "lucide-react";
import { GlassCard } from "@/components/ui/GlassCard";
import { MetricBadge } from "@/components/ui/MetricBadge";

export default function PerformanceDashboard() {
    return (
        <div className="space-y-12 animate-fade-up">
            <header className="flex justify-between items-end">
                <div>
                    <h2 className="text-6xl font-black italic tracking-tighter uppercase text-gradient">Performance</h2>
                    <p className="text-zinc-500 font-bold uppercase text-[10px] tracking-[0.3em] mt-3">Channel Efficiency & Conversion Mix</p>
                </div>
                <div className="flex gap-4">
                    <button className="p-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-colors">
                        <Filter size={18} className="opacity-60" />
                    </button>
                    <button className="p-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-colors">
                        <Search size={18} className="opacity-60" />
                    </button>
                </div>
            </header>

            {/* Channel Performance Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
                <ChannelCard
                    channel="Meta Ads"
                    roas="6.4x"
                    spend="R$ 4,500"
                    cpa="R$ 12.40"
                    trend="+14%"
                    color="bg-primary"
                />
                <ChannelCard
                    channel="Google Ads"
                    roas="9.2x"
                    spend="R$ 6,200"
                    cpa="R$ 18.10"
                    trend="+22%"
                    color="bg-indigo-500"
                />
                <ChannelCard
                    channel="Organic / SEO"
                    roas="∞"
                    spend="R$ 0"
                    cpa="R$ 4.20"
                    trend="+5%"
                    color="bg-emerald-500"
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
                {/* CPA Trend Chart Simulation */}
                <GlassCard className="lg:col-span-3 p-10 space-y-10 min-h-[450px]">
                    <div className="flex justify-between items-center">
                        <div>
                            <h3 className="font-black italic uppercase italic tracking-tighter text-xl">Conversion Velocity</h3>
                            <span className="text-[10px] font-bold opacity-30 uppercase tracking-widest">CPA Trend over 30 days</span>
                        </div>
                        <Activity size={20} className="text-primary opacity-40" />
                    </div>

                    <div className="flex-1 flex items-end justify-between gap-2 h-64 px-4">
                        {[40, 50, 45, 60, 55, 70, 65, 80, 75, 90, 85, 95, 82, 70, 60, 50, 40, 35, 45, 55, 65, 75, 85, 95, 85, 75, 65, 55, 45, 35].map((h, i) => (
                            <div key={i} className="flex-1 bg-primary/20 hover:bg-primary transition-colors cursor-pointer group relative" style={{ height: `${h}%` }}>
                                <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-white text-black text-[8px] font-black italic px-1 rounded opacity-0 group-hover:opacity-100 transition-opacity">
                                    R$ {h}
                                </div>
                            </div>
                        ))}
                    </div>
                </GlassCard>

                {/* Lead Mix / Quality */}
                <GlassCard className="lg:col-span-2 p-10 space-y-10">
                    <h3 className="font-black italic uppercase italic tracking-tighter text-xl text-gradient">Lead Maturity Mix</h3>
                    <div className="space-y-8">
                        <p className="text-sm font-bold opacity-60 italic">Distribuição de qualidade por estágio do funil.</p>
                        <div className="space-y-6">
                            <QualityItem label="Prontos para Venda (MQL)" value={68} color="bg-emerald-500" />
                            <QualityItem label="Consideração Ativa" value={42} color="bg-primary" />
                            <QualityItem label="Awareness / Curiosos" value={85} color="bg-indigo-500" />
                            <QualityItem label="Revisão Manual Necessária" value={12} color="bg-red-500" />
                        </div>
                    </div>
                </GlassCard>
            </div>
        </div>
    );
}

function ChannelCard({ channel, roas, spend, cpa, trend, color }: { channel: string, roas: string, spend: string, cpa: string, trend: string, color: string }) {
    return (
        <GlassCard className="p-8 space-y-6 group hover:translate-y-[-4px] transition-transform">
            <div className="flex justify-between items-center">
                <h4 className="font-black italic uppercase text-sm italic tracking-widest opacity-60">{channel}</h4>
                <Layers size={18} className="opacity-20 translate-x-1 translate-y-[-1px]" />
            </div>
            <div className="space-y-1">
                <p className="text-5xl font-black italic tracking-tighter italic">{roas}</p>
                <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold opacity-30 uppercase tracking-[0.2em] italic">ROAS MÉDIO</span>
                    <MetricBadge value={trend} trend="up" />
                </div>
            </div>
            <div className="pt-6 grid grid-cols-2 gap-4 border-t border-border/50">
                <div>
                    <p className="text-[8px] font-black uppercase tracking-widest opacity-30 mb-1">Spend</p>
                    <p className="text-sm font-black italic uppercase tracking-tighter">{spend}</p>
                </div>
                <div>
                    <p className="text-[8px] font-black uppercase tracking-widest opacity-30 mb-1">Avg CPA</p>
                    <p className="text-sm font-black italic uppercase tracking-tighter">{cpa}</p>
                </div>
            </div>
        </GlassCard>
    );
}

function QualityItem({ label, value, color }: { label: string, value: number, color: string }) {
    return (
        <div className="space-y-3">
            <div className="flex justify-between text-[10px] font-bold uppercase tracking-widest group">
                <span className="opacity-40">{label}</span>
                <span className="opacity-80 italic">{value}%</span>
            </div>
            <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden p-0.5">
                <div className={cn("h-full rounded-full transition-all duration-1000", color)} style={{ width: `${value}%` }} />
            </div>
        </div>
    );
}

function cn(...inputs: any[]) {
    return inputs.filter(Boolean).join(" ");
}
