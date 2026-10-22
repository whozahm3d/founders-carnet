import styles from './Card.module.css';

interface CardProps {
  children: React.ReactNode;
  /** Make the card respond to hover with a shadow lift */
  hoverable?: boolean;
  /** Compact padding variant */
  compact?: boolean;
  /** No padding (for custom inner layouts) */
  flush?: boolean;
  className?: string;
}

/**
 * White rounded card — the primary container for dashboard content.
 * Matches the wireframe pattern: white bg, light border, rounded corners.
 */
export function Card({ children, hoverable, compact, flush, className }: CardProps) {
  const classes = [
    styles.card,
    hoverable && styles.cardHoverable,
    compact && styles.cardCompact,
    flush && styles.cardFlush,
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return <div className={classes}>{children}</div>;
}
