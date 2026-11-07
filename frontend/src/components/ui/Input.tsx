import { forwardRef } from 'react';
import styles from './Input.module.css';

/* ---------- Text input ---------- */
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  hint?: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, hint, error, className, id, ...rest }, ref) => {
    const inputId = id || `input-${label?.toLowerCase().replace(/\s+/g, '-')}`;
    return (
      <div className={styles.field}>
        {label && (
          <label htmlFor={inputId} className={styles.label}>
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={`${styles.input} ${error ? styles.error : ''} ${className || ''}`}
          aria-invalid={!!error}
          aria-describedby={error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined}
          {...rest}
        />
        {hint && !error && (
          <span id={`${inputId}-hint`} className={styles.hint}>
            {hint}
          </span>
        )}
        {error && (
          <span id={`${inputId}-error`} className={styles.errorText} role="alert">
            {error}
          </span>
        )}
      </div>
    );
  },
);
Input.displayName = 'Input';

/* ---------- Textarea ---------- */
interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  hint?: string;
  error?: string;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ label, hint, error, className, id, ...rest }, ref) => {
    const inputId = id || `textarea-${label?.toLowerCase().replace(/\s+/g, '-')}`;
    return (
      <div className={styles.field}>
        {label && (
          <label htmlFor={inputId} className={styles.label}>
            {label}
          </label>
        )}
        <textarea
          ref={ref}
          id={inputId}
          className={`${styles.textarea} ${error ? styles.error : ''} ${className || ''}`}
          aria-invalid={!!error}
          {...rest}
        />
        {hint && !error && <span className={styles.hint}>{hint}</span>}
        {error && (
          <span className={styles.errorText} role="alert">
            {error}
          </span>
        )}
      </div>
    );
  },
);
Textarea.displayName = 'Textarea';

/* ---------- Select ---------- */
interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  hint?: string;
  error?: string;
  options: { value: string; label: string }[];
  placeholder?: string;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, hint, error, options, placeholder, className, id, ...rest }, ref) => {
    const inputId = id || `select-${label?.toLowerCase().replace(/\s+/g, '-')}`;
    return (
      <div className={styles.field}>
        {label && (
          <label htmlFor={inputId} className={styles.label}>
            {label}
          </label>
        )}
        <select
          ref={ref}
          id={inputId}
          className={`${styles.select} ${error ? styles.error : ''} ${className || ''}`}
          aria-invalid={!!error}
          {...rest}
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        {hint && !error && <span className={styles.hint}>{hint}</span>}
        {error && (
          <span className={styles.errorText} role="alert">
            {error}
          </span>
        )}
      </div>
    );
  },
);
Select.displayName = 'Select';
