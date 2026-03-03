#!/usr/bin/env python3
"""
LUNA OS Project Creator - Part 4
Creates frontend Next.js files
"""

import os
import json

BASE_DIR = "/Users/franciscotaveira.ads/LUNA OS"

def create_file(path: str, content: str):
    """Create a file with given content"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {os.path.relpath(path, BASE_DIR)}")

def main():
    print("\n🌙 Creating LUNA OS v2.0 - Part 4 (Frontend)...\n")
    
    # ========== frontend/package.json ==========
    create_file(f"{BASE_DIR}/frontend/package.json", '''{
  "name": "luna-dashboard",
  "version": "2.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.1.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "@tanstack/react-query": "^5.17.9",
    "axios": "^1.6.5",
    "recharts": "^2.10.4",
    "lucide-react": "^0.312.0",
    "date-fns": "^3.3.1",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.1"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "autoprefixer": "^10.0.1",
    "postcss": "^8",
    "tailwindcss": "^3.3.0",
    "typescript": "^5"
  }
}
''')
    
    # ========== frontend/Dockerfile ==========
    create_file(f"{BASE_DIR}/frontend/Dockerfile", '''FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
''')
    
    # ========== frontend/tailwind.config.js ==========
    create_file(f"{BASE_DIR}/frontend/tailwind.config.js", """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        luna: {
          50: '#f0f4ff',
          100: '#e0e9ff',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          900: '#1e1b4b',
        }
      }
    },
  },
  plugins: [],
}
""")
    
    # ========== frontend/postcss.config.js ==========
    create_file(f"{BASE_DIR}/frontend/postcss.config.js", """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
""")
    
    # ========== frontend/tsconfig.json ==========
    create_file(f"{BASE_DIR}/frontend/tsconfig.json", '''{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
''')
    
    # ========== frontend/next.config.js ==========
    create_file(f"{BASE_DIR}/frontend/next.config.js", """/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}

module.exports = nextConfig
""")
    
    # ========== frontend/app/globals.css ==========
    create_file(f"{BASE_DIR}/frontend/app/globals.css", """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-start-rgb: 249, 250, 251;
  --background-end-rgb: 255, 255, 255;
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
    to bottom,
    transparent,
    rgb(var(--background-end-rgb))
  ) rgb(var(--background-start-rgb));
}
""")
    
    # ========== frontend/app/layout.tsx ==========
    create_file(f"{BASE_DIR}/frontend/app/layout.tsx", """import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Providers } from './providers'
import { Sidebar } from '@/components/Sidebar'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Luna Core - Dashboard',
  description: 'Sistema de Atendimento IA Haven',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>
        <Providers>
          <div className="flex h-screen bg-gray-100">
            <Sidebar />
            <main className="flex-1 overflow-y-auto p-8">
              {children}
            </main>
          </div>
        </Providers>
      </body>
    </html>
  )
}
""")
    
    # ========== frontend/app/providers.tsx ==========
    create_file(f"{BASE_DIR}/frontend/app/providers.tsx", """'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient())
  
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}
""")
    
    # ========== frontend/app/page.tsx ==========
    create_file(f"{BASE_DIR}/frontend/app/page.tsx", """'use client'

import { useQuery } from '@tanstack/react-query'
import { MetricCard } from '@/components/MetricCard'
import { ConversionChart } from '@/components/ConversionChart'
import { HourlyChart } from '@/components/HourlyChart'
import { TopServicesChart } from '@/components/TopServicesChart'
import { MessageSquare, Calendar, TrendingUp, Clock, Users, AlertCircle } from 'lucide-react'
import { api } from '@/lib/api'

export default function Dashboard() {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['dashboard'],
    queryFn: () => api.get('/analytics/dashboard?days=7').then(r => r.data)
  })
  
  const { data: hourly } = useQuery({
    queryKey: ['hourly'],
    queryFn: () => api.get('/analytics/hourly?days=30').then(r => r.data)
  })
  
  const { data: services } = useQuery({
    queryKey: ['services'],
    queryFn: () => api.get('/analytics/services?days=30').then(r => r.data)
  })
  
  if (isLoading) {
    return <div className="flex items-center justify-center h-full">Carregando...</div>
  }
  
  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Últimos 7 dias</p>
      </div>
      
      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Conversas"
          value={metrics?.conversations?.total || 0}
          icon={<MessageSquare className="w-6 h-6" />}
          color="blue"
        />
        <MetricCard
          title="Taxa de Conversão"
          value={`${metrics?.conversations?.conversion_rate || 0}%`}
          icon={<TrendingUp className="w-6 h-6" />}
          color="green"
        />
        <MetricCard
          title="Agendamentos"
          value={metrics?.appointments?.total || 0}
          icon={<Calendar className="w-6 h-6" />}
          color="purple"
        />
        <MetricCard
          title="Tempo Médio"
          value={`${Math.round((metrics?.messages?.avg_response_time_ms || 0) / 1000)}s`}
          icon={<Clock className="w-6 h-6" />}
          color="orange"
        />
      </div>
      
      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm">
          <h3 className="text-lg font-semibold mb-4">Horários de Pico</h3>
          <HourlyChart data={hourly || []} />
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm">
          <h3 className="text-lg font-semibold mb-4">Serviços Mais Pedidos</h3>
          <TopServicesChart data={services || []} />
        </div>
      </div>
      
      {/* Handoffs Alert */}
      {metrics?.conversations?.handoffs > 0 && (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-lg">
          <div className="flex items-center">
            <AlertCircle className="w-5 h-5 text-yellow-400 mr-2" />
            <span className="text-yellow-700">
              {metrics.conversations.handoffs} conversa(s) aguardando atendimento humano
            </span>
          </div>
        </div>
      )}
    </div>
  )
}
""")
    
    # ========== frontend/components/Sidebar.tsx ==========
    create_file(f"{BASE_DIR}/frontend/components/Sidebar.tsx", """'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  LayoutDashboard, 
  MessageSquare, 
  BarChart3, 
  Users, 
  Megaphone, 
  BookOpen,
  Settings,
  Moon
} from 'lucide-react'
import { clsx } from 'clsx'

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Conversas', href: '/conversations', icon: MessageSquare },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Clientes', href: '/clients', icon: Users },
  { name: 'Campanhas', href: '/campaigns', icon: Megaphone },
  { name: 'Knowledge', href: '/knowledge', icon: BookOpen },
  { name: 'Configurações', href: '/settings', icon: Settings },
]

