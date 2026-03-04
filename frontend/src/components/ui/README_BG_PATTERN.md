# 🎨 **BGPattern — Componente Integrado**

> **Status**: ✅ **100% Integrado**  
> **Data**: 2026-03-03  
> **Local**: `/frontend/src/components/ui/bg-pattern.tsx`

---

## 📁 **ESTRUTURA CRIADA**

```
frontend/src/
├── 📂 components/
│   ├── ui/                        ✅ NOVO — Padrão shadcn
│   │   ├── bg-pattern.tsx         ✅ Componente principal
│   │   └── bg-pattern-demo.tsx    ✅ Demo de uso
│   ├── KPICard.jsx
│   └── ...
├── 📂 lib/
│   └── utils.ts                   ✅ Função cn() shadcn
├── 📂 hooks/
│   └── useDashboard.js
├── 📂 services/
│   └── ...
└── App.jsx
```

---

## 🎯 **O QUE É BGPattern**

Componente para **backgrounds decorativos** com padrões geométricos e masks.

### **Variantes**

| Variante | Visual | Uso Ideal |
| :------- | :----- | :-------- |
| `grid` | Grid quadriculado | Cards de KPI, dashboard |
| `dots` | Pontos | Background sutil |
| `diagonal-stripes` | Listras diagonais | Insights, destaques |
| `horizontal-lines` | Linhas horizontais | Timeline, gráficos |
| `vertical-lines` | Linhas verticais | Performance, métricas |
| `checkerboard` | Xadrez | Budget, seções especiais |

### **Masks**

| Mask | Efeito |
| :--- | :----- |
| `fade-edges` | Fade nas bordas (elipse) |
| `fade-center` | Fade no centro |
| `fade-top` | Fade no topo |
| `fade-bottom` | Fade embaixo |
| `fade-left` | Fade esquerda |
| `fade-right` | Fade direita |
| `fade-x` | Fade horizontal (X) |
| `fade-y` | Fade vertical (Y) |
| `none` | Sem mask |

---

## 🚀 **COMO USAR**

### **Import**

```tsx
import { BGPattern } from '@/components/ui/bg-pattern';
```

---

### **Uso Básico**

```tsx
// Background simples
<BGPattern variant="grid" mask="fade-edges" />
```

---

### **Uso em Cards (KPI)**

```tsx
<div className="relative overflow-hidden rounded-xl border bg-card p-6">
  {/* Background pattern */}
  <BGPattern 
    variant="grid" 
    mask="fade-edges" 
    size={24} 
    fill="#b89b76" 
    className="opacity-10"
  />
  
  {/* Conteúdo (z-index maior) */}
  <div className="relative z-10">
    <p className="text-sm text-muted-foreground">Receita Hoje</p>
    <p className="mt-2 text-3xl font-bold">R$ 45.2K</p>
    <p className="mt-1 text-sm text-green-600">↑ +12.5%</p>
  </div>
</div>
```

---

### **Uso em Seções Inteiras**

```tsx
<section className="relative min-h-screen">
  <BGPattern 
    variant="dots" 
    mask="fade-y" 
    size={16} 
    fill="#8a7457"
    className="opacity-20"
  />
  
  {/* Conteúdo da seção */}
  <div className="relative z-10">
    <h1>Dashboard CMO 360°</h1>
    {/* ... */}
  </div>
</section>
```

---

## 🎨 **PROPS DISPONÍVEIS**

| Prop | Tipo | Default | Descrição |
| :--- | :--- | :------ | :-------- |
| `variant` | `'grid' \| 'dots' \| 'diagonal-stripes' \| 'horizontal-lines' \| 'vertical-lines' \| 'checkerboard'` | `'grid'` | Tipo de padrão |
| `mask` | `'fade-edges' \| 'fade-center' \| 'fade-top' \| 'fade-bottom' \| 'fade-left' \| 'fade-right' \| 'fade-x' \| 'fade-y' \| 'none'` | `'none'` | Tipo de mask |
| `size` | `number` | `24` | Tamanho do padrão em px |
| `fill` | `string` | `'#b89b76'` | Cor do padrão (hex, rgb, css var) |
| `className` | `string` | - | Classes Tailwind adicionais |
| `style` | `React.CSSProperties` | - | Estilos inline adicionais |

---

## 📊 **EXEMPLOS PRÁTICOS**

### **1. Dashboard KPI Cards**

```tsx
// 4 KPI Cards com backgrounds diferentes
<div className="grid gap-6 md:grid-cols-4">
  <KPICard>
    <BGPattern variant="grid" mask="fade-edges" fill="#b89b76" />
    Receita: R$ 45.2K
  </KPICard>
  
  <KPICard>
    <BGPattern variant="dots" mask="fade-edges" fill="#8a7457" />
    CAC: R$ 52
  </KPICard>
  
  <KPICard>
    <BGPattern variant="diagonal-stripes" mask="fade-edges" fill="#5c4e3a" />
    ROAS: 3.8x
  </KPICard>
  
  <KPICard>
    <BGPattern variant="horizontal-lines" mask="fade-edges" fill="#2e271d" />
    NPS: 64
  </KPICard>
</div>
```

---

