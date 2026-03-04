/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * BGPattern Demo — CMO 360°
 * ═══════════════════════════════════════════════════════════════════════════════
 * Demonstração do componente BGPattern adaptado ao CMO 360°
 */

import { BGPattern } from '@/components/ui/bg-pattern';

/**
 * Demo de todos os variants e masks disponíveis
 */
export default function BGPatternDemo() {
  return (
    <div className="mx-auto max-w-6xl space-y-8 p-8">
      <div className="mb-12 text-center">
        <h1 className="text-4xl font-bold text-foreground">🎨 BGPattern — CMO 360°</h1>
        <p className="mt-2 text-muted-foreground">
          Background patterns para dashboards e seções do painel
        </p>
      </div>

      {/* ═══════════════════════════════════════════════════════════════════════════
          GRID (Padrão CMO 360°)
      ═══════════════════════════════════════════════════════════════════════════ */}
      <section>
        <h2 className="mb-4 text-2xl font-semibold">📊 Grid — Padrão CMO 360°</h2>
        <div className="grid gap-6 md:grid-cols-2">
          <div className="relative flex aspect-video flex-col items-center justify-center overflow-hidden rounded-2xl border-2 bg-card">
            <BGPattern variant="grid" mask="fade-edges" size={24} fill="#b89b76" />
            <h3 className="text-2xl font-bold text-foreground">Grid + Fade Edges</h3>
            <p className="text-muted-foreground font-mono">
              Ideal para cards de KPI
            </p>
          </div>

          <div className="relative flex aspect-video flex-col items-center justify-center overflow-hidden rounded-2xl border-2 bg-card">
            <BGPattern variant="grid" mask="fade-center" size={24} fill="#b89b76" />
            <h3 className="text-2xl font-bold text-foreground">Grid + Fade Center</h3>
            <p className="text-muted-foreground font-mono">
              Destaque para seções centrais
            </p>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════════════
          DOTS (Pontos)
      ═══════════════════════════════════════════════════════════════════════════ */}
      <section>
        <h2 className="mb-4 text-2xl font-semibold">⚫ Dots — Pontos</h2>
        <div className="grid gap-6 md:grid-cols-2">
          <div className="relative flex aspect-video flex-col items-center justify-center overflow-hidden rounded-2xl border-2 bg-card">
            <BGPattern variant="dots" mask="fade-y" size={16} fill="#8a7457" />
            <h3 className="text-2xl font-bold text-foreground">Dots + Fade Y</h3>
            <p className="text-muted-foreground font-mono">
              Background sutil para seções
            </p>
          </div>

          <div className="relative flex aspect-video flex-col items-center justify-center overflow-hidden rounded-2xl border-2 bg-card">
            <BGPattern variant="dots" mask="fade-x" size={12} fill="#5c4e3a" />
            <h3 className="text-2xl font-bold text-foreground">Dots + Fade X</h3>
            <p className="text-muted-foreground font-mono">
              Background para alertas
            </p>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════════════
          DIAGONAL STRIPES (Listras Diagonais)
      ═══════════════════════════════════════════════════════════════════════════ */}
      <section>
        <h2 className="mb-4 text-2xl font-semibold">📐 Diagonal Stripes</h2>
        <div className="grid gap-6 md:grid-cols-2">
          <div className="relative flex aspect-video flex-col items-center justify-center overflow-hidden rounded-2xl border-2 bg-card">
            <BGPattern variant="diagonal-stripes" mask="fade-edges" size={32} fill="#b89b76" />
            <h3 className="text-2xl font-bold text-foreground">Stripes + Fade Edges</h3>
            <p className="text-muted-foreground font-mono">
              Destaque para insights
            </p>
          </div>

          <div className="relative flex aspect-video flex-col items-center justify-center overflow-hidden rounded-2xl border-2 bg-card">
            <BGPattern variant="diagonal-stripes" mask="none" size={24} fill="#2e271d" />
            <h3 className="text-2xl font-bold text-foreground">Stripes (No Mask)</h3>
            <p className="text-muted-foreground font-mono">
              Background completo
            </p>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════════════
          LINES (Linhas)
      ═══════════════════════════════════════════════════════════════════════════ */}
      <section>
        <h2 className="mb-4 text-2xl font-semibold">📏 Lines — Linhas</h2>
        <div className="grid gap-6 md:grid-cols-2">
          <div className="relative flex aspect-video flex-col items-center justify-center overflow-hidden rounded-2xl border-2 bg-card">
            <BGPattern variant="horizontal-lines" mask="fade-right" size={20} fill="#8a7457" />
            <h3 className="text-2xl font-bold text-foreground">Horizontal + Fade Right</h3>
            <p className="text-muted-foreground font-mono">
              Timeline de campanhas
            </p>
          </div>

          <div className="relative flex aspect-video flex-col items-center justify-center overflow-hidden rounded-2xl border-2 bg-card">
            <BGPattern variant="vertical-lines" mask="fade-bottom" size={20} fill="#5c4e3a" />
            <h3 className="text-2xl font-bold text-foreground">Vertical + Fade Bottom</h3>
            <p className="text-muted-foreground font-mono">
              Gráficos de performance
            </p>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════════════
          CHECKERBOARD (Xadrez)
      ═══════════════════════════════════════════════════════════════════════════ */}
      <section>
        <h2 className="mb-4 text-2xl font-semibold">◼️ Checkerboard — Xadrez</h2>
        <div className="grid gap-6 md:grid-cols-2">
          <div className="relative flex aspect-video flex-col items-center justify-center overflow-hidden rounded-2xl border-2 bg-card">
            <BGPattern variant="checkerboard" mask="fade-top" size={32} fill="#b89b76" />
            <h3 className="text-2xl font-bold text-foreground">Checkerboard + Fade Top</h3>
            <p className="text-muted-foreground font-mono">
              Seções de budget
            </p>
          </div>

          <div className="relative flex aspect-video flex-col items-center justify-center overflow-hidden rounded-2xl border-2 bg-card">
            <BGPattern variant="checkerboard" mask="fade-bottom" size={24} fill="#8a7457" />
            <h3 className="text-2xl font-bold text-foreground">Checkerboard + Fade Bottom</h3>
            <p className="text-muted-foreground font-mono">
              Seções de métricas
            </p>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════════════
          USO PRÁTICO — CMO 360° DASHBOARD
      ═══════════════════════════════════════════════════════════════════════════ */}
      <section>
        <h2 className="mb-4 text-2xl font-semibold">🎯 Uso Prático — Dashboard CMO 360°</h2>
        
        {/* KPI Card com Background */}
        <div className="grid gap-6 md:grid-cols-4">
          <div className="relative overflow-hidden rounded-xl border bg-card p-6 shadow">
            <BGPattern variant="grid" mask="fade-edges" size={24} fill="#b89b76" opacity={0.1} />
            <div className="relative z-10">
              <p className="text-sm text-muted-foreground">Receita Hoje</p>
              <p className="mt-2 text-3xl font-bold text-foreground">R$ 45.2K</p>
              <p className="mt-1 text-sm text-green-600">↑ +12.5%</p>
            </div>
          </div>

          <div className="relative overflow-hidden rounded-xl border bg-card p-6 shadow">
            <BGPattern variant="dots" mask="fade-edges" size={16} fill="#8a7457" opacity={0.1} />
            <div className="relative z-10">
              <p className="text-sm text-muted-foreground">CAC Médio</p>
              <p className="mt-2 text-3xl font-bold text-foreground">R$ 52</p>
              <p className="mt-1 text-sm text-red-600">↓ -8.3%</p>
            </div>
          </div>

          <div className="relative overflow-hidden rounded-xl border bg-card p-6 shadow">
            <BGPattern variant="diagonal-stripes" mask="fade-edges" size={32} fill="#5c4e3a" opacity={0.1} />
            <div className="relative z-10">
              <p className="text-sm text-muted-foreground">ROAS Médio</p>
              <p className="mt-2 text-3xl font-bold text-foreground">3.8x</p>
              <p className="mt-1 text-sm text-green-600">↑ +5.2%</p>
            </div>
          </div>

          <div className="relative overflow-hidden rounded-xl border bg-card p-6 shadow">
            <BGPattern variant="horizontal-lines" mask="fade-edges" size={20} fill="#2e271d" opacity={0.1} />
            <div className="relative z-10">
              <p className="text-sm text-muted-foreground">NPS</p>
              <p className="mt-2 text-3xl font-bold text-foreground">64</p>
              <p className="mt-1 text-sm text-muted-foreground">→ 0%</p>
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════════════
          CÓDIGO DE EXEMPLO
      ═══════════════════════════════════════════════════════════════════════════ */}
      <section className="rounded-xl border bg-card p-6">
        <h2 className="mb-4 text-xl font-semibold">📝 Como Usar</h2>
        <pre className="overflow-x-auto rounded-lg bg-muted p-4 text-sm font-mono">
{`// Importar
import { BGPattern } from '@/components/ui/bg-pattern';

// Uso básico
<BGPattern variant="grid" mask="fade-edges" />

// Uso avançado (KPI Cards)
<div className="relative">
  <BGPattern 
    variant="grid" 
    mask="fade-edges" 
    size={24} 
    fill="#b89b76" 
  />
  <div className="relative z-10">
    {/* Conteúdo do card */}
  </div>
</div>`}
        </pre>
      </section>
    </div>
  );
}
