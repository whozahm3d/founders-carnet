'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import styles from './Sidebar.module.css';

/** A single nav item for the sidebar. */
export interface NavItem {
  label: string;
  href: string;
  /** Optional SVG icon as a React node */
  icon?: React.ReactNode;
}

interface SidebarProps {
  /** Role label shown below the brand, e.g. "Founder workspace" */
  roleLabel: string;
  /** Navigation items for this role */
  items?: NavItem[];
  navItems?: NavItem[];
  userEmail?: string;
  userName?: string;
  /** Mobile drawer open state */
  isOpen?: boolean;
  /** Mobile drawer close callback */
  onClose?: () => void;
  /** Called when the user clicks "Log out" */
  onLogout?: () => void;
}

/** Default SVG icons matching wireframe sidebars exactly */
function getDefaultIcon(label: string) {
  const l = label.toLowerCase();
  if (l === 'dashboard' || l === 'console') {
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="7" height="7" rx="1" />
        <rect x="14" y="3" width="7" height="7" rx="1" />
        <rect x="14" y="14" width="7" height="7" rx="1" />
        <rect x="3" y="14" width="7" height="7" rx="1" />
      </svg>
    );
  }
  if (l === 'profile') {
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
        <circle cx="12" cy="7" r="4" />
      </svg>
    );
  }
  if (l.includes('readiness')) {
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="22 7 13.5 15.5 8.5 10.5 2 17" />
        <polyline points="16 7 22 7 22 13" />
      </svg>
    );
  }
  if (l.includes('pitch')) {
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
        <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
        <line x1="12" y1="19" x2="12" y2="22" />
      </svg>
    );
  }
  if (l.includes('feedback')) {
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <path d="m9 15 2 2 4-4" />
      </svg>
    );
  }
  if (l.includes('match') || l.includes('founder')) {
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
      </svg>
    );
  }
  if (l.includes('resume')) {
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" />
        <line x1="16" y1="17" x2="8" y2="17" />
      </svg>
    );
  }
  if (l.includes('job')) {
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="7" width="20" height="14" rx="2" ry="2" />
        <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
      </svg>
    );
  }
  if (l.includes('request')) {
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="4" width="20" height="16" rx="2" />
        <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" />
      </svg>
    );
  }
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <polygon points="12 8 8 12 12 16 16 12 12 8" />
    </svg>
  );
}

export function Sidebar({
  roleLabel,
  items,
  navItems,
  isOpen = false,
  onClose,
  onLogout,
}: SidebarProps) {
  const links = items || navItems || [];
  const pathname = usePathname();

  return (
    <>
      {/* Mobile Backdrop overlay */}
      {isOpen && (
        <div
          className={styles.backdrop}
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      <aside
        className={`${styles.sidebar} ${isOpen ? styles.sidebarOpen : ''}`}
        aria-label="Main navigation"
        id="app-sidebar"
      >
        {/* Header / Brand */}
        <div className={styles.brand}>
          <div className={styles.brandTitleRow}>
            <div className={styles.brandTitle}>
              The<br />Founder&apos;s<br />Carnet
            </div>
            {/* Close button inside mobile drawer */}
            <button
              type="button"
              className={styles.closeDrawerBtn}
              onClick={onClose}
              aria-label="Close navigation menu"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>
          <div className={styles.roleLabel}>{roleLabel}</div>
        </div>

        {/* Tablet rail brand icon */}
        <div className={styles.railBrand} title="The Founder's Carnet">
          <span className={styles.railBadge}>FC</span>
        </div>

        {/* Navigation links */}
        <nav className={styles.nav}>
          {links.map((item) => {
            // Strict exact match for root/dashboard to prevent false active highlight
            const isActive = pathname === item.href;
            const icon = item.icon || getDefaultIcon(item.label);
            return (
              <Link
                key={item.href}
                href={item.href}
                className={isActive ? styles.navLinkActive : styles.navLink}
                aria-current={isActive ? 'page' : undefined}
                title={item.label}
                onClick={onClose}
              >
                <span className={styles.navIcon} aria-hidden="true">
                  {icon}
                </span>
                <span className={styles.navLabel}>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Footer / Logout */}
        <div className={styles.footer}>
          <button
            className={styles.logoutBtn}
            onClick={onLogout}
            type="button"
            aria-label="Log out of session"
            title="Log out"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
            <span className={styles.logoutText}>Log out</span>
          </button>
        </div>
      </aside>
    </>
  );
}
