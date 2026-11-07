'use client';

import { PageHeader } from '@/components/layout/PageHeader';
import { Input, Textarea, Select, Button } from '@/components/ui';
import { useState } from 'react';
import styles from './FounderProfile.module.css';

const SECTOR_OPTIONS = [
  { value: 'fintech', label: 'Fintech' },
  { value: 'edtech', label: 'Edtech' },
  { value: 'healthtech', label: 'Healthtech' },
  { value: 'saas', label: 'SaaS' },
  { value: 'aiml', label: 'AI/ML' },
  { value: 'ecommerce', label: 'E-commerce tech' },
  { value: 'agritech', label: 'Agritech' },
];

export default function FounderProfilePage() {
  const [startupName, setStartupName] = useState('Munshi Books');
  const [oneLine, setOneLine] = useState('Automated accounting workflows for e-commerce founders');
  const [sector, setSector] = useState('fintech');
  const [team, setTeam] = useState('Founding team covers product and engineering with ex-Careem operators.');
  const [productLink, setProductLink] = useState('https://munshibooks.pk');
  const [savedMessage, setSavedMessage] = useState('');

  const handleSaveDraft = (e: React.FormEvent) => {
    e.preventDefault();
    setSavedMessage('Draft saved successfully.');
    setTimeout(() => setSavedMessage(''), 3000);
  };

  const handleSubmitReview = (e: React.FormEvent) => {
    e.preventDefault();
    setSavedMessage('Profile submitted for human verification review.');
    setTimeout(() => setSavedMessage(''), 3000);
  };

  return (
    <div className={styles.container}>
      <PageHeader
        title="Startup profile"
        action={
          <span className={styles.pendingBadge}>Pending review</span>
        }
      />

      {savedMessage && (
        <div style={{ backgroundColor: 'var(--color-success-bg)', color: 'var(--color-success)', padding: 'var(--space-3) var(--space-4)', borderRadius: 'var(--radius-md)', fontSize: 'var(--font-size-xs)' }}>
          {savedMessage}
        </div>
      )}

      <div className={styles.twoColumnLayout}>
        {/* Left main form card */}
        <form className={styles.formCard}>
          <div className={styles.fieldGroup}>
            <label className={styles.fieldLabel} htmlFor="startup-name">Startup name</label>
            <Input
              id="startup-name"
              value={startupName}
              onChange={(e) => setStartupName(e.target.value)}
              placeholder="Enter your startup name"
            />
          </div>

          <div className={styles.fieldGroup}>
            <label className={styles.fieldLabel} htmlFor="one-line">One-line description</label>
            <Input
              id="one-line"
              value={oneLine}
              onChange={(e) => setOneLine(e.target.value)}
              placeholder="Short summary of what you build"
            />
          </div>

          <div className={styles.fieldGroup}>
            <label className={styles.fieldLabel} htmlFor="sector-select">Sector</label>
            <Select
              id="sector-select"
              value={sector}
              onChange={(e) => setSector(e.target.value)}
              options={SECTOR_OPTIONS}
              placeholder="Select sector"
            />
          </div>

          <div className={styles.fieldGroup}>
            <label className={styles.fieldLabel} htmlFor="team-desc">Team</label>
            <Textarea
              id="team-desc"
              value={team}
              onChange={(e) => setTeam(e.target.value)}
              placeholder="Describe the founding team, key hires, and operating setup"
              rows={4}
            />
          </div>

          <div className={styles.fieldGroup}>
            <label className={styles.fieldLabel} htmlFor="portfolio-link">Portfolio or product link (optional)</label>
            <Input
              id="portfolio-link"
              type="url"
              value={productLink}
              onChange={(e) => setProductLink(e.target.value)}
              placeholder="https://"
            />
            <span className={styles.fieldHint}>
              This link is optional. If you provide it, we&apos;ll check that it&apos;s reachable and consistent with your profile. Used only for verification, never shared publicly.
            </span>
          </div>

          <div className={styles.buttonRow}>
            <Button type="button" variant="secondary" onClick={handleSaveDraft}>
              Save draft
            </Button>
            <Button type="button" variant="primary" onClick={handleSubmitReview}>
              Submit for review
            </Button>
          </div>
        </form>

        {/* Right review status card */}
        <div className={styles.sidebarCard}>
          <div className={styles.sidebarTitle}>Review status</div>
          <span className={styles.pendingBadge}>Pending review</span>

          <p className={styles.reviewExplainer}>
            Most profiles are verified instantly. Anything unclear gets a real second look from a person.
          </p>

          <div className={styles.checklist}>
            <div className={styles.checklistItem}>
              <span className={styles.checkIconSuccess}>&#10003;</span>
              <span>LinkedIn connected</span>
            </div>
            <div className={styles.checklistItem}>
              <span className={styles.checkIconDash}>&minus;</span>
              <span>Profile completeness 70%</span>
            </div>
            <div className={styles.checklistItem}>
              <span className={styles.checkIconPending} />
              <span>Link check pending</span>
            </div>
          </div>

          <div className={styles.reviewNote}>
            Your readiness score is available now, before review finishes.
          </div>
        </div>
      </div>
    </div>
  );
}
