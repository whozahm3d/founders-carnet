import styles from './Button.module.css';

type ButtonVariant = 'primary' | 'secondary' | 'accent' | 'ghost' | 'link';
type ButtonSize = 'sm' | 'md' | 'lg';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  fullWidth?: boolean;
  block?: boolean;
  children: React.ReactNode;
}

/**
 * Button component.
 * Primary: black fill (wireframe "Submit for review", "Create account").
 * Secondary: white outlined (wireframe "Save draft", "Recalculate score").
 * Accent: blue fill (wireframe "Practice your pitch", "Send").
 */
export function Button({
  variant = 'primary',
  size = 'md',
  fullWidth,
  block,
  children,
  className,
  ...rest
}: ButtonProps) {
  const isBlock = fullWidth || block;
  const classes = [
    styles.btn,
    styles[variant],
    size !== 'md' && styles[size],
    isBlock && styles.fullWidth,
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <button className={classes} {...rest}>
      {children}
    </button>
  );
}
