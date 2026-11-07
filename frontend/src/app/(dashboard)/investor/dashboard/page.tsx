'use client';

import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui';
import { useState } from 'react';
import styles from './InvestorDashboard.module.css';

interface FounderMatch {
  rank: number;
  initial: string;
  name: string;
  desc: string;
  tags: string[];
  score: number;
  similarity: number;
}

const FOUNDERS: FounderMatch[] = [
  {
    rank: 1,
    initial: 'N',
    name: 'NovaPay',
    desc: 'Digital wallet for unbanked communities.',
    tags: ['Fintech', 'Seed'],
    score: 4.2,
    similarity: 95,
  },
  {
    rank: 2,
    initial: 'S',
    name: 'SaaSFlow',
    desc: 'Automated accounting workflows for e-commerce founders.',
    tags: ['B2B SaaS', 'Seed'],
    score: 3.9,
    similarity: 88,
  },
  {
    rank: 3,
    initial: 'C',
    name: 'CryptoHive',
    desc: 'Institutional trading infrastructure for crypto markets.',
    tags: ['Fintech', 'Seed'],
    score: 3.6,
    similarity: 82,
  },
  {
    rank: 4,
    initial: 'M',
    name: 'MediLink',
    desc: 'Telehealth platform connecting rural patients to specialists.',
    tags: ['B2B SaaS', 'Seed'],
    score: 3.3,
    similarity: 75,
  },
];

export default function InvestorDashboardPage() {
  const [requestedIds, setRequestedIds] = useState<number[]>([]);

  const handleRequest = (rank: number) => {
    setRequestedIds((prev) => [...prev, rank]);
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

      <div className={styles.topRowLayout}>
        <div className={styles.topLeftCol}>
          {/* Top 3 Stat Cards */}
          <div className={styles.statsRow}>
            <div className={styles.statCard}>
              <span className={styles.statLabel}>Verified Founders</span>
              <span className={styles.statNumber}>18</span>
            </div>
            <div className={styles.statCard}>
              <span className={styles.statLabel}>Pending Match Requests</span>
              <span className={styles.statNumber}>1</span>
            </div>
            <div className={styles.statCard}>
              <span className={styles.statLabel}>Accepted Matches</span>
              <span className={styles.statNumber}>1</span>
            </div>
          </div>

          {/* Investment Profile */}
          <div className={styles.investmentProfileCard}>
            <div className={styles.cardTitle}>Investment Profile</div>
            <div className={styles.thesisTagsRow}>
              <span className={styles.thesisTag}>Thesis: Fintech, SaaS</span>
              <span className={styles.thesisTag}>Stage: Seed</span>
              <span className={styles.thesisTag}>Ticket: PKR 2M to 10M</span>
              <span className={styles.thesisTag}>Geography: Pakistan</span>
            </div>
            <button
              type="button"
              className={styles.editLink}
              onClick={() => alert('Edit investment profile')}
            >
              Edit investment profile
            </button>
          </div>
        </div>

        {/* Right Match Requests */}
        <div className={styles.requestsCard}>
          <div className={styles.cardTitle}>Match requests</div>

          <div className={styles.requestItem}>
            <div>
              <div className={styles.requestName}>Dastak Exchange</div>
              <div className={styles.requestSent}>Sent 2 days ago</div>
            </div>
            <span className={styles.statusPending}>Pending</span>
          </div>

          <div className={styles.requestItem}>
            <div>
              <div className={styles.requestName}>SaaSFlow</div>
              <div className={styles.requestSent}>Sent 1 week ago</div>
            </div>
            <span className={styles.statusAccepted}>Accepted</span>
          </div>

          <div className={styles.requestItem}>
            <div>
              <div className={styles.requestName}>CryptoHive</div>
              <div className={styles.requestSent}>Sent 2 weeks ago</div>
            </div>
            <span className={styles.statusDeclined}>Declined</span>
          </div>
        </div>
      </div>

      {/* Recommended founders table */}
      <div className={styles.foundersSection}>
        <div className={styles.sectionHeaderRow}>
          <div>
            <h2 className={styles.sectionHeading}>Recommended founders</h2>
            <div className={styles.sectionSubhead}>
              Only verified startups with a completed readiness assessment are shown.
            </div>
          </div>
          <span className={styles.matchesBadge}>4 Matches</span>
        </div>

        <div className={styles.founderList}>
          {FOUNDERS.map((f) => (
            <div key={f.rank} className={styles.founderRow}>
              <div className={styles.founderLeft}>
                <div className={styles.rankCircle}>{f.rank}</div>
                <div className={styles.initialAvatar}>{f.initial}</div>
                <div className={styles.founderMeta}>
                  <div className={styles.founderNameRow}>
                    <span className={styles.founderName}>{f.name}</span>
                    <span className={styles.aiPill}>AI-generated</span>
                  </div>
                  <div className={styles.founderDesc}>{f.desc}</div>
                  <div className={styles.sectorTags}>
                    {f.tags.map((t) => (
                      <span key={t} className={styles.miniTag}>
                        {t}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <div className={styles.scoreArea}>
                <span className={styles.readinessText}>{f.score} / 5</span>
                <div className={styles.scoreTrack}>
                  <div
                    className={styles.scoreBar}
                    style={{ width: `${(f.score / 5) * 100}%` }}
                  />
                </div>
              </div>

              <div className={styles.similarityCol}>
                <span className={styles.similarityPercent}>{f.similarity}% similarity</span>
                <div className={styles.fitTagsRow}>
                  <span className={styles.fitPill}>Thesis fit</span>
                  <span className={styles.fitPill}>Stage fit</span>
                </div>
              </div>

              <div className={styles.actionButtons}>
                <Button variant="secondary" size="sm" onClick={() => alert(`View ${f.name}`)}>
                  View founder
                </Button>
                <Button
                  variant="primary"
                  size="sm"
                  disabled={requestedIds.includes(f.rank)}
                  onClick={() => handleRequest(f.rank)}
                >
                  {requestedIds.includes(f.rank) ? 'Requested' : 'Request match'}
                </Button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
