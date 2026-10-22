import styles from './Spinner.module.css';

interface SpinnerProps {
  size?: 'normal' | 'large';
  label?: string;
  className?: string;
}

export function Spinner({ size = 'normal', label, className = '' }: SpinnerProps) {
  return (
    <div className={`${styles.spinnerWrapper} ${className}`} role="status">
      <div
        className={`${styles.spinner} ${size === 'large' ? styles.large : ''}`}
        aria-hidden="true"
      />
      {label && <span className={styles.label}>{label}</span>}
      <span className="sr-only">{label || 'Loading...'}</span>
    </div>
  );
}
