'use client';

import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import styles from './PitchFeedback.module.css';

export default function PitchFeedbackPage() {
  const router = useRouter();

  const [nextSteps, setNextSteps] = useState([
    { id: '1', text: 'Add a one-sentence market sizing claim to your opening pitch.', checked: false },
    { id: '2', text: 'Prepare one defensibility example and one paid acquisition example.', checked: false },
    { id: '3', text: 'Practice answering scaling questions with a specific metric and next step.', checked: false },
  ]);

  const toggleStep = (id: string) => {
    setNextSteps((prev) =>
      prev.map((s) => (s.id === id ? { ...s, checked: !s.checked } : s))
    );
  };

  return (
    <div className={styles.container}>
      <PageHeader
        title="Session feedback"
        subtitle="Investor persona: Seed-stage fintech investor | Session 3 of 3"
      />

      <div className={styles.mainLayout}>
        {/* Left column */}
        <div className={styles.leftCol}>
          {/* Feedback by rubric */}
          <div className={styles.card}>
            <div className={styles.headerRow}>
              <span className={styles.cardTitle}>Feedback by rubric</span>
              <span className={styles.averageText}>
                Session average <span className={styles.averageScore}>3.0 / 5</span>
              </span>
            </div>

            <div className={styles.rubricList}>
              <div className={styles.rubricItem}>
                <div className={styles.itemHeader}>
                  <span>Clarity</span>
                  <span style={{ fontWeight: 'var(--font-weight-bold)' }}>4 / 5</span>
                </div>
                <div className={styles.track}>
                  <div className={styles.bar} style={{ width: '80%' }} />
                </div>
                <p className={styles.feedbackNote}>
                  Your opening sentence was concise and easy to follow. Keep the core value proposition this clear.
                </p>
              </div>

              <div className={styles.rubricItem}>
                <div className={styles.itemHeader}>
                  <span>Market understanding</span>
                  <span style={{ fontWeight: 'var(--font-weight-bold)' }}>3 / 5</span>
                </div>
                <div className={styles.track}>
                  <div className={styles.bar} style={{ width: '60%' }} />
                </div>
                <p className={styles.feedbackNote}>
                  You mentioned fintech founders, but did not quantify the addressable market or competitive gap clearly.
                </p>
              </div>

              <div className={styles.rubricItem}>
                <div className={styles.itemHeader}>
                  <span>Defensibility of numbers</span>
                  <span style={{ fontWeight: 'var(--font-weight-bold)' }}>3 / 5</span>
                </div>
                <div className={styles.track}>
                  <div className={styles.bar} style={{ width: '60%' }} />
                </div>
                <p className={styles.feedbackNote}>
                  Mentioning 85% month-over-month retention helped, but you did not explain how that converts into revenue.
                </p>
              </div>

              <div className={styles.rubricItem}>
                <div className={styles.itemHeader}>
                  <span>Handling pushback</span>
                  <span style={{ fontWeight: 'var(--font-weight-bold)' }}>2 / 5</span>
                </div>
                <div className={styles.track}>
                  <div className={styles.bar} style={{ width: '40%' }} />
                </div>
                <p className={styles.feedbackNote}>
                  When asked about scaling beyond the pilot, your answer felt rushed and lacked a clear go-to-market plan.
                </p>
              </div>
            </div>
          </div>

          {/* Questions you struggled with */}
          <div className={styles.card}>
            <div className={styles.cardTitle}>Questions you struggled with</div>
            <div className={styles.struggledList}>
              <div className={styles.struggledItem}>
                <span className={styles.struggledIcon}>&#10003;</span>
                <div className={styles.struggledContent}>
                  <span className={styles.questionText}>
                    What makes your solution defensible, and how do you plan to acquire users at scale?
                  </span>
                  <span className={styles.suggestionText}>
                    Suggest: name one moat, then explain one paid and one organic acquisition channel.
                  </span>
                </div>
              </div>

              <div className={styles.struggledItem}>
                <span className={styles.struggledIcon}>&#10003;</span>
                <div className={styles.struggledContent}>
                  <span className={styles.questionText}>
                    How do you plan to move from a small pilot to a larger market?
                  </span>
                  <span className={styles.suggestionText}>
                    Suggest: describe one partner channel and one paid channel with a rough customer acquisition cost.
                  </span>
                </div>
              </div>

              <div className={styles.struggledItem}>
                <span className={styles.struggledIcon}>&#10003;</span>
                <div className={styles.struggledContent}>
                  <span className={styles.questionText}>
                    Retention is strong, but how do you plan to move from a small pilot to a larger market?
                  </span>
                  <span className={styles.suggestionText}>
                    Suggest: give a specific expansion metric and explain how the pilot informs the next stage.
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Transcript */}
          <div className={styles.card}>
            <div className={styles.cardTitle}>Transcript</div>
            <div>
              <button
                type="button"
                className={styles.transcriptLink}
                onClick={() => alert('Transcript: Full conversation loaded.')}
                style={{ background: 'none', border: 'none', padding: 0 }}
              >
                View full transcript
              </button>
            </div>
          </div>
        </div>

        {/* Right column */}
        <div className={styles.rightCol}>
          {/* Progress across sessions */}
          <div className={styles.card}>
            <div className={styles.cardTitle}>Progress across sessions</div>

            <div className={styles.progressItem}>
              <div className={styles.progressItemHeader}>
                <span className={styles.sessionDate}>Session 1 &bull; 02 Mar 2026</span>
                <span className={styles.sessionScore}>2.5 / 5</span>
              </div>
              <div className={styles.track}>
                <div className={styles.bar} style={{ width: '50%' }} />
              </div>
            </div>

            <div className={styles.progressItem}>
              <div className={styles.progressItemHeader}>
                <span className={styles.sessionDate}>Session 2 &bull; 08 Mar 2026</span>
                <span className={styles.sessionScore}>2.8 / 5</span>
              </div>
              <div className={styles.track}>
                <div className={styles.bar} style={{ width: '56%' }} />
              </div>
            </div>

            <div className={styles.progressItem}>
              <div className={styles.progressItemHeader}>
                <span className={styles.sessionDate}>Session 3 &bull; 12 Mar 2026</span>
                <span className={styles.sessionScore}>3.0 / 5</span>
              </div>
              <div className={styles.track}>
                <div className={styles.bar} style={{ width: '60%' }} />
              </div>
            </div>
          </div>

          {/* Next steps */}
          <div className={styles.card}>
            <div className={styles.cardTitle}>Next steps</div>
            <div className={styles.checklist}>
              {nextSteps.map((step) => (
                <label key={step.id} className={styles.checklistItem}>
                  <input
                    type="checkbox"
                    checked={step.checked}
                    onChange={() => toggleStep(step.id)}
                    className={styles.checkboxInput}
                  />
                  <span style={{ textDecoration: step.checked ? 'line-through' : 'none', opacity: step.checked ? 0.6 : 1 }}>
                    {step.text}
                  </span>
                </label>
              ))}
            </div>
          </div>

          <Link href="/founder/pitch">
            <Button variant="primary" block>
              Practice again
            </Button>
          </Link>

          <Button variant="secondary" block onClick={() => router.push('/founder/dashboard')}>
            Back to dashboard
          </Button>
        </div>
      </div>
    </div>
  );
}
