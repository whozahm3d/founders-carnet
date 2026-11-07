import styles from './ConsentBox.module.css';

interface ConsentBoxProps {
  id: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  label: string;
  details?: string;
  className?: string;
}

export function ConsentBox({
  id,
  checked,
  onChange,
  label,
  details,
  className = '',
}: ConsentBoxProps) {
  return (
    <div className={`${styles.consentBox} ${className}`}>
      <input
        type="checkbox"
        id={id}
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className={styles.checkbox}
      />
      <div className={styles.content}>
        <label htmlFor={id} className={styles.label}>
          {label}
        </label>
        {details && <p className={styles.details}>{details}</p>}
      </div>
    </div>
  );
}
