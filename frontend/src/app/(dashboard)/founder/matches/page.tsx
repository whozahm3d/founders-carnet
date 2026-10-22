'use client';

import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui';
import { useState } from 'react';
import styles from './MatchFeed.module.css';

interface MatchItem {
  id: string;
  initials: string;
  name: string;
  role: 'Investor' | 'Mentor';
  isVerified: boolean;
  similarity: number;
  factors: string[];
  contactStatus: 'locked' | 'requested' | 'accepted';
  email?: string;
  phone?: string;
}

const INITIAL_MATCHES: MatchItem[] = [
  {
    id: '1',
    initials: 'AQ',
    name: 'Ayesha Qureshi',
    role: 'Investor',
    isVerified: true,
    similarity: 92,
    factors: ['strong sector fit', 'compatible stage', 'skill overlap'],
    contactStatus: 'locked',
  },
  {
    id: '2',
    initials: 'HI',
    name: 'Hamza Iqbal',
    role: 'Mentor',
    isVerified: true,
    similarity: 88,
    factors: ['strong sector fit', 'compatible stage', 'skill overlap'],
    contactStatus: 'locked',
  },
  {
    id: '3',
    initials: 'SR',
    name: 'Sana Rauf',
    role: 'Investor',
    isVerified: true,
    similarity: 84,
    factors: ['strong sector fit', 'compatible stage', 'skill overlap'],
    contactStatus: 'requested',
  },
  {
    id: '4',
    initials: 'PS',
    name: 'Priya Shah',
    role: 'Mentor',
    isVerified: true,
    similarity: 76,
    factors: ['strong sector fit', 'compatible stage', 'skill overlap'],
    contactStatus: 'accepted',
    email: 'priya.shah@example.pk',
    phone: '+92 300 1234567',
  },
];

export default function FounderMatchesPage() {
  const [filterType, setFilterType] = useState<'All' | 'Mentors' | 'Investors'>('All');
  const [sectorFilter, setSectorFilter] = useState('All');
  const [stageFilter, setStageFilter] = useState('All');
  const [matches, setMatches] = useState<MatchItem[]>(INITIAL_MATCHES);

  const handleRequestMatch = (id: string) => {
    setMatches((prev) =>
      prev.map((m) => (m.id === id ? { ...m, contactStatus: 'requested' } : m))
    );
  };

  const filteredMatches = matches.filter((m) => {
    if (filterType === 'Mentors' && m.role !== 'Mentor') return false;
    if (filterType === 'Investors' && m.role !== 'Investor') return false;
    return true;
  });

  return (
    <div className={styles.container}>
      <PageHeader
        title="Matches"
        subtitle="Ranked by sector, stage, and expertise fit. Percentages show profile similarity, not the likelihood of a successful match."
      />

      {/* Filter Row */}
      <div className={styles.filtersRow}>
        <button
          type="button"
          className={`${styles.filterPill} ${filterType === 'All' ? styles.filterPillActive : ''}`}
          onClick={() => setFilterType('All')}
        >
          All
        </button>
        <button
          type="button"
          className={`${styles.filterPill} ${filterType === 'Mentors' ? styles.filterPillActive : ''}`}
          onClick={() => setFilterType('Mentors')}
        >
          Mentors
        </button>
        <button
          type="button"
          className={`${styles.filterPill} ${filterType === 'Investors' ? styles.filterPillActive : ''}`}
          onClick={() => setFilterType('Investors')}
        >
          Investors
        </button>

        <select
          value={sectorFilter}
          onChange={(e) => setSectorFilter(e.target.value)}
          className={styles.filterDropdown}
        >
          <option value="All">Sector</option>
          <option value="Fintech">Fintech</option>
          <option value="SaaS">SaaS</option>
          <option value="Healthtech">Healthtech</option>
        </select>

        <select
          value={stageFilter}
          onChange={(e) => setStageFilter(e.target.value)}
          className={styles.filterDropdown}
        >
          <option value="All">Stage</option>
          <option value="Pre-seed">Pre-seed</option>
          <option value="Seed">Seed</option>
          <option value="Series A">Series A</option>
        </select>
      </div>

      {/* Match Feed Cards */}
      <div className={styles.feedList}>
        {filteredMatches.map((m) => (
          <div key={m.id} className={styles.matchFeedCard}>
            <div className={styles.cardTopRow}>
              <div className={styles.userBioRow}>
                <div className={styles.avatarCircle}>{m.initials}</div>
                <div className={styles.userNameArea}>
                  <div className={styles.nameRow}>
                    <span className={styles.nameText}>{m.name}</span>
                    <span className={styles.roleTag}>{m.role}</span>
                    {m.isVerified && <span className={styles.verifiedTag}>Verified</span>}
                  </div>
                </div>
              </div>
              <div className={styles.similarityScore}>{m.similarity}% similarity</div>
            </div>

            <div className={styles.tagsRow}>
              {m.factors.map((f) => (
                <span key={f} className={styles.factorTag}>
                  {f}
                </span>
              ))}
            </div>

            <div className={styles.cardBottomRow}>
              {m.contactStatus === 'locked' && (
                <>
                  <div className={styles.contactNote}>
                    <span>&#128274;</span> Contact revealed on mutual accept
                  </div>
                  <Button variant="primary" size="sm" onClick={() => handleRequestMatch(m.id)}>
                    Request match
                  </Button>
                </>
              )}

              {m.contactStatus === 'requested' && (
                <>
                  <div className={styles.contactNote}>
                    <span>&#128274;</span> Contact revealed on mutual accept
                  </div>
                  <Button variant="secondary" size="sm" disabled>
                    Requested
                  </Button>
                </>
              )}

              {m.contactStatus === 'accepted' && (
                <>
                  <div className={styles.revealedContact}>
                    <span>&#9993;</span> {m.email} &bull; {m.phone}
                  </div>
                  <Button variant="secondary" size="sm" disabled>
                    Accepted
                  </Button>
                </>
              )}
            </div>
          </div>
        ))}

        {/* Empty state bottom card */}
        <div className={styles.emptyFeedCard}>
          <div className={styles.emptyTitle}>No more matches yet.</div>
          <div className={styles.emptyDesc}>Complete your profile to see more.</div>
        </div>
      </div>
    </div>
  );
}
