import React from "react";
import { Sparkles, LucideIcon } from "lucide-react";
import { GlassCard } from "./GlassCard";
import { cn } from "@/lib/utils";

interface AIInsightCardProps {
    content: string;
    type?: "opportunity" | "warning" | "info";
    timestamp: string;
    icon?: LucideIcon;
}

export function AIInsightCard({
    content,
    type = "info",
    timestamp,
    icon: Icon = Sparkles
}: AIInsightCardProps) {
    const typeStyles = {
        opportunity: "border-indigo-500/30 bg-indigo-500/5 text-indigo-400",
        warning: "border-amber-500/30 bg-amber-500/5 text-amber-400",
        info: "border-blue-500/30 bg-blue-500/5 text-blue-400"
    };

    return (
        <GlassCard className={cn("relative group transition-all duration-500", typeStyles[type])}>
            <div className="flex items-start gap-4">
                <div className="p-2 rounded-xl bg-white/5 border border-white/10 group-hover:scale-110 transition-transform">
                    <Icon size={18} />
                </div>
                <div className="flex-1 space-y-2">
                    <div className="flex justify-between items-center">
                        <span className="text-[10px] font-bold uppercase tracking-widest opacity-60">Insight Automático</span>
                        <span className="text-[10px] opacity-40">{timestamp}</span>
                    </div>
                    <p className="text-sm leading-relaxed text-zinc-300 group-hover:text-white transition-colors">
                        {content}
                    </p>
                    <div className="pt-2 flex gap-2">
                        <button className="text-[10px] font-bold px-3 py-1 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 transition-colors">
                            Aplicar Sugestão
                        </button>
                        <button className="text-[10px] font-bold px-3 py-1 rounded-lg hover:bg-white/5 transition-colors opacity-60">
                            Arquivar
                        </button>
                    </div>
                </div>
            </div>
        </GlassCard>
    );
}
