'use client';

import { useAuth } from '@/context/AuthContext';
import { Sidebar } from '@/components/layout/Sidebar';
import { ROLE_NAVIGATION } from '@/lib/navigation';
import { useRouter, usePathname } from 'next/navigation';
import { useEffect, useState, useCallback } from 'react';
import styles from './DashboardLayout.module.css';

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, isLoading, logout } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  // Mobile menu drawer state
  const [drawerOpen, setDrawerOpen] = useState(false);

  // Close drawer on Escape key press (a11y)
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      setDrawerOpen(false);
    }
  }, []);

  useEffect(() => {
    if (drawerOpen) {
      window.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = '';
    };
  }, [drawerOpen, handleKeyDown]);

  // 1. If unauthenticated, redirect to /login
  // 2. Role-based route guard: prevent user from visiting another role's routes
  useEffect(() => {
    if (!isLoading) {
      if (!user) {
        router.replace('/login');
        return;
      }

      // Check if current route belongs to another role
      const roles = ['founder', 'talent', 'mentor', 'investor', 'admin'] as const;
      const targetRole = roles.find((r) => pathname.startsWith(`/${r}`));
      if (targetRole && targetRole !== user.role) {
        // User attempted to access another role's path -> send them back to their own dashboard
        router.replace(`/${user.role}/dashboard`);
      }
    }
  }, [user, isLoading, pathname, router]);

  if (isLoading || !user) {
    return (
      <div className={styles.loadingWrapper}>
        <div className="spinner" />
        <p>Loading session...</p>
      </div>
    );
  }

  // Prevent flash of another role's content while redirect is executing
  const roles = ['founder', 'talent', 'mentor', 'investor', 'admin'] as const;
  const targetRole = roles.find((r) => pathname.startsWith(`/${r}`));
  if (targetRole && targetRole !== user.role) {
    return (
      <div className={styles.loadingWrapper}>
        <div className="spinner" />
        <p>Redirecting to your workspace...</p>
      </div>
    );
  }

  const roleNav = ROLE_NAVIGATION[user.role] || ROLE_NAVIGATION.founder;

  return (
    <div className={styles.container}>
      {/* Mobile Top Header (Visible only on < 640px) */}
      <header className={styles.mobileHeader}>
        <button
          type="button"
          className={styles.menuButton}
          onClick={() => setDrawerOpen(true)}
          aria-label="Open navigation menu"
          aria-expanded={drawerOpen}
          aria-controls="app-sidebar"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <line x1="3" y1="12" x2="21" y2="12" />
            <line x1="3" y1="6" x2="21" y2="6" />
            <line x1="3" y1="18" x2="21" y2="18" />
          </svg>
        </button>

        <div className={styles.mobileBrand}>
          <span className={styles.mobileLogoBadge}>FC</span>
          <span className={styles.mobileTitle}>The Founder&apos;s Carnet</span>
        </div>

        <div className={styles.mobileUserBadge} title={`${user.fullName || user.email} (${user.role})`}>
          <span className={styles.statusDot} />
        </div>
      </header>

      {/* Sidebar */}
      <Sidebar
        roleLabel={roleNav.label}
        items={roleNav.items}
        userEmail={user.email}
        userName={user.fullName}
        isOpen={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        onLogout={() => {
          logout();
          router.replace('/login');
        }}
      />

      <div className={styles.contentArea}>
        {/* Top User Session Bar */}
        <header className={styles.topBar}>
          <div className={styles.workspaceIndicator}>
            <span className={styles.roleTag}>{user.role}</span>
            <span className={styles.dividerDot}>&bull;</span>
            <span className={styles.workspaceLabel}>{roleNav.label}</span>
          </div>

          <div className={styles.userBadge}>
            <span className={styles.statusDot} />
            <span className={styles.userNameText}>{user.fullName || user.email}</span>
            <button
              type="button"
              onClick={() => {
                logout();
                router.replace('/login');
              }}
              className={styles.topLogoutBtn}
              title="Log out"
            >
              Log out
            </button>
          </div>
        </header>

        {/* Scrollable container with capped max-width on large screens */}
        <main className={styles.mainContent}>
          <div className={styles.mainContentInner}>{children}</div>
        </main>
      </div>
    </div>
  );
}
