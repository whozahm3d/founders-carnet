'use client';

import { useState } from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import { StatCard, Badge } from '@/components/ui';
import styles from '@/components/layout/Dashboard.module.css';
import queueStyles from './AdminQueue.module.css';

interface ReviewItem {
  id: string;
  name: string;
  type: string;
  badgeLabel: string;
  badgeVariant: 'accent' | 'warning' | 'neutral' | 'success';
  statusTag: string;
  statusDesc: string;
  signals: { label: string; value: string }[];
  scoreLabel: string;
  scoreValue: string;
}

export default function AdminDashboardPage() {
  const [escalatedCount, setEscalatedCount] = useState(2);
  const [appealsCount, setAppealsCount] = useState(1);
  const [decidedCount, setDecidedCount] = useState(2);

  const [reasons, setReasons] = useState<Record<string, string>>({
    'munshi-books': '',
    'nida-farooq': '',
  });

  const [decisions, setDecisions] = useState<Record<string, 'approved' | 'rejected' | null>>({
    'munshi-books': null,
    'nida-farooq': null,
  });

  const handleReasonChange = (id: string, text: string) => {
    setReasons((prev) => ({ ...prev, [id]: text }));
  };

  const handleDecision = (id: string, decision: 'approved' | 'rejected', isAppeal: boolean) => {
    setDecisions((prev) => ({ ...prev, [id]: decision }));
    setDecidedCount((prev) => prev + 1);
    if (isAppeal) {
      setAppealsCount((prev) => Math.max(0, prev - 1));
    } else {
      setEscalatedCount((prev) => Math.max(0, prev - 1));
    }
  };

  return (
    <div className={styles.pageContainer}>
      <PageHeader
        title="Console"
        subtitle="Review escalated profiles and appeals. Rejection is final."
      />

      {/* Top 3 Stat Cards from 12_Admin_Queue.png */}
      <div className={styles.statGrid}>
        <StatCard label="Escalated profiles" value={String(escalatedCount)} />
        <StatCard label="Appeals" value={String(appealsCount)} />
        <StatCard label="Decided today" value={String(decidedCount)} />
      </div>

      {/* Review Cards Grid */}
      <div className={queueStyles.adminQueueGrid}>
        {/* Card 1: Munshi Books */}
        <div className={queueStyles.reviewCard}>
          <div className={queueStyles.cardHeader}>
            <div>
              <h2 className={queueStyles.entityName}>Munshi Books</h2>
              <div className={queueStyles.entitySubtitle}>Founder profile</div>
            </div>
            <Badge variant="default">Pending review</Badge>
          </div>

          <div className={queueStyles.pillsRow}>
            <span className={queueStyles.escalatedBadge}>Escalated profile</span>
          </div>

          <div>
            <div className={queueStyles.sectionLabel}>CURRENT STATUS</div>
            <div className={queueStyles.statusRow} style={{ marginTop: '4px' }}>
              <Badge variant="default">Pending review</Badge>
              <span>Manual verification required</span>
            </div>
          </div>

          <div>
            <div className={queueStyles.sectionLabel}>SIGNALS</div>
            <div className={queueStyles.signalsGrid}>
              <div className={queueStyles.signalItem}>
                <span className={queueStyles.signalLabel}>LinkedIn</span>
                <span className={queueStyles.signalValue}>Connected</span>
              </div>
              <div className={queueStyles.signalItem}>
                <span className={queueStyles.signalLabel}>Link check</span>
                <span className={queueStyles.signalValue}>Pending</span>
              </div>
              <div className={queueStyles.signalItem}>
                <span className={queueStyles.signalLabel}>Completeness</span>
                <span className={queueStyles.signalValue}>70%</span>
              </div>
            </div>
          </div>

          <div className={queueStyles.scoreBlock}>
            <div className={queueStyles.sectionLabel}>SCORE</div>
            <div className={queueStyles.scoreValue}>Readiness 3.1 / 5</div>
          </div>

          {decisions['munshi-books'] ? (
            <div className={queueStyles.decidedNotice}>
              Decided as <strong>{decisions['munshi-books']}</strong>. Rejection is final.
            </div>
          ) : (
            <>
              <div className={queueStyles.reasonBlock}>
                <div className={queueStyles.sectionLabel}>REASON (REQUIRED)</div>
                <textarea
                  className={queueStyles.reasonInput}
                  placeholder="Enter reason for decision..."
                  value={reasons['munshi-books']}
                  onChange={(e) => handleReasonChange('munshi-books', e.target.value)}
                  aria-label="Reason for decision on Munshi Books"
                />
              </div>

              <div className={queueStyles.actionsRow}>
                <button
                  type="button"
                  className={queueStyles.rejectBtnWrapper}
                  onClick={() => handleDecision('munshi-books', 'rejected', false)}
                  aria-label="Reject profile"
                >
                  <span className={queueStyles.rejectTitle}>Reject</span>
                  <span className={queueStyles.rejectNotice}>Rejection is final. The user cannot appeal.</span>
                </button>
                <button
                  type="button"
                  className={queueStyles.approveBtn}
                  onClick={() => handleDecision('munshi-books', 'approved', false)}
                >
                  Approve
                </button>
              </div>
            </>
          )}
        </div>

        {/* Card 2: Nida Farooq */}
        <div className={queueStyles.reviewCard}>
          <div className={queueStyles.cardHeader}>
            <div>
              <h2 className={queueStyles.entityName}>Nida Farooq</h2>
              <div className={queueStyles.entitySubtitle}>Talent profile</div>
            </div>
            <Badge variant="accent">Appeal</Badge>
          </div>

          <div>
            <div className={queueStyles.sectionLabel}>CURRENT STATUS</div>
            <div className={queueStyles.statusRow} style={{ marginTop: '4px' }}>
              <Badge variant="default">Appeal pending</Badge>
              <span>Auto-rejected: Product link unreachable</span>
            </div>
          </div>

          <div>
            <div className={queueStyles.sectionLabel}>SIGNALS</div>
            <div className={queueStyles.signalsGrid}>
              <div className={queueStyles.signalItem}>
                <span className={queueStyles.signalLabel}>LinkedIn</span>
                <span className={queueStyles.signalValue}>Connected</span>
              </div>
              <div className={queueStyles.signalItem}>
                <span className={queueStyles.signalLabel}>Link check</span>
                <span className={queueStyles.signalValue} style={{ color: 'var(--color-danger)' }}>Failed</span>
              </div>
              <div className={queueStyles.signalItem}>
                <span className={queueStyles.signalLabel}>Completeness</span>
                <span className={queueStyles.signalValue}>85%</span>
              </div>
            </div>
          </div>

          <div className={queueStyles.scoreBlock}>
            <div className={queueStyles.sectionLabel}>SCORE</div>
            <div className={queueStyles.scoreValue}>Profile strength 85%</div>
          </div>

          {decisions['nida-farooq'] ? (
            <div className={queueStyles.decidedNotice}>
              Decided as <strong>{decisions['nida-farooq']}</strong>. Rejection is final.
            </div>
          ) : (
            <>
              <div className={queueStyles.reasonBlock}>
                <div className={queueStyles.sectionLabel}>REASON (REQUIRED)</div>
                <textarea
                  className={queueStyles.reasonInput}
                  placeholder="Enter reason for decision..."
                  value={reasons['nida-farooq']}
                  onChange={(e) => handleReasonChange('nida-farooq', e.target.value)}
                  aria-label="Reason for decision on Nida Farooq"
                />
              </div>

              <div className={queueStyles.actionsRow}>
                <button
                  type="button"
                  className={queueStyles.rejectBtnWrapper}
                  onClick={() => handleDecision('nida-farooq', 'rejected', true)}
                  aria-label="Reject profile"
                >
                  <span className={queueStyles.rejectTitle}>Reject</span>
                  <span className={queueStyles.rejectNotice}>Rejection is final. The user cannot appeal.</span>
                </button>
                <button
                  type="button"
                  className={queueStyles.approveBtn}
                  onClick={() => handleDecision('nida-farooq', 'approved', true)}
                >
                  Approve
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
