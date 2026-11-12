'use client';

import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui';
import Link from 'next/link';
import styles from './ReadinessScore.module.css';

interface DimensionData {
  title: string;
  score: number;
  narrative: string;
  gapText: string;
  actionText: string;
}

const DIMENSIONS: DimensionData[] = [
  {
    title: 'Problem clarity',
    score: 4,
    narrative: 'The pain point is clear, the target user is well-defined, and the problem statement is concise enough for a first conversation.',
    gapText: 'Gap: no customer quote',
    actionText: 'Suggested next action',
  },
  {
    title: 'Market definition',
    score: 2,
    narrative: 'The market is mentioned, but sizing, competition, and expansion vectors are not yet defined with enough precision.',
    gapText: 'Gap: no market sizing',
    actionText: 'Suggested next action',
  },
  {
    title: 'Differentiation',
    score: 3,
    narrative: 'The solution is easy to understand, but the unique advantage over existing alternatives still feels more claimed than proven.',
    gapText: 'Gap: no competitive edge',
    actionText: 'Suggested next action',
  },
  {
    title: 'Business model',
    score: 3,
    narrative: 'Revenue mechanics are visible, but pricing, unit economics, and customer acquisition cost assumptions are still rough.',
    gapText: 'Gap: no pricing logic',
    actionText: 'Suggested next action',
  },
  {
    title: 'Traction',
    score: 3,
    narrative: 'Early pilot results are described, but the numbers are not yet tied to revenue or growth over time.',
    gapText: 'Gap: no growth trend',
    actionText: 'Suggested next action',
  },
  {
    title: 'Team',
    score: 4,
    narrative: 'The founding team covers product and engineering, and roles and responsibilities are clearly assigned.',
    gapText: 'Gap: no advisor listed',
    actionText: 'Suggested next action',
  },
  {
    title: 'Go-to-market',
    score: 3,
    narrative: 'Initial channels are named, but cost per acquisition and a partner plan are not yet specified.',
    gapText: 'Gap: no channel cost',
    actionText: 'Suggested next action',
  },
];

export default function ReadinessScorePage() {
  return (
    <div className={styles.container}>
      <PageHeader
        title="Readiness score"
        subtitle="A rubric-based guide to where your startup stands. It is not a funding probability."
      />

      <div className={styles.mainLayout}>
        {/* Left: 7 Dimensions 2-column grid */}
        <div className={styles.dimensionsGrid}>
          {DIMENSIONS.map((dim) => (
            <div key={dim.title} className={styles.dimensionCard}>
              <div className={styles.headerRow}>
                <span className={styles.dimensionTitle}>{dim.title}</span>
                <span className={styles.scoreFraction}>{dim.score} / 5</span>
              </div>

              <div className={styles.track}>
                <div
                  className={styles.bar}
                  style={{ width: `${(dim.score / 5) * 100}%` }}
                />
              </div>

              <p className={styles.narrative}>{dim.narrative}</p>

              <div>
                <span className={styles.gapPill}>{dim.gapText}</span>
              </div>

              <button
                type="button"
                className={styles.actionLink}
                onClick={() => alert(`${dim.actionText} for ${dim.title}`)}
                style={{ background: 'none', border: 'none', padding: 0, textAlign: 'left' }}
              >
                {dim.actionText}
              </button>
            </div>
          ))}
        </div>

        {/* Right sidebar summary card & recalculate */}
        <div className={styles.sidebarCol}>
          <div className={styles.summaryCard}>
            <div className={styles.summaryTitle}>Summary</div>
            <div className={styles.bigScore}>3.1 / 5</div>
            <p className={styles.summaryText}>
              Average across the seven dimensions. Strongest on problem clarity and team; market definition needs the most evidence.
            </p>
            <Link href="/founder/pitch">
              <Button variant="primary" block>
                Practice your pitch
              </Button>
            </Link>
          </div>

          <Button
            variant="secondary"
            block
            onClick={() => alert('Recalculating readiness score against latest profile data...')}
          >
            Recalculate score
          </Button>
        </div>
      </div>
    </div>
  );
}
