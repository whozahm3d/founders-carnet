'use client';

import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui';
import Link from 'next/link';
import styles from './TalentDashboard.module.css';

export default function TalentDashboardPage() {
  return (
    <div className={styles.dashboard}>
      <PageHeader
        title="Dashboard"
        subtitle="Track your profile, applications, and recommended startup tech roles."
      />

      {/* Verified Banner */}
      <div className={styles.verifiedBanner}>
        <div>
          <div className={styles.verifiedTitle}>Verified</div>
          <div className={styles.verifiedSubtitle}>Your profile is verified. You can browse and apply to startup jobs.</div>
        </div>
        <span className={styles.verifiedBadge}>Verified</span>
      </div>

      {/* Top 3 Cards Row */}
      <div className={styles.topRowGrid}>
        {/* Profile Strength */}
        <div className={styles.card}>
          <div className={styles.cardTitle}>Profile strength</div>
          <div className={styles.bigPercent}>70% complete</div>
          <div className={styles.scoreTrack}>
            <div className={styles.scoreBar} style={{ width: '70%' }} />
          </div>
          <Link href="/talent/profile" className={styles.cardLink}>
            Complete profile
          </Link>
        </div>

        {/* Resume Optimizer */}
        <div className={styles.card}>
          <div className={styles.cardTitle}>Resume optimizer</div>
          <div className={styles.cardSubtitle}>Get line-by-line suggestions for startup tech roles</div>
          <div>
            <span className={styles.paidTierPill}>
              <span>&#128274;</span> Paid tier
            </span>
          </div>
          <div style={{ marginTop: 'auto' }}>
            <Button variant="primary" block onClick={() => alert('Paid tier modal')}>
              See paid tier
            </Button>
          </div>
        </div>

        {/* Applications */}
        <div className={styles.card}>
          <div className={styles.cardTitle}>Applications</div>
          <div className={styles.applicationsList}>
            <div className={styles.applicationRow}>
              <div>
                <div className={styles.companyName}>Mehran Works</div>
                <div className={styles.jobTitle}>Data Analyst Intern</div>
              </div>
              <span className={styles.statusApplied}>Applied</span>
            </div>

            <div className={styles.applicationRow}>
              <div>
                <div className={styles.companyName}>Ravi Health</div>
                <div className={styles.jobTitle}>DevOps Engineer</div>
              </div>
              <span className={styles.statusReview}>In review</span>
            </div>

            <div className={styles.applicationRow}>
              <div>
                <div className={styles.companyName}>Kaarwan Systems</div>
                <div className={styles.jobTitle}>Backend Engineer Intern</div>
              </div>
              <span className={styles.statusClosed}>Closed</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recommended Jobs */}
      <div>
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>Recommended jobs</h2>
          <Link href="/talent/jobs" className={styles.cardLink}>
            Browse all jobs
          </Link>
        </div>

        <div className={styles.jobList}>
          <div className={styles.jobCard}>
            <div className={styles.jobInfo}>
              <div className={styles.jobCardTitle}>Software Engineering Intern</div>
              <div className={styles.jobCompany}>Chenab Pay</div>
              <div className={styles.jobLocation}>Lahore</div>
              <div className={styles.tagRow}>
                <span className={styles.tagPill}>Internship</span>
                <span className={styles.tagPill}>Hybrid</span>
              </div>
            </div>
            <button
              type="button"
              className={styles.viewBtn}
              onClick={() => alert('View Software Engineering Intern')}
            >
              View
            </button>
          </div>

          <div className={styles.jobCard}>
            <div className={styles.jobInfo}>
              <div className={styles.jobCardTitle}>Machine Learning Intern</div>
              <div className={styles.jobCompany}>Rozgar Labs</div>
              <div className={styles.jobLocation}>Remote (Pakistan)</div>
              <div className={styles.tagRow}>
                <span className={styles.tagPill}>Internship</span>
                <span className={styles.tagPill}>Remote</span>
              </div>
            </div>
            <button
              type="button"
              className={styles.viewBtn}
              onClick={() => alert('View Machine Learning Intern')}
            >
              View
            </button>
          </div>

          <div className={styles.jobCard}>
            <div className={styles.jobInfo}>
              <div className={styles.jobCardTitle}>QA Engineer Intern</div>
              <div className={styles.jobCompany}>Abhi</div>
              <div className={styles.jobLocation}>Lahore</div>
              <div className={styles.tagRow}>
                <span className={styles.tagPill}>Internship</span>
                <span className={styles.tagPill}>Hybrid</span>
              </div>
            </div>
            <button
              type="button"
              className={styles.viewBtn}
              onClick={() => alert('View QA Engineer Intern')}
            >
              View
            </button>
          </div>
        </div>
      </div>

      {/* Mentor Guidance */}
      <div className={styles.mentorCard}>
        <div className={styles.cardTitle}>Mentor guidance</div>
        <Button variant="secondary" onClick={() => alert('Search mentors')}>
          Find a mentor
        </Button>
      </div>
    </div>
  );
}
