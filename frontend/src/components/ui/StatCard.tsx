import styles from './StatCard.module.css';

interface StatCardProps {
  label: string;
  value: string | number;
  subtext?: string;
  badge?: React.ReactNode;
  className?: string;
}

export function StatCard({ label, value, subtext, badge, className = '' }: StatCardProps) {
  return (
    <div className={`${styles.statCard} ${className}`}>
      <div className={styles.header}>
        <span className={styles.label}>{label}</span>
        {badge}
      </div>
      <div className={styles.value}>{value}</div>
      {subtext && <div className={styles.subtext}>{subtext}</div>}
    </div>
  );
}
