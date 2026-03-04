/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * UTILS — shadcn/ui Utilities
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Combina classes do Tailwind de forma inteligente
 * @param inputs - Classes para combinar
 * @returns Classes combinadas e otimizadas
 * 
 * Usage:
 * cn('text-red-500', 'bg-white') // => 'text-red-500 bg-white'
 * cn('text-red-500', 'text-blue-500') // => 'text-blue-500' (override)
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
