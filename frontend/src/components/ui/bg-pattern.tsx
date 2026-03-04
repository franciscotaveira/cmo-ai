/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * BGPattern — Background Pattern Component
 * ═══════════════════════════════════════════════════════════════════════════════
 * Componente para backgrounds decorativos com padrões e masks
 * 
 * @see https://ui.aceternity.com/components/background-pattern
 */

import React from 'react';
import { cn } from '@/lib/utils';

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

type BGVariantType =
  | 'dots'
  | 'diagonal-stripes'
  | 'grid'
  | 'horizontal-lines'
  | 'vertical-lines'
  | 'checkerboard';

type BGMaskType =
  | 'fade-center'
  | 'fade-edges'
  | 'fade-top'
  | 'fade-bottom'
  | 'fade-left'
  | 'fade-right'
  | 'fade-x'
  | 'fade-y'
  | 'none';

type BGPatternProps = React.ComponentProps<'div'> & {
  variant?: BGVariantType;
  mask?: BGMaskType;
  size?: number;
  fill?: string;
};

// ═══════════════════════════════════════════════════════════════════════════════
// MASK CLASSES
// ═══════════════════════════════════════════════════════════════════════════════

const maskClasses: Record<BGMaskType, string> = {
  'fade-edges': '[mask-image:radial-gradient(ellipse_at_center,var(--background),transparent)]',
  'fade-center': '[mask-image:radial-gradient(ellipse_at_center,transparent,var(--background))]',
  'fade-top': '[mask-image:linear-gradient(to_bottom,transparent,var(--background))]',
  'fade-bottom': '[mask-image:linear-gradient(to_bottom,var(--background),transparent)]',
  'fade-left': '[mask-image:linear-gradient(to_right,transparent,var(--background))]',
  'fade-right': '[mask-image:linear-gradient(to_right,var(--background),transparent)]',
  'fade-x': '[mask-image:linear-gradient(to_right,transparent,var(--background),transparent)]',
  'fade-y': '[mask-image:linear-gradient(to_bottom,transparent,var(--background),transparent)]',
  none: '',
};

// ═══════════════════════════════════════════════════════════════════════════════
// BACKGROUND IMAGE GENERATOR
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Gera imagem de background baseada na variante
 */
function getBgImage(variant: BGVariantType, fill: string, size: number): string {
  switch (variant) {
    case 'dots':
      return `radial-gradient(${fill} 1px, transparent 1px)`;

    case 'grid':
      return `linear-gradient(to right, ${fill} 1px, transparent 1px), linear-gradient(to bottom, ${fill} 1px, transparent 1px)`;

    case 'diagonal-stripes':
      return `repeating-linear-gradient(45deg, ${fill}, ${fill} 1px, transparent 1px, transparent ${size}px)`;

    case 'horizontal-lines':
      return `linear-gradient(to bottom, ${fill} 1px, transparent 1px)`;

    case 'vertical-lines':
      return `linear-gradient(to right, ${fill} 1px, transparent 1px)`;

    case 'checkerboard':
      return `linear-gradient(45deg, ${fill} 25%, transparent 25%), linear-gradient(-45deg, ${fill} 25%, transparent 25%), linear-gradient(45deg, transparent 75%, ${fill} 75%), linear-gradient(-45deg, transparent 75%, ${fill} 75%)`;

    default:
      return undefined;
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPONENT
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * BGPattern Component
 * 
 * @param variant - Tipo de padrão (default: 'grid')
 * @param mask - Tipo de mask (default: 'none')
 * @param size - Tamanho do padrão em px (default: 24)
 * @param fill - Cor do padrão (default: '#252525')
 * 
 * @example
 * <BGPattern variant="grid" mask="fade-edges" />
 * <BGPattern variant="dots" mask="fade-center" fill="#b89b76" />
 */
const BGPattern = ({
  variant = 'grid',
  mask = 'none',
  size = 24,
  fill = '#b89b76', // Cor primária do CMO 360°
  className,
  style,
  ...props
}: BGPatternProps) => {
  const bgSize = `${size}px ${size}px`;
  const backgroundImage = getBgImage(variant, fill, size);

  return (
    <div
      className={cn(
        'absolute inset-0 z-[-10] size-full',
        maskClasses[mask],
        className
      )}
      style={{
        backgroundImage,
        backgroundSize: bgSize,
        ...style,
      }}
      {...props}
    />
  );
};

BGPattern.displayName = 'BGPattern';

export { BGPattern };
export type { BGPatternProps, BGVariantType, BGMaskType };
