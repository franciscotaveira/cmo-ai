import React from 'react';
import { Info, FileText, Database, ShieldCheck } from 'lucide-react';
import { cn } from '@/lib/utils';

/**
 * LineageTooltip Component
 * Displays the audit trail (lineage) of a metric.
 */
export const LineageTooltip = ({ lineage, className }) => {
    if (!lineage) return null;

    const { source, confidence, date, file_name, file_type, ingested_at } = lineage;

    return (
        <div className={cn(
            "group relative inline-block ml-2 cursor-help",
            className
        )}>
            <Info size={14} className="text-muted-foreground hover:text-primary transition-colors" />

            {/* Tooltip Content */}
            <div className="absolute bottom-full left-1/2 mb-2 w-64 -translate-x-1/2 scale-95 opacity-0 transition-all group-hover:scale-100 group-hover:opacity-100 z-50">
                <div className="rounded-xl border border-border bg-card/95 p-4 shadow-xl backdrop-blur-md">
                    <div className="flex items-center gap-2 mb-3 pb-2 border-b border-border/50">
                        <ShieldCheck size={16} className="text-green-500" />
                        <span className="text-xs font-bold uppercase tracking-wider">Linhagem Auditável</span>
                    </div>

                    <div className="space-y-3">
                        <div className="flex items-start gap-3">
                            <Database size={14} className="mt-0.5 text-primary" />
                            <div>
                                <p className="text-[10px] uppercase text-muted-foreground font-semibold">Fonte de Origem</p>
                                <p className="text-xs font-medium">{source}</p>
                            </div>
                        </div>

                        {file_name && (
                            <div className="flex items-start gap-3">
                                <FileText size={14} className="mt-0.5 text-primary" />
                                <div>
                                    <p className="text-[10px] uppercase text-muted-foreground font-semibold">Arquivo Relacionado</p>
                                    <p className="text-xs font-medium truncate w-40">{file_name}</p>
                                </div>
                            </div>
                        )}

                        <div className="grid grid-cols-2 gap-2 pt-1">
                            <div>
                                <p className="text-[10px] uppercase text-muted-foreground font-semibold">Confiança</p>
                                <span className={cn(
                                    "text-[10px] font-bold px-1.5 py-0.5 rounded",
                                    confidence === 'alta' ? "bg-green-500/10 text-green-500" : "bg-yellow-500/10 text-yellow-500"
                                )}>
                                    {confidence?.toUpperCase()}
                                </span>
                            </div>
                            <div>
                                <p className="text-[10px] uppercase text-muted-foreground font-semibold">Data Ref</p>
                                <p className="text-[10px] font-mono">{date}</p>
                            </div>
                        </div>
                    </div>

                    <div className="mt-3 pt-2 border-t border-border/50 text-[9px] text-muted-foreground italic">
                        Ingerido em: {ingested_at ? new Date(ingested_at).toLocaleString() : 'N/A'}
                    </div>
                </div>

                {/* Triangle Arrow */}
                <div className="absolute top-full left-1/2 -translate-x-1/2 border-8 border-transparent border-t-card/95" />
            </div>
        </div>
    );
};
