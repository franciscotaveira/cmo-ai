import React, { useState, useEffect } from 'react';
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar
} from 'recharts';
import { TrendingUp, DollarSign, Target, Activity, ArrowUpRight, ArrowDownRight, Loader } from 'lucide-react';
import { getExecutiveDashboard } from '../../lib/api';

const ExecutiveDashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await getExecutiveDashboard('default');
                setData(response);
            } catch (err) {
                setError('Falha ao carregar os dados do painel.');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="flex h-full items-center justify-center text-primary">
                <Loader className="w-10 h-10 animate-spin" />
                <span className="ml-3 font-medium">Conectando ao Cérebro...</span>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex h-full items-center justify-center text-danger flex-col">
                <Activity className="w-10 h-10 mb-3" />
                <span className="font-medium">{error}</span>
                <button onClick={() => window.location.reload()} className="mt-4 px-4 py-2 bg-white/5 border border-white/10 hover:bg-white/10 rounded-lg text-sm text-gray-300 transition-colors">Tentar Novamente</button>
            </div>
        );
    }

    const { kpis, charts, tenant_name } = data;

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Header */}
            <div>
                <h1 className="text-3xl font-extrabold tracking-tight text-white mb-1">Command Center</h1>
                <p className="text-sm text-gray-400">Visão executiva agregada. Operando para: <span className="text-primary font-semibold">{tenant_name}</span>.</p>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <KpiCard
                    title="Receita Atribuída"
                    value={`R$ ${(kpis.revenue.value / 1000).toFixed(1)}k`}
                    trend={kpis.revenue.trend}
                    isPositive={kpis.revenue.isPositive}
                    icon={<DollarSign className="w-5 h-5 text-success" />}
                    colorClass="text-success"
                />
                <KpiCard
                    title="Investimento Total"
                    value={`R$ ${(kpis.spend.value / 1000).toFixed(1)}k`}
                    trend={kpis.spend.trend}
                    isPositive={kpis.spend.isPositive}
                    icon={<TrendingUp className="w-5 h-5 text-secondary" />}
                    colorClass="text-secondary"
                />
                <KpiCard
                    title="ROAS Blended"
                    value={`${kpis.roas.value.toFixed(2)}x`}
                    trend={kpis.roas.trend}
                    isPositive={kpis.roas.isPositive}
                    icon={<Target className="w-5 h-5 text-primary" />}
                    colorClass="text-primary neon-text-primary"
                />
                <KpiCard
                    title="CAC Global"
                    value={`R$ ${kpis.cac.value.toFixed(2)}`}
                    trend={kpis.cac.trend}
                    isPositive={kpis.cac.isPositive}
                    icon={<Activity className="w-5 h-5 text-danger" />}
                    colorClass="text-danger"
                />
            </div>

            {/* Charts Area */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="glass-card p-6 lg:col-span-2 relative overflow-hidden">
                    {/* Subtle bg glow */}
                    <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 blur-[100px] rounded-full pointer-events-none"></div>

                    <h3 className="text-lg font-bold mb-6 text-white">Evolução Histórica (Spend vs Receita)</h3>
                    <div className="h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={charts} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                                <defs>
                                    <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.8} />
                                        <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0} />
                                    </linearGradient>
                                    <linearGradient id="colorSpend" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#06B6D4" stopOpacity={0.8} />
                                        <stop offset="95%" stopColor="#06B6D4" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                                <XAxis dataKey="name" stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} />
                                <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(val) => `R$${val / 1000}k`} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#16161A', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '0.5rem', color: '#fff' }}
                                    itemStyle={{ color: '#fff' }}
                                />
                                <Area type="monotone" dataKey="revenue" name="Receita" stroke="#8B5CF6" strokeWidth={3} fillOpacity={1} fill="url(#colorRevenue)" />
                                <Area type="monotone" dataKey="spend" name="Investimento" stroke="#06B6D4" strokeWidth={3} fillOpacity={1} fill="url(#colorSpend)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="glass-card p-6">
                    <h3 className="text-lg font-bold mb-6 text-white">Estabilidade do ROAS</h3>
                    <div className="h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={charts} margin={{ top: 10, right: 0, left: -30, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                                <XAxis dataKey="name" stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} />
                                <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} />
                                <Tooltip
                                    cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                                    contentStyle={{ backgroundColor: '#16161A', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '0.5rem' }}
                                />
                                <Bar dataKey="roas" name="ROAS Blended" fill="#10B981" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        </div>
    );
};

const KpiCard = ({ title, value, trend, isPositive, icon, colorClass }) => (
    <div className="glass-card p-5 group flex flex-col justify-between" suppressHydrationWarning>
        <div className="flex justify-between items-start mb-4">
            <div className={`p-2 rounded-lg bg-white/5 border border-white/5 group-hover:bg-white/10 transition-colors`}>
                {icon}
            </div>
            <div className={`flex items-center space-x-1 text-xs font-bold px-2 py-1 rounded-full ${isPositive ? 'bg-success/10 text-success' : 'bg-danger/10 text-danger'}`}>
                <span>{trend}</span>
                {isPositive ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
            </div>
        </div>
        <div>
            <h3 className="text-sm font-medium text-gray-400 mb-1">{title}</h3>
            <p className={`text-3xl font-extrabold tracking-tight ${colorClass}`}>{value}</p>
        </div>
    </div>
);

export default ExecutiveDashboard;
