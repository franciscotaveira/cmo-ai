"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import {
    TrendingUp,
    Target,
    Zap,
    DollarSign,
    PieChart,
    Activity
} from "lucide-react";
import { GlassCard } from "@/components/ui/GlassCard";
import { MetricBadge } from "@/components/ui/MetricBadge";

export default function ExecutiveDashboard() {
    return (
        <div className="space-y-12 animate-fade-up">
            <header className="flex justify-between items-end">
                <div>
                    <h2 className="text-6xl font-black italic tracking-tighter uppercase text-gradient">Executive</h2>
                    <p className="text-zinc-500 font-bold uppercase text-[10px] tracking-[0.3em] mt-3">Strategic ROI Control</p>
                </div>
                <div className="bg-white/5 border border-white/10 px-6 py-3 rounded-2xl backdrop-blur-md">
                    <span className="text-[10px] font-bold uppercase opacity-40">Período Fiscal</span>
                    <p className="text-sm font-black italic">Q1 2026 • JAN-MAR</p>
                </div>
            </header>

            {/* Main Strategic KPIs */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <GlassCard className="p-8 space-y-6 bg-primary/5 border-primary/20">
                    <div className="flex justify-between">
                        <span className="text-xs font-black uppercase tracking-widest text-primary">ROAS Goal</span>
                        <Target size={20} className="text-primary opacity-40" />
                    </div>
                    <p className="text-6xl font-black italic tracking-tighter italic">12.5x</p>
                    <div className="flex items-center gap-3">
                        <MetricBadge value="+1.2x" trend="up" className="bg-primary/20 text-primary" />
                        <span className="text-[10px] font-bold opacity-30 uppercase tracking-[0.2em]">Acima da Meta</span>
                    </div>
                    <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                        <div className="h-full bg-primary w-[88%]" />
                    </div>
                </GlassCard>

                <GlassCard className="p-8 space-y-6">
                    <div className="flex justify-between">
                        <span className="text-xs font-black uppercase tracking-widest opacity-40">Receita Total</span>
                        <DollarSign size={20} className="text-emerald-500 opacity-40" />
                    </div>
                    <p className="text-6xl font-black italic tracking-tighter italic">R$ 2.4M</p>
                    <div className="flex items-center gap-3">
                        <MetricBadge value="+22%" trend="up" />
                        <span className="text-[10px] font-bold opacity-30 uppercase tracking-[0.2em]">Crescimento MoM</span>
                    </div>
                </GlassCard>

                <GlassCard className="p-8 space-y-6">
                    <div className="flex justify-between">
                        <span className="text-xs font-black uppercase tracking-widest opacity-40">Custo de Aquisição</span>
                        <Zap size={20} className="text-amber-500 opacity-40" />
                    </div>
                    <p className="text-6xl font-black italic tracking-tighter italic">R$ 14.80</p>
                    <div className="flex items-center gap-3">
                        <MetricBadge value="-15%" trend="up" />
                        <span className="text-[10px] font-bold opacity-30 uppercase tracking-[0.2em]">Redução de Custo</span>
                    </div>
                </GlassCard>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Market Share / Channel Efficiency */}
                <GlassCard className="p-10 space-y-10 min-h-[500px]">
                    <div className="flex justify-between items-center">
                        <h3 className="font-black italic uppercase italic tracking-tighter text-xl">Market Efficiency Grid</h3>
                        <PieChart size={20} className="opacity-20" />
                    </div>

                    <div className="space-y-8">
                        <EfficiencyItem label="Paid Social (Meta)" value={78} color="bg-primary" />
                        <EfficiencyItem label="Paid Search (Google)" value={92} color="bg-indigo-500" />
                        <EfficiencyItem label="Email Marketing" value={45} color="bg-emerald-500" />
                        <EfficiencyItem label="Direct / Organic" value={65} color="bg-amber-500" />
                    </div>
                </GlassCard>

                {/* Strategic Roadmap */}
                <GlassCard className="p-10 space-y-10 relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-10 opacity-[0.02]">
                        <Activity size={200} />
                    </div>
                    <h3 className="font-black italic uppercase italic tracking-tighter text-xl">Strategic Insights Engine</h3>
                    <div className="space-y-6">
                        <InsightItem
                            title="Saturação de Ad Spend"
                            desc="O canal Meta Ads atingiu o ponto de retorno decrescente. Recomendamos realocação de 15% do orçamento para Google Shopping em Q2."
                            type="critical"
                        />
                        <InsightItem
                            title="Oportunidade de LTV"
                            desc="Leads vindos do canal Orgânico possuem LTV 2.4x maior. Sugerimos dobrar o investimento em produção de conteúdo em vídeo."
                            type="growth"
                        />
                        <InsightItem
                            title="Redução em Churn"
                            desc="A nova régua de e-mail reduziu o churn precoce em 18%. Manter estratégia atual."
                            type="success"
                        />
                    </div>
                </GlassCard>
            </div>
        </div>
    );
}

function EfficiencyItem({ label, value, color }: { label: string, value: number, color: string }) {
    return (
        <div className="space-y-3">
            <div className="flex justify-between text-[10px] font-bold uppercase tracking-widest opacity-60">
                <span>{label}</span>
                <span>{value}%</span>
            </div>
            <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                <div className={cn("h-full transition-all duration-1000", color)} style={{ width: `${value}%` }} />
            </div>
        </div>
    );
}

function InsightItem({ title, desc, type }: { title: string, desc: string, type: "critical" | "growth" | "success" }) {
    const styles = {
        critical: "border-red-500/20 bg-red-500/5 text-red-400",
        growth: "border-primary/20 bg-primary/5 text-primary",
        success: "border-emerald-500/20 bg-emerald-500/5 text-emerald-400"
    };

    return (
        <div className={cn("p-6 rounded-2xl border transition-all hover:scale-[1.01] cursor-pointer", styles[type])}>
            <h4 className="font-black italic uppercase text-xs tracking-widest mb-2">{title}</h4>
            <p className="text-xs font-medium leading-relaxed opacity-80 text-white">{desc}</p>
        </div>
    );
}

function cn(...inputs: any[]) {
    return inputs.filter(Boolean).join(" ");
}
