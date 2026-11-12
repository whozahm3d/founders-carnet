import styles from './Badge.module.css';

type BadgeVariant = 'default' | 'accent' | 'success' | 'warning' | 'error' | 'dark' | 'outlined';

interface BadgeProps {
  children: React.ReactNode;
  variant?: BadgeVariant;
  className?: string;
}

/**
 * Small rounded pill — used for status labels (Verified, Pending review),
 * fit tags (sector fit, stage fit), and AI-generated badges.
 */
export function Badge({ children, variant = 'default', className }: BadgeProps) {
  const classes = [styles.badge, styles[variant], className].filter(Boolean).join(' ');
  return <span className={classes}>{children}</span>;
}
