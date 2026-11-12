'use client';

import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui';
import { useState } from 'react';
import styles from './MentorDashboard.module.css';

export default function MentorDashboardPage() {
  const [openToMentees, setOpenToMentees] = useState(true);
  const [requestStatus, setRequestStatus] = useState<Record<string, 'accepted' | 'declined' | null>>({});

  const handleAction = (id: string, action: 'accepted' | 'declined') => {
    setRequestStatus((prev) => ({ ...prev, [id]: action }));
  };

  return (
    <div className={styles.dashboard}>
      <PageHeader
        title="Dashboard"
        subtitle="Your profile is verified by admin and visible to founders."
        action={
          <span style={{ backgroundColor: '#ffffff', border: '1px solid var(--color-border)', borderRadius: 'var(--radius-full)', padding: '4px 12px', fontSize: 'var(--font-size-xs)' }}>
            Verified
          </span>
        }
      />

      {/* Top 3 Stat Cards */}
      <div className={styles.topStatsRow}>
        <div className={styles.statCard}>
          <span className={styles.statLabel}>New requests</span>
          <span className={styles.statNumber}>3</span>
        </div>

        <div className={styles.statCard}>
          <span className={styles.statLabel}>Active matches</span>
          <span className={styles.statNumber}>6</span>
        </div>

        <div className={styles.availabilityCard}>
          <div>
            <div style={{ fontSize: 'var(--font-size-sm)', fontWeight: 'var(--font-weight-bold)' }}>Availability</div>
            <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)' }}>Open to new mentees</div>
          </div>
          <div
            className={`${styles.toggleSwitch} ${!openToMentees ? styles.toggleSwitchOff : ''}`}
            onClick={() => setOpenToMentees(!openToMentees)}
            role="switch"
            aria-checked={openToMentees}
          >
            <div className={`${styles.toggleKnob} ${!openToMentees ? styles.toggleKnobOff : ''}`} />
          </div>
        </div>
      </div>

      {/* Two Column Layout */}
      <div className={styles.mainLayout}>
        {/* Left: Recommended founders and talent */}
        <div className={styles.recommendedCard}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>Recommended founders and talent</h2>
            <button type="button" className={styles.viewAllLink} onClick={() => alert('View all')}>
              View all
            </button>
          </div>

          {/* Profile 1 */}
          <div className={styles.profileItem}>
            <div className={styles.profileInfo}>
              <div className={styles.avatarBox}>FP</div>
              <div>
                <div style={{ display: 'flex', alignItems: 'center' }}>
                  <span style={{ fontSize: 'var(--font-size-sm)', fontWeight: 'var(--font-weight-bold)' }}>
                    1. Founder Profile
                  </span>
                  <span className={styles.roleTag}>Founder</span>
                </div>
                <div className={styles.sectorStageText}>SaaS &bull; Seed</div>
                <div className={styles.similarityText}>92% similarity</div>
              </div>
            </div>

            <div className={styles.fitTags}>
              <span className={styles.fitPill}>strong sector fit</span>
              <span className={styles.fitPill}>needs fundraising help</span>
              <button type="button" className={styles.viewProfileLink} onClick={() => alert('View founder profile')}>
                View profile
              </button>
            </div>
          </div>

          {/* Profile 2 */}
          <div className={styles.profileItem}>
            <div className={styles.profileInfo}>
              <div className={styles.avatarBox}>TP</div>
              <div>
                <div style={{ display: 'flex', alignItems: 'center' }}>
                  <span style={{ fontSize: 'var(--font-size-sm)', fontWeight: 'var(--font-weight-bold)' }}>
                    2. Talent Profile
                  </span>
                  <span className={styles.roleTag}>Talent</span>
                </div>
                <div className={styles.sectorStageText}>Healthtech &bull; Series A</div>
                <div className={styles.similarityText}>88% similarity</div>
              </div>
            </div>

            <div className={styles.fitTags}>
              <span className={styles.fitPill}>strong sector fit</span>
              <span className={styles.fitPill}>needs hiring guidance</span>
              <button type="button" className={styles.viewProfileLink} onClick={() => alert('View talent profile')}>
                View profile
              </button>
            </div>
          </div>

          {/* Profile 3 */}
          <div className={styles.profileItem}>
            <div className={styles.profileInfo}>
              <div className={styles.avatarBox}>FP</div>
              <div>
                <div style={{ display: 'flex', alignItems: 'center' }}>
                  <span style={{ fontSize: 'var(--font-size-sm)', fontWeight: 'var(--font-weight-bold)' }}>
                    3. Founder Profile
                  </span>
                  <span className={styles.roleTag}>Founder</span>
                </div>
                <div className={styles.sectorStageText}>Agritech &bull; Pre-seed</div>
                <div className={styles.similarityText}>84% similarity</div>
              </div>
            </div>

            <div className={styles.fitTags}>
              <span className={styles.fitPill}>strong stage fit</span>
              <span className={styles.fitPill}>needs product feedback</span>
              <button type="button" className={styles.viewProfileLink} onClick={() => alert('View founder profile')}>
                View profile
              </button>
            </div>
          </div>
        </div>

        {/* Right column: Pending requests & Your expertise */}
        <div className={styles.rightCol}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>Pending requests</h2>
            <button type="button" className={styles.viewAllLink} onClick={() => alert('View all requests')}>
              View all
            </button>
          </div>

          {/* Request 1 */}
          <div className={styles.requestCard}>
            <div className={styles.requestName}>Founder Profile</div>
            <p className={styles.requestDesc}>
              Needs fundraising guidance and pitch feedback for a seed round.
            </p>
            {requestStatus['req1'] ? (
              <span style={{ fontSize: 'var(--font-size-xs)', fontWeight: 'var(--font-weight-semibold)', color: 'var(--color-accent)' }}>
                {requestStatus['req1'] === 'accepted' ? 'Accepted' : 'Declined'}
              </span>
            ) : (
              <div className={styles.requestButtons}>
                <Button variant="primary" size="sm" onClick={() => handleAction('req1', 'accepted')}>
                  Accept
                </Button>
                <Button variant="secondary" size="sm" onClick={() => handleAction('req1', 'declined')}>
                  Decline
                </Button>
              </div>
            )}
          </div>

          {/* Request 2 */}
          <div className={styles.requestCard}>
            <div className={styles.requestName}>Talent Profile</div>
            <p className={styles.requestDesc}>
              Looking for career transition advice and startup hiring insights.
            </p>
            {requestStatus['req2'] ? (
              <span style={{ fontSize: 'var(--font-size-xs)', fontWeight: 'var(--font-weight-semibold)', color: 'var(--color-accent)' }}>
                {requestStatus['req2'] === 'accepted' ? 'Accepted' : 'Declined'}
              </span>
            ) : (
              <div className={styles.requestButtons}>
                <Button variant="primary" size="sm" onClick={() => handleAction('req2', 'accepted')}>
                  Accept
                </Button>
                <Button variant="secondary" size="sm" onClick={() => handleAction('req2', 'declined')}>
                  Decline
                </Button>
              </div>
            )}
          </div>

          {/* Request 3 */}
          <div className={styles.requestCard}>
            <div className={styles.requestName}>Founder Profile</div>
            <p className={styles.requestDesc}>
              Wants product strategy input and operational scaling guidance.
            </p>
            {requestStatus['req3'] ? (
              <span style={{ fontSize: 'var(--font-size-xs)', fontWeight: 'var(--font-weight-semibold)', color: 'var(--color-accent)' }}>
                {requestStatus['req3'] === 'accepted' ? 'Accepted' : 'Declined'}
              </span>
            ) : (
              <div className={styles.requestButtons}>
                <Button variant="primary" size="sm" onClick={() => handleAction('req3', 'accepted')}>
                  Accept
                </Button>
                <Button variant="secondary" size="sm" onClick={() => handleAction('req3', 'declined')}>
                  Decline
                </Button>
              </div>
            )}
          </div>

          <div className={styles.mutualNotice}>
            Contact details are revealed only after you both accept.
          </div>

          {/* Your expertise */}
          <div className={styles.expertiseCard}>
            <h3 style={{ fontSize: 'var(--font-size-sm)', fontWeight: 'var(--font-weight-bold)' }}>Your expertise</h3>
            <div className={styles.expertiseTags}>
              <span className={styles.expertisePill}>Fundraising</span>
              <span className={styles.expertisePill}>Product</span>
              <span className={styles.expertisePill}>Operations</span>
              <span className={styles.expertisePill}>Financial management</span>
              <span className={styles.expertisePill}>HR and team-building</span>
            </div>
            <div>
              <button type="button" className={styles.editExpertiseLink} onClick={() => alert('Edit expertise')}>
                Edit expertise
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
