import styles from './ProgressBar.module.css';

interface ProgressBarProps {
  value: number; // 0 to 100
  label?: string;
  showValueText?: boolean;
  variant?: 'accent' | 'success' | 'warning';
  size?: 'normal' | 'large';
  className?: string;
}

export function ProgressBar({
  value,
  label,
  showValueText = true,
  variant = 'accent',
  size = 'normal',
  className = '',
}: ProgressBarProps) {
  const clampedValue = Math.min(100, Math.max(0, value));

  const barVariantClass =
    variant === 'success'
      ? styles.barSuccess
      : variant === 'warning'
      ? styles.barWarning
      : '';

  return (
    <div className={`${styles.progressWrapper} ${className}`}>
      {(label || showValueText) && (
        <div className={styles.labelRow}>
          {label && <span className={styles.label}>{label}</span>}
          {showValueText && <span className={styles.value}>{Math.round(clampedValue)}%</span>}
        </div>
      )}
      <div
        className={`${styles.track} ${size === 'large' ? styles.trackLarge : ''}`}
        role="progressbar"
        aria-valuenow={clampedValue}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div
          className={`${styles.bar} ${barVariantClass}`}
          style={{ width: `${clampedValue}%` }}
        />
      </div>
    </div>
  );
}
