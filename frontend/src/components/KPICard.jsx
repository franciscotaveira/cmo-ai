/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * KPI CARD — Componente para exibir KPIs do Dashboard
 * ═══════════════════════════════════════════════════════════════════════════════
 * Componente reutilizável para exibir KPIs com ícone, valor, mudança percentual
 */

import React from 'react';
import { ArrowUpRight, ArrowDownRight, Minus } from 'lucide-react';
import { LineageTooltip } from './ui/lineage-tooltip';

// ═══════════════════════════════════════════════════════════════════════════════
// KPI CARD COMPONENT
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Componente para exibir KPIs do dashboard
 * @param {Object} props
 * @param {React.ComponentType} props.icon - Ícone do Lucide React
 * @param {string} props.title - Título do KPI
 * @param {string} props.value - Valor formatado do KPI
 * @param {number} props.change - Mudança percentual (positiva ou negativa)
 * @param {string} props.color - Cor principal (hex ou CSS variable)
 * @param {Object} props.lineage - Dados de linhagem do KPI
 * @param {string} props.className - Classe CSS adicional
 */
export function KPICard({
  icon: Icon,
  title,
  value,
  change = 0,
  color = 'var(--primary)',
  lineage = null,
  className = '',
}) {
  // Determinar se mudança é positiva, negativa ou neutra
  const isPositive = change > 0;
  const isNeutral = change === 0;

  // Ícone de mudança
  const ChangeIcon = isNeutral ? Minus : isPositive ? ArrowUpRight : ArrowDownRight;
  const changeColor = isNeutral ? 'var(--muted-foreground)' : isPositive ? 'var(--chart-1)' : 'var(--destructive)';

  return (
    <div className={`kpi-card group ${className}`} style={{ ...styles.kpiCard, borderLeft: `4px solid ${color}` }}>
      {/* Header com ícone e título */}
      <div style={styles.kpiHeader}>
        <div className="flex items-center gap-2">
          {Icon && <Icon size={20} color={color} />}
          <span style={styles.kpiTitle}>{title}</span>
        </div>
        <LineageTooltip lineage={lineage} />
      </div>

      {/* Valor do KPI */}
      <div style={styles.kpiValue} className="group-hover:scale-105 transition-transform origin-left duration-300">
        {value}
      </div>

      {/* Mudança percentual */}
      <div style={styles.kpiChange}>
        <ChangeIcon size={16} color={changeColor} />
        <span style={{ color: changeColor, fontWeight: '600' }}>
          {isNeutral ? '—' : isPositive ? '+' : ''}{typeof change === 'number' ? change.toFixed(1) : change}%
        </span>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════════════════════
// STYLES
// ═══════════════════════════════════════════════════════════════════════════════

const styles = {
  kpiCard: {
    backgroundColor: 'var(--card)',
    padding: '20px',
    borderRadius: 'var(--radius)',
    boxShadow: 'var(--shadow)',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  kpiHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    marginBottom: '10px',
  },
  kpiTitle: {
    fontSize: '14px',
    color: 'var(--muted-foreground)',
    fontWeight: '500',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
  kpiValue: {
    fontSize: '28px',
    fontWeight: 'bold',
    color: 'var(--foreground)',
    marginBottom: '5px',
    fontFamily: 'var(--font-mono)',
  },
  kpiChange: {
    display: 'flex',
    alignItems: 'center',
    gap: '5px',
    fontSize: '14px',
    fontWeight: '600',
  },
};

// ═══════════════════════════════════════════════════════════════════════════════
// CSS (para usar com o index.css que tem as variáveis CSS)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * CSS para o KPI Card (adicionar ao index.css ou App.css)
 * 
 * .kpi-card {
 *   background-color: var(--card);
 *   padding: 20px;
 *   border-radius: var(--radius);
 *   box-shadow: var(--shadow);
 *   transition: transform 0.2s, box-shadow 0.2s;
 * }
 * 
 * .kpi-card:hover {
 *   transform: translateY(-2px);
 *   box-shadow: var(--shadow-md);
 * }
 */

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT DEFAULT
// ═══════════════════════════════════════════════════════════════════════════════

export default KPICard;
