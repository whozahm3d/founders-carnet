'use client';

import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui';
import { useState } from 'react';
import styles from './JobBoard.module.css';

interface JobItem {
  id: string;
  initial: string;
  title: string;
  company: string;
  location: string;
  postedTime: string;
  tags: string[];
}

const JOBS_DATA: JobItem[] = [
  {
    id: '1',
    initial: 'S',
    title: 'Software Engineering Intern',
    company: 'Chenab Pay',
    location: 'Lahore',
    postedTime: 'Posted today',
    tags: ['Internship', 'Hybrid', 'Fintech', 'MVP'],
  },
  {
    id: '2',
    initial: 'D',
    title: 'Data Analyst Intern',
    company: 'Mehran Works',
    location: 'Karachi',
    postedTime: 'Posted 1d ago',
    tags: ['Internship', 'Remote (Pakistan)', 'AI/ML', 'Growth'],
  },
  {
    id: '3',
    initial: 'M',
    title: 'Machine Learning Intern',
    company: 'Rozgar Labs',
    location: 'Karachi',
    postedTime: 'Posted 2d ago',
    tags: ['Internship', 'Remote (Pakistan)', 'SaaS', 'MVP'],
  },
  {
    id: '4',
    initial: 'R',
    title: 'DevOps Engineer',
    company: 'Ravi Health',
    location: 'Lahore',
    postedTime: 'Posted 3d ago',
    tags: ['Job', 'On-site', 'Healthtech', 'Growth'],
  },
  {
    id: '5',
    initial: 'A',
    title: 'QA Engineer Intern',
    company: 'Abhi',
    location: 'Lahore',
    postedTime: 'Posted 5d ago',
    tags: ['Internship', 'Hybrid', 'Fintech', 'MVP'],
  },
];

export default function TalentJobBoardPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [appliedIds, setAppliedIds] = useState<string[]>([]);
  const [savedIds, setSavedIds] = useState<string[]>([]);

  const handleApply = (id: string) => {
    setAppliedIds((prev) => [...prev, id]);
  };

  const handleSave = (id: string) => {
    setSavedIds((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
    );
  };

  return (
    <div className={styles.container}>
      <PageHeader
        title="Startup tech jobs and internships"
        subtitle="Curated tech roles at Pakistani startups."
      />

      <div className={styles.mainLayout}>
        {/* Left Filter Panel */}
        <aside className={styles.filterPanel}>
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search roles..."
            className={styles.searchInput}
          />

          <div className={styles.filterGroup}>
            <div className={styles.filterHeading}>Type</div>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" defaultChecked className={styles.checkboxInput} />
              <span>Job</span>
            </label>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" defaultChecked className={styles.checkboxInput} />
              <span>Internship</span>
            </label>
          </div>

          <div className={styles.filterGroup}>
            <div className={styles.filterHeading}>Sector</div>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" defaultChecked className={styles.checkboxInput} />
              <span>Fintech</span>
            </label>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" defaultChecked className={styles.checkboxInput} />
              <span>Healthtech</span>
            </label>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" className={styles.checkboxInput} />
              <span>Edtech</span>
            </label>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" defaultChecked className={styles.checkboxInput} />
              <span>SaaS</span>
            </label>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" defaultChecked className={styles.checkboxInput} />
              <span>AI/ML</span>
            </label>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" className={styles.checkboxInput} />
              <span>E-commerce tech</span>
            </label>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" className={styles.checkboxInput} />
              <span>Agritech</span>
            </label>
          </div>

          <div className={styles.filterGroup}>
            <div className={styles.filterHeading}>Stage</div>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" className={styles.checkboxInput} />
              <span>Idea</span>
            </label>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" defaultChecked className={styles.checkboxInput} />
              <span>MVP</span>
            </label>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" defaultChecked className={styles.checkboxInput} />
              <span>Growth</span>
            </label>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" className={styles.checkboxInput} />
              <span>Scaling</span>
            </label>
          </div>

          <div className={styles.filterGroup}>
            <div className={styles.filterHeading}>Work mode</div>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" defaultChecked className={styles.checkboxInput} />
              <span>Remote (Pakistan)</span>
            </label>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" defaultChecked className={styles.checkboxInput} />
              <span>Hybrid</span>
            </label>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" defaultChecked className={styles.checkboxInput} />
              <span>On-site</span>
            </label>
          </div>

          <div className={styles.filterGroup}>
            <div className={styles.filterHeading}>City</div>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" defaultChecked className={styles.checkboxInput} />
              <span>Lahore</span>
            </label>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" defaultChecked className={styles.checkboxInput} />
              <span>Karachi</span>
            </label>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" className={styles.checkboxInput} />
              <span>Islamabad</span>
            </label>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" className={styles.checkboxInput} />
              <span>Rawalpindi</span>
            </label>
            <label className={styles.checkboxLabel}>
              <input type="checkbox" className={styles.checkboxInput} />
              <span>Faisalabad</span>
            </label>
          </div>

          <button type="button" className={styles.clearFiltersBtn}>
            Clear filters
          </button>
        </aside>

        {/* Right Jobs Area */}
        <div className={styles.jobsArea}>
          <div className={styles.topBar}>
            <span className={styles.rolesCount}>24 roles</span>
            <select className={styles.sortSelect}>
              <option value="newest">Newest</option>
              <option value="relevant">Most relevant</option>
            </select>
          </div>

          {JOBS_DATA.map((job) => (
            <div key={job.id} className={styles.jobCard}>
              <div className={styles.jobCardHeader}>
                <div className={styles.companyInfo}>
                  <div className={styles.avatar}>{job.initial}</div>
                  <div>
                    <div className={styles.jobTitleText}>{job.title}</div>
                    <div className={styles.companyLocation}>
                      {job.company}, {job.location}
                    </div>
                  </div>
                </div>
                <span className={styles.postedTime}>{job.postedTime}</span>
              </div>

              <div className={styles.tagsRow}>
                {job.tags.map((t) => (
                  <span key={t} className={styles.tagPill}>
                    {t}
                  </span>
                ))}
              </div>

              <div className={styles.actionsRow}>
                <Button
                  variant="primary"
                  size="sm"
                  disabled={appliedIds.includes(job.id)}
                  onClick={() => handleApply(job.id)}
                >
                  {appliedIds.includes(job.id) ? 'Applied' : 'Apply'}
                </Button>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => handleSave(job.id)}
                >
                  {savedIds.includes(job.id) ? 'Saved' : 'Save'}
                </Button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
