import type { UserRole } from '@/types/auth';
import type { NavItem } from '@/components/layout/Sidebar';

export interface RoleNavigation {
  /** Shown under the brand in the sidebar and in the top bar */
  label: string;
  items: NavItem[];
}

export const ROLE_NAVIGATION: Record<UserRole, RoleNavigation> = {
  founder: {
    label: 'Founder workspace',
    items: [
      { label: 'Dashboard', href: '/founder/dashboard' },
      { label: 'Profile', href: '/founder/profile' },
      { label: 'Readiness', href: '/founder/readiness' },
      { label: 'Pitch practice', href: '/founder/pitch' },
      { label: 'Feedback', href: '/founder/feedback' },
      { label: 'Matches', href: '/founder/matches' },
    ],
  },
  talent: {
    label: 'Talent workspace',
    items: [
      { label: 'Dashboard', href: '/talent/dashboard' },
      { label: 'Profile', href: '/talent/profile' },
      { label: 'Resume', href: '/talent/resume' },
      { label: 'Jobs', href: '/talent/jobs' },
      { label: 'Matches', href: '/talent/matches' },
    ],
  },
  mentor: {
    label: 'Mentor workspace',
    items: [
      { label: 'Dashboard', href: '/mentor/dashboard' },
      { label: 'Profile', href: '/mentor/profile' },
      { label: 'Requests', href: '/mentor/requests' },
    ],
  },
  investor: {
    label: 'Investor workspace',
    items: [
      { label: 'Dashboard', href: '/investor/dashboard' },
      { label: 'Profile', href: '/investor/profile' },
      { label: 'Founders', href: '/investor/founders' },
      { label: 'Requests', href: '/investor/requests' },
    ],
  },
  admin: {
    label: 'Admin workspace',
    items: [{ label: 'Console', href: '/admin/dashboard' }],
  },
};