export function Sidebar() {
  const pathname = usePathname()
  
  return (
    <div className="w-64 bg-luna-900 text-white flex flex-col">
      {/* Logo */}
      <div className="p-6 flex items-center space-x-3">
        <Moon className="w-8 h-8 text-luna-500" />
        <div>
          <h1 className="text-xl font-bold">Luna Core</h1>
          <p className="text-xs text-gray-400">v2.0</p>
        </div>
      </div>
      
      {/* Navigation */}
      <nav className="flex-1 px-4 space-y-1">
        {navigation.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.name}
              href={item.href}
              className={clsx(
                'flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors',
                isActive 
                  ? 'bg-luna-700 text-white' 
                  : 'text-gray-300 hover:bg-luna-800 hover:text-white'
              )}
            >
              <item.icon className="w-5 h-5" />
              <span>{item.name}</span>
            </Link>
          )
        })}
      </nav>
      
      {/* Status */}
      <div className="p-4 border-t border-luna-700">
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
          <span className="text-sm text-gray-400">Sistema Online</span>
        </div>
      </div>
    </div>
  )
}
""")
    
    # ========== frontend/components/MetricCard.tsx ==========
    create_file(f"{BASE_DIR}/frontend/components/MetricCard.tsx", """import { clsx } from 'clsx'

interface MetricCardProps {
  title: string
  value: string | number
  icon: React.ReactNode
  color: 'blue' | 'green' | 'purple' | 'orange' | 'red'
  change?: number
}

const colorClasses = {
  blue: 'bg-blue-50 text-blue-600',
  green: 'bg-green-50 text-green-600',
  purple: 'bg-purple-50 text-purple-600',
  orange: 'bg-orange-50 text-orange-600',
  red: 'bg-red-50 text-red-600',
}

export function MetricCard({ title, value, icon, color, change }: MetricCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <div className="flex items-center justify-between">
        <div className={clsx('p-3 rounded-lg', colorClasses[color])}>
          {icon}
        </div>
        {change !== undefined && (
          <span className={clsx(
            'text-sm font-medium',
            change >= 0 ? 'text-green-600' : 'text-red-600'
          )}>
            {change >= 0 ? '+' : ''}{change}%
          </span>
        )}
      </div>
      <div className="mt-4">
        <h3 className="text-sm font-medium text-gray-500">{title}</h3>
        <p className="text-2xl font-bold text-gray-900">{value}</p>
      </div>
    </div>
  )
}
""")
    
    # ========== frontend/components/ConversionChart.tsx ==========
    create_file(f"{BASE_DIR}/frontend/components/ConversionChart.tsx", """'use client'

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface ConversionChartProps {
  data: any[]
}

export function ConversionChart({ data }: ConversionChartProps) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="conversions" stroke="#4f46e5" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  )
}
""")
    
    # ========== frontend/components/HourlyChart.tsx ==========
    create_file(f"{BASE_DIR}/frontend/components/HourlyChart.tsx", """'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface HourlyChartProps {
  data: any[]
}

export function HourlyChart({ data }: HourlyChartProps) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="hour" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="count" fill="#6366f1" />
      </BarChart>
    </ResponsiveContainer>
  )
}
""")
    
    # ========== frontend/components/TopServicesChart.tsx ==========
    create_file(f"{BASE_DIR}/frontend/components/TopServicesChart.tsx", """'use client'

import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts'

interface TopServicesChartProps {
  data: any[]
}

const COLORS = ['#4f46e5', '#6366f1', '#818cf8', '#a5b4fc', '#c7d2fe']

export function TopServicesChart({ data }: TopServicesChartProps) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
          outerRadius={80}
          fill="#8884d8"
          dataKey="count"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  )
}
""")
    
    # ========== frontend/lib/api.ts ==========
    create_file(f"{BASE_DIR}/frontend/lib/api.ts", """import axios from 'axios'

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})
""")
    
    print("\n✅ Frontend files created!")

if __name__ == "__main__":
    main()
