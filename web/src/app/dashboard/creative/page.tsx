"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import {
    Flame,
    TrendingUp,
    Image as ImageIcon,
    Play,
    Layout,
    Star,
    Zap,
    Clock
} from "lucide-react";
import { GlassCard } from "@/components/ui/GlassCard";
import { MetricBadge } from "@/components/ui/MetricBadge";

export default function CreativeDashboard() {
    return (
        <div className="space-y-12 animate-fade-up">
            <header className="flex justify-between items-end">
                <div>
                    <h2 className="text-6xl font-black italic tracking-tighter uppercase text-gradient">Creatives</h2>
                    <p className="text-zinc-500 font-bold uppercase text-[10px] tracking-[0.3em] mt-3">Ad Asset Performance & Audience Fatigue</p>
                </div>
                <div className="flex gap-4">
                    <div className="bg-white/5 border border-white/10 px-6 py-3 rounded-2xl backdrop-blur-md flex items-center gap-3">
                        <Star className="text-amber-500 fill-amber-500" size={16} />
                        <span className="text-sm font-black italic tracking-tighter uppercase italic">Best Asset: Lançamento_V1.mp4</span>
                    </div>
                </div>
            </header>

            {/* Top Assets Ranking */}
            <h3 className="font-black italic uppercase italic tracking-widest text-sm px-2">Top Performing Assets</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
                <AssetCard
                    name="Lançamento_V1.mp4"
                    type="Video"
                    ctr="3.24%"
                    roas="8.1x"
                    status="Escalado"
                    color="border-primary/40 bg-primary/5"
                    icon={<Play size={20} className="text-primary" />}
                />
                <AssetCard
                    name="Oferta_Static_Q1.png"
                    type="Image"
                    ctr="2.15%"
                    roas="6.4x"
                    status="Estável"
                    color="border-indigo-500/20 bg-indigo-500/5"
                    icon={<ImageIcon size={20} className="text-indigo-500" />}
                />
                <AssetCard
                    name="UGC_Feedback_Beta.mp4"
                    type="Video"
                    ctr="4.10%"
                    roas="11.2x"
                    status="Promissor"
                    color="border-emerald-500/20 bg-emerald-500/5"
                    icon={<Zap size={20} className="text-emerald-500" />}
                />
                <AssetCard
                    name="Carousel_Features.jpg"
                    type="Carousel"
                    ctr="1.85%"
                    roas="4.2x"
                    status="Fadiga"
                    color="border-amber-500/20 bg-amber-500/5"
                    icon={<Layout size={20} className="text-amber-500" />}
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Ad Fatigue Heatmap Simulation */}
                <GlassCard className="lg:col-span-2 p-10 space-y-10">
                    <div className="flex justify-between items-center">
                        <div>
                            <h3 className="font-black italic uppercase italic tracking-tighter text-xl text-gradient italic">Audience Fatigue Matrix</h3>
                            <span className="text-[10px] font-bold opacity-30 uppercase tracking-widest">Frequência vs. Queda de CTR</span>
                        </div>
                        <Flame size={20} className="text-primary animate-pulse" />
                    </div>

                    <div className="grid grid-cols-7 gap-3">
                        {Array.from({ length: 28 }).map((_, i) => {
                            const intensity = Math.random() * 0.4 + (i / 40);
                            return (
                                <div key={i} className="aspect-square rounded-xl transition-all hover:scale-110 hover:shadow-xl cursor-crosshair border border-white/5"
                                    style={{ backgroundColor: `rgba(59, 130, 246, ${intensity})` }} />
                            );
                        })}
                    </div>

                    <div className="flex justify-between text-[10px] font-bold uppercase tracking-widest opacity-30 px-2 pt-4 border-t border-border/50">
                        <span>Baixa Frequência (Novo)</span>
                        <span>Alta Fadiga (Saturação)</span>
                    </div>
                </GlassCard>

                {/* Quick Creative Action */}
                <GlassCard className="p-10 space-y-8 bg-gradient-to-br from-primary/10 to-transparent">
                    <h3 className="font-black italic uppercase italic tracking-tighter text-xl">Immediate Actions</h3>
                    <div className="space-y-4">
                        <CreativeAction
                            title="Renovar Gancho"
                            target="Lançamento_V1.mp4"
                            msg="O CTR nos primeiros 3s caiu 20%. Testar variação de gancho com pergunta direta."
                            icon={<Clock size={16} />}
                        />
                        <CreativeAction
                            title="Escalar Verba"
                            target="UGC_Feedback_Beta.mp4"
                            msg="ROI 3x acima da média. Suporta aumento de 40% no spend diário."
                            icon={<TrendingUp size={16} />}
                        />
                        <CreativeAction
                            title="Pausar Imediato"
                            target="Carousel_Features.jpg"
                            msg="Frequência > 5.2. Público saturado. Substituir por novo ângulo de oferta."
                            icon={<Flame size={16} />}
                        />
                    </div>
                </GlassCard>
            </div>
        </div>
    );
}

function AssetCard({ name, type, ctr, roas, status, color, icon }: { name: string, type: string, ctr: string, roas: string, status: string, color: string, icon: any }) {
    return (
        <GlassCard className={cn("p-6 space-y-4 border transition-all duration-500 hover:scale-[1.02]", color)}>
            <div className="flex justify-between items-start">
                <div className="space-y-1">
                    <p className="text-[8px] font-black uppercase tracking-widest opacity-40">{type}</p>
                    <h4 className="text-xs font-black italic uppercase tracking-tighter truncate w-32">{name}</h4>
                </div>
                <div className="p-2 bg-white/5 rounded-xl border border-white/10 group-hover:rotate-12 transition-transform">
                    {icon}
                </div>
            </div>

            <div className="pt-4 space-y-3">
                <div className="flex justify-between items-center text-[10px] font-bold uppercase tracking-widest opacity-60">
                    <span>CTR</span>
                    <span className="text-white">{ctr}</span>
                </div>
                <div className="flex justify-between items-center text-[10px] font-bold uppercase tracking-widest opacity-60">
                    <span>ROAS</span>
                    <span className="text-white">{roas}</span>
                </div>
                <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                    <div className="h-full bg-white/40" style={{ width: parseFloat(ctr) * 20 + '%' }} />
                </div>
            </div>

            <div className="pt-2">
                <div className="inline-block px-2 py-0.5 rounded-lg bg-white/5 border border-white/10 text-[8px] font-black uppercase tracking-widest opacity-60">
                    {status}
                </div>
            </div>
        </GlassCard>
    );
}

function CreativeAction({ title, target, msg, icon }: { title: string, target: string, msg: string, icon: any }) {
    return (
        <div className="p-5 rounded-2xl bg-white/5 border border-white/5 space-y-2 hover:bg-white/10 transition-colors cursor-pointer group">
            <div className="flex justify-between items-center">
                <h5 className="text-[10px] font-black italic uppercase text-primary flex items-center gap-2">
                    {icon} {title}
                </h5>
                <span className="text-[8px] font-bold opacity-30 uppercase">{target}</span>
            </div>
            <p className="text-[10px] leading-relaxed opacity-60 group-hover:opacity-100 transition-opacity">{msg}</p>
        </div>
    );
}

function cn(...inputs: any[]) {
    return inputs.filter(Boolean).join(" ");
}
