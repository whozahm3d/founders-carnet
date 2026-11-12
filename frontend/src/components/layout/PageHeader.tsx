import styles from './PageHeader.module.css';

interface PageHeaderProps {
  /** Page title (rendered as <h1>) */
  title: string;
  /** Gray subtitle under the title */
  subtitle?: string;
  /** Optional action element shown to the right of the title */
  action?: React.ReactNode;
}

/**
 * Consistent page header: a bold title, optional gray subtitle, and optional right-side action.
 * Matches the wireframe pattern across all dashboard pages.
 */
export function PageHeader({ title, subtitle, action }: PageHeaderProps) {
  return (
    <header className={styles.header}>
      <div className={styles.titleRow}>
        <h1 className={styles.title}>{title}</h1>
        {action && <div className={styles.action}>{action}</div>}
      </div>
      {subtitle && <p className={styles.subtitle}>{subtitle}</p>}
    </header>
  );
}
