import styles from './MatchCard.module.css';
import { Badge } from './Badge';
import { Button } from './Button';

interface MatchCardProps {
  id: string;
  name: string;
  role: string;
  matchScore: number;
  tags?: string[];
  explanation?: string;
  onConnect?: (id: string) => void;
  onDismiss?: (id: string) => void;
  actionLabel?: string;
  className?: string;
}

export function MatchCard({
  id,
  name,
  role,
  matchScore,
  tags = [],
  explanation,
  onConnect,
  onDismiss,
  actionLabel = 'Connect',
  className = '',
}: MatchCardProps) {
  return (
    <div className={`${styles.matchCard} ${className}`}>
      <div className={styles.header}>
        <div className={styles.titleArea}>
          <span className={styles.name}>{name}</span>
          <span className={styles.role}>{role}</span>
        </div>
        <div className={styles.scoreBadge}>{Math.round(matchScore)}% match</div>
      </div>

      {tags.length > 0 && (
        <div className={styles.tags}>
          {tags.map((tag) => (
            <Badge key={tag} variant="default">
              {tag}
            </Badge>
          ))}
        </div>
      )}

      {explanation && <p className={styles.explanation}>{explanation}</p>}

      {(onConnect || onDismiss) && (
        <div className={styles.actions}>
          {onDismiss && (
            <Button variant="ghost" size="sm" onClick={() => onDismiss(id)}>
              Dismiss
            </Button>
          )}
          {onConnect && (
            <Button variant="primary" size="sm" onClick={() => onConnect(id)}>
              {actionLabel}
            </Button>
          )}
        </div>
      )}
    </div>
  );
}
