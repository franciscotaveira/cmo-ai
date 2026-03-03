"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import {
    TrendingUp,
    AlertTriangle,
    LayoutDashboard,
    Target,
    BarChart3,
    User,
    Settings,
    Flame,
    Globe,
    Bell
} from "lucide-react";
import { GlassCard } from "@/components/ui/GlassCard";
import { MetricBadge } from "@/components/ui/MetricBadge";
import { AIInsightCard } from "@/components/ui/AIInsightCard";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

// --- Tipos ---
interface Metric {
    metric_key: string;
    metric_value: number;
    date_ref: string;
}

interface Insight {
    id: string;
    ai_response: string;
    created_at: string;
    status: string;
}

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    const [metrics, setMetrics] = useState<Metric[]>([]);
    const [insights, setInsights] = useState<Insight[]>([]);
    const [loading, setLoading] = useState(true);
    const pathname = usePathname();

    useEffect(() => {
        async function fetchData() {
            try {
                const { data: mData } = await supabase.from("business_metrics").select("*").order("date_ref", { ascending: false }).limit(20);
                const { data: iData } = await supabase.from("strategic_insights").select("*").order("created_at", { ascending: false }).limit(3);

                if (mData) setMetrics(mData);
                if (iData) setInsights(iData);
            } catch (e) { console.error(e); }
            finally { setLoading(false); }
        }
        fetchData();
    }, []);

    return (
        <div className="flex min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
            {/* Sidebar de Elite */}
            <aside className="w-72 border-r border-border bg-card/40 backdrop-blur-3xl p-8 flex flex-col gap-10 sticky top-0 h-screen hidden xl:flex">
                <div className="flex items-center gap-4">
                    <div className="w-10 h-10 bg-primary rounded-2xl flex items-center justify-center shadow-2xl shadow-primary/40 group cursor-pointer">
                        <LayoutDashboard className="text-primary-foreground group-hover:rotate-12 transition-transform" />
                    </div>
                    <div>
                        <h1 className="text-xl font-black tracking-tighter uppercase italic">CMO 360</h1>
                        <p className="text-[10px] font-bold opacity-40 tracking-widest">COMMAND CENTER</p>
                    </div>
                </div>

                <nav className="flex flex-col gap-1">
                    <NavItem href="/dashboard" icon={<Globe size={18} />} label="Overview" active={pathname === "/dashboard"} />
                    <NavItem href="/dashboard/executive" icon={<Target size={18} />} label="Executive" active={pathname === "/dashboard/executive"} />
                    <NavItem href="/dashboard/performance" icon={<BarChart3 size={18} />} label="Performance" active={pathname === "/dashboard/performance"} />
                    <NavItem href="/dashboard/creative" icon={<Flame size={18} />} label="Creatives" active={pathname === "/dashboard/creative"} />
                </nav>

                <div className="mt-auto space-y-6">
                    <GlassCard className="p-4 bg-primary/5 border-primary/20">
                        <p className="text-[10px] font-black uppercase text-primary mb-2">Smart Routing</p>
                        <div className="flex items-center justify-between text-xs font-bold mb-3">
                            <span>Eficiência IA</span>
                            <span className="text-primary">94.2%</span>
                        </div>
                        <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                            <div className="h-full bg-primary w-[94%]" />
                        </div>
                    </GlassCard>

                    <div className="flex items-center gap-4 p-2 group cursor-pointer">
                        <div className="w-11 h-11 rounded-full bg-white/5 border border-white/10 flex items-center justify-center group-hover:border-primary/40 transition-colors shadow-xl">
                            <User size={22} className="opacity-60" />
                        </div>
                        <div>
                            <p className="text-sm font-black italic tracking-tight uppercase">MCT Admin</p>
                            <p className="text-[10px] font-bold opacity-30 uppercase tracking-widest">Premium Tier</p>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Content Area */}
            <main className="flex-1 min-w-0 bg-grid relative overflow-x-hidden">
                {/* Top Header Floating */}
                <header className="sticky top-0 z-50 w-full px-8 py-4 flex justify-between items-center backdrop-blur-md border-b border-border/50">
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.5)]" />
                        <span className="text-[10px] font-bold uppercase tracking-widest opacity-40">System Live</span>
                    </div>

                    <div className="flex items-center gap-4">
                        <button className="p-2 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-colors relative">
                            <Bell size={18} className="opacity-60" />
                            <div className="absolute top-2 right-2 w-1.5 h-1.5 bg-primary rounded-full" />
                        </button>
                        <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-xl text-xs font-black uppercase italic hover:scale-105 transition-transform shadow-2xl shadow-primary/20">
                            Garantir ROI 300%
                        </button>
                    </div>
                </header>

                <div className="p-8 max-w-7xl mx-auto space-y-12 animate-fade-up">
                    {children}
                </div>
            </main>
        </div>
    );
}

function NavItem({ href, icon, label, active = false }: { href: string, icon: any, label: string, active?: boolean }) {
    return (
        <Link
            href={href}
            className={cn(
                "flex items-center gap-4 px-5 py-3.5 rounded-2xl text-sm font-bold transition-all group",
                active
                    ? "bg-primary text-primary-foreground shadow-xl shadow-primary/20"
                    : "text-zinc-500 hover:text-white hover:bg-white/5"
            )}
        >
            <span className={cn(
                "transition-transform group-hover:scale-110",
                active ? "text-primary-foreground" : "text-zinc-500 group-hover:text-primary"
            )}>
                {icon}
            </span>
            <span>{label}</span>
        </Link>
    );
}