### **2. Alertas Críticos**

```tsx
<div className="relative rounded-xl border border-red-200 bg-red-50 p-6">
  <BGPattern 
    variant="diagonal-stripes" 
    mask="fade-edges" 
    size={32} 
    fill="#ef4444"
    className="opacity-20"
  />
  <div className="relative z-10">
    <AlertTriangle className="text-red-600" />
    <h3>Alerta Crítico</h3>
    <p>CAC 120% acima do benchmark</p>
  </div>
</div>
```

---

### **3. Insights da IA**

```tsx
<div className="relative overflow-hidden rounded-xl border bg-card p-6">
  <BGPattern 
    variant="dots" 
    mask="fade-y" 
    size={12} 
    fill="#b89b76"
    className="opacity-10"
  />
  <div className="relative z-10">
    <Brain className="text-primary" />
    <h3>Insight da IA</h3>
    <p>Recomenda-se otimizar campanhas do Meta Ads...</p>
  </div>
</div>
```

---

### **4. Seção de Budget**

```tsx
<section className="relative bg-card py-16">
  <BGPattern 
    variant="checkerboard" 
    mask="fade-top" 
    size={32} 
    fill="#b89b76"
    className="opacity-5"
  />
  <div className="relative z-10 container mx-auto">
    <h2>Budget & ROI</h2>
    {/* Tabela de budget */}
  </div>
</section>
```

---

## 🎯 **CORES DO CMO 360°**

Use as cores do design system do CMO 360°:

```tsx
// Cores disponíveis (do index.css)
<BGPattern fill="#b89b76" /> // Primary (ouro)
<BGPattern fill="#8a7457" /> // Secondary (bronze)
<BGPattern fill="#5c4e3a" /> // Accent (marrom)
<BGPattern fill="#2e271d" /> // Dark (quase preto)
<BGPattern fill="#18294d" /> // Navy (azul escuro)
```

---

## ⚙️ **CONFIGURAÇÃO TÉCNICA**

### **Dependências**

```json
{
  "clsx": "^2.1.1",      // ✅ Já instalado
  "tailwind-merge": "^3.5.0" // ✅ Já instalado
}
```

---

### **Utils (cn function)**

```ts
// frontend/src/lib/utils.ts
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

---

### **Vite Config (Alias)**

```js
// vite.config.js
export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

---

## 📝 **DEMO**

Para ver todos os variants e masks:

```tsx
// Importar demo
import BGPatternDemo from '@/components/ui/bg-pattern-demo';

// Usar em rota de desenvolvimento
<Route path="/demo/bg-pattern" element={<BGPatternDemo />} />
```

**Acessar**: http://localhost:5173/demo/bg-pattern

---

## 🎨 **INTEGRAÇÃO COM APP.JSX**

### **Opção 1: Background do Dashboard Inteiro**

```tsx
// App.jsx
import { BGPattern } from '@/components/ui/bg-pattern';

function App() {
  return (
    <div style={styles.container}>
      {/* Background pattern em toda a página */}
      <BGPattern 
        variant="grid" 
        mask="fade-edges" 
        size={24} 
        fill="#b89b76"
        className="opacity-5"
      />
      
      {/* Conteúdo */}
      <header>...</header>
      <main>...</main>
    </div>
  );
}
```

---

### **Opção 2: Background em Cards Específicos**

```tsx
// components/KPICard.jsx
import { BGPattern } from '@/components/ui/bg-pattern';

export function KPICard({ icon: Icon, title, value, change, color }) {
  return (
    <div className="relative overflow-hidden rounded-xl border bg-card p-6">
      <BGPattern 
        variant="grid" 
        mask="fade-edges" 
        size={24} 
        fill={color}
        className="opacity-10"
      />
      
      <div className="relative z-10">
        {/* Conteúdo do KPI */}
      </div>
    </div>
  );
}
```

---

## ✅ **CHECKLIST DE INTEGRAÇÃO**

| Tarefa | Status |
| :----- | :----- |
| **Criar `/components/ui/`** | ✅ FEITO |
| **Criar `/lib/utils.ts`** | ✅ FEITO |
| **Copiar `bg-pattern.tsx`** | ✅ FEITO |
| **Criar `bg-pattern-demo.tsx`** | ✅ FEITO |
| **Configurar alias @** | ✅ JÁ CONFIGURADO |
| **Instalar clsx + tailwind-merge** | ✅ JÁ INSTALADO |
| **Testar demo** | ⏳ FAZER |

---

## 🚀 **PRÓXIMOS PASSOS**

1. **Testar Demo**:
   ```bash
   cd frontend
   npm run dev
   
   # Acessar: http://localhost:5173 (se adicionar rota)
   ```

2. **Integrar no App.jsx**:
   - Adicionar background no dashboard
   - Ou usar em cards específicos

3. **Customizar**:
   - Ajustar cores para match com CMO 360°
   - Criar variantes específicas (KPI, Alertas, Insights)

---

<div align="center">

**✅ BGPattern INTEGRADO!**

*Componente shadcn • 6 variants • 9 masks • Pronto para uso*

**PRÓXIMO: Usar em `/components/ui/bg-pattern.tsx`**

</div>
