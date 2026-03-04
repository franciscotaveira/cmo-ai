import React from 'react';
import { MessageSquare, Sparkles, AlertCircle, ChevronRight } from 'lucide-react';

const CopilotPanel = () => {
    return (
        <aside className="w-80 bg-panel/50 backdrop-blur-xl border-l border-white/10 h-screen fixed right-0 top-0 flex flex-col shadow-[-10px_0_30px_rgba(0,0,0,0.5)] z-20">
            {/* Header */}
            <div className="p-6 border-b border-white/5 bg-panel/80">
                <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-[0_0_15px_rgba(139,92,246,0.5)]">
                        <Sparkles className="w-5 h-5 text-white" />
                    </div>
                    <div>
                        <h2 className="text-lg font-bold text-white tracking-wide">CMO Copilot</h2>
                        <p className="text-xs text-secondary font-medium uppercase tracking-widest">Kimi-K2 Active</p>
                    </div>
                </div>
            </div>

            {/* Insight Stream */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                <InsightCard
                    type="anomaly"
                    title="Queda no ROAS"
                    message="Identifiquei uma queda de 34% no ROAS do Google Ads comparado à média dos últimos 7 dias. O Z-Score atual é de -2.4."
                    action="Ver detalhes"
                />
                <InsightCard
                    type="opportunity"
                    title="Saturação de Criativo"
                    message="O conjunto de anúncios 'Black Friday Antecipada' no Meta Ads atingiu frequência 4.2. Recomendo pausar ou trocar os criativos."
                    action="Gerar novos criativos"
                />
            </div>

            {/* Input Area */}
            <div className="p-4 border-t border-white/5 bg-panel/80">
                <div className="relative">
                    <input
                        type="text"
                        placeholder="Pergunte ao Cérebro de Marketing..."
                        className="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-4 pr-12 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all"
                    />
                    <button className="absolute right-2 top-2 p-1.5 rounded-lg bg-primary/20 hover:bg-primary/40 text-primary transition-colors">
                        <MessageSquare size={16} />
                    </button>
                </div>
            </div>
        </aside>
    );
};

const InsightCard = ({ type, title, message, action }) => {
    const isAnomaly = type === 'anomaly';

    return (
        <div className={`glass-card p-4 border-l-2 ${isAnomaly ? 'border-l-danger' : 'border-l-secondary'}`}>
            <div className="flex items-center space-x-2 mb-2">
                {isAnomaly ? <AlertCircle className="w-4 h-4 text-danger" /> : <Sparkles className="w-4 h-4 text-secondary" />}
                <h4 className="text-sm font-semibold text-white">{title}</h4>
            </div>
            <p className="text-xs text-gray-300 leading-relaxed mb-3">{message}</p>
            <button className="flex items-center space-x-1 text-xs text-primary font-medium hover:text-white transition-colors group">
                <span>{action}</span>
                <ChevronRight size={14} className="group-hover:translate-x-1 transition-transform" />
            </button>
        </div>
    );
};

export default CopilotPanel;
