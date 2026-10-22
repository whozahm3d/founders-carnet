'use client';

import { PageHeader } from '@/components/layout/PageHeader';
import { Card } from '@/components/ui';
import Link from 'next/link';
import { useState } from 'react';
import styles from './FounderDashboard.module.css';

export default function FounderDashboardPage() {
  const [actions, setActions] = useState([
    { id: '1', text: 'Add market sizing', completed: false },
    { id: '2', text: 'Practice a pitch', completed: false },
    { id: '3', text: 'Add a product link', completed: false },
  ]);

  const toggleAction = (id: string) => {
    setActions((prev) =>
      prev.map((item) => (item.id === id ? { ...item, completed: !item.completed } : item))
    );
  };

  return (
    <div className={styles.dashboard}>
      <PageHeader
        title="Dashboard"
        subtitle="Track your readiness, next actions, and investor matches from one place."
      />

      {/* Verified Banner */}
      <div className={styles.verifiedBanner}>
        <div>
          <div className={styles.verifiedTitle}>Verified</div>
          <div className={styles.verifiedSubtitle}>Your profile is verified and visible to investors.</div>
        </div>
        <span className={styles.verifiedBadge}>Verified</span>
      </div>

      {/* Top 3-Card Row */}
      <div className={styles.topRowGrid}>
        {/* 1. Readiness Score */}
        <Card>
          <div className={styles.cardTitle}>Readiness score</div>
          <div className={styles.cardSubtitle}>Average across 7 dimensions</div>

          <div className={styles.scoreRow}>
            <span className={styles.bigScore}>3.1 / 5</span>
            <span className={styles.percentText}>62%</span>
          </div>

          <div className={styles.scoreTrack}>
            <div className={styles.scoreBar} style={{ width: '62%' }} />
          </div>

          <div>
            <span className={styles.aiBadge}>AI-generated</span>
          </div>

          <Link href="/founder/readiness" className={styles.cardLink}>
            View breakdown
          </Link>
        </Card>

        {/* 2. Next Actions */}
        <Card>
          <div className={styles.cardTitle}>Next actions</div>
          <div className={styles.actionsList}>
            {actions.map((act) => (
              <label key={act.id} className={styles.actionItem}>
                <input
                  type="checkbox"
                  checked={act.completed}
                  onChange={() => toggleAction(act.id)}
                  className={styles.checkboxInput}
                />
                <span style={{ textDecoration: act.completed ? 'line-through' : 'none', opacity: act.completed ? 0.6 : 1 }}>
                  {act.text}
                </span>
              </label>
            ))}
          </div>
        </Card>

        {/* 3. Recent Pitch Feedback */}
        <Card>
          <div className={styles.cardTitle}>Recent pitch feedback</div>
          <div className={styles.pitchList}>
            <div className={styles.pitchRow}>
              <span className={styles.pitchDate}>12 Mar 2026</span>
              <span className={styles.pitchScore}>3.0 / 5</span>
            </div>
            <div className={styles.pitchRow}>
              <span className={styles.pitchDate}>08 Mar 2026</span>
              <span className={styles.pitchScore}>2.8 / 5</span>
            </div>
            <div className={styles.pitchRow}>
              <span className={styles.pitchDate}>02 Mar 2026</span>
              <span className={styles.pitchScore}>2.5 / 5</span>
            </div>
          </div>
          <Link href="/founder/feedback" className={styles.cardLink}>
            View latest feedback
          </Link>
        </Card>
      </div>

      {/* Match Preview Section */}
      <div>
        <div className={styles.matchSectionHeader}>
          <h2 className={styles.matchSectionTitle}>Match preview</h2>
          <Link href="/founder/matches" className={styles.cardLink}>
            View all matches
          </Link>
        </div>

        <div className={styles.matchGrid}>
          {/* Card 1 */}
          <div className={styles.matchCard}>
            <div className={styles.matchName}>Ayesha Qureshi</div>
            <div className={styles.matchRole}>Investor</div>
            <div className={styles.matchSimilarity}>92% similarity</div>
            <div className={styles.matchTags}>
              <span className={styles.matchTag}>sector fit</span>
              <span className={styles.matchTag}>stage fit</span>
            </div>
            <div className={styles.matchNote}>Contact revealed on mutual accept</div>
          </div>

          {/* Card 2 */}
          <div className={styles.matchCard}>
            <div className={styles.matchName}>Hamza Iqbal</div>
            <div className={styles.matchRole}>Mentor</div>
            <div className={styles.matchSimilarity}>88% similarity</div>
            <div className={styles.matchTags}>
              <span className={styles.matchTag}>sector fit</span>
              <span className={styles.matchTag}>stage fit</span>
            </div>
            <div className={styles.matchNote}>Contact revealed on mutual accept</div>
          </div>

          {/* Card 3 */}
          <div className={styles.matchCard}>
            <div className={styles.matchName}>Sana Rauf</div>
            <div className={styles.matchRole}>Investor</div>
            <div className={styles.matchSimilarity}>84% similarity</div>
            <div className={styles.matchTags}>
              <span className={styles.matchTag}>sector fit</span>
              <span className={styles.matchTag}>stage fit</span>
            </div>
            <div className={styles.matchNote}>Contact revealed on mutual accept</div>
          </div>
        </div>
      </div>
    </div>
  );
}
