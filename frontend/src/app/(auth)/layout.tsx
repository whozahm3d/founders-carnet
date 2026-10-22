import styles from './layout.module.css';

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className={styles.wrapper}>
      {/* Left panel: Dark branded panel on tablet/laptop/desktop, brand banner on mobile */}
      <aside className={styles.leftPanel}>
        <div className={styles.brandContent}>
          <div className={styles.logoBadge}>FC</div>
          <h1 className={styles.brandTitle}>
            The Founder&apos;s<br />Carnet
          </h1>
          <p className={styles.brandTagline}>
            AI-assisted co-pilot platform for Pakistani startups &amp; ecosystem partners.
          </p>

          <div className={styles.featureList}>
            <div className={styles.featureItem}>
              <span className={styles.featureBullet}>&bull;</span>
              <span>Regulatory compliance with SECP &amp; PSEB regulations</span>
            </div>
            <div className={styles.featureItem}>
              <span className={styles.featureBullet}>&bull;</span>
              <span>7-dimension readiness index calibrated for Pakistani founders</span>
            </div>
            <div className={styles.featureItem}>
              <span className={styles.featureBullet}>&bull;</span>
              <span>Mutual contact reveal protocol (NFR-6 &amp; PECA 2016 compliant)</span>
            </div>
          </div>
        </div>

        <div className={styles.panelFooter}>
          <span>&copy; 2026 The Founder&apos;s Carnet</span>
          <span className={styles.footerDot}>&bull;</span>
          <span>NFR-4 Secure</span>
        </div>
      </aside>

      {/* Right panel: Form card container */}
      <main className={styles.mainArea}>
        <div className={styles.cardWrapper}>
          <div className={styles.card}>{children}</div>
          <p className={styles.mobileDisclaimer}>
            SEC &amp; PSEB compliant ecosystem platform &bull; NFR-4 secure
          </p>
        </div>
      </main>
    </div>
  );
}
