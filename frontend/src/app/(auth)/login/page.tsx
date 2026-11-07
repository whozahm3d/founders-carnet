'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { UserRole } from '@/types/auth';
import { Input, Select, Button } from '@/components/ui';

const MOCK_ROLE_OPTIONS = [
  { value: 'founder', label: 'Founder' },
  { value: 'talent', label: 'Talent' },
  { value: 'mentor', label: 'Mentor' },
  { value: 'investor', label: 'Investor' },
  { value: 'admin', label: 'Admin' },
];

export default function LoginPage() {
  const router = useRouter();
  const { user, login, isMockEnabled, isLoading } = useAuth();

  // If already logged in, redirect to user's role dashboard
  useEffect(() => {
    if (!isLoading && user) {
      router.replace(`/${user.role}/dashboard`);
    }
  }, [user, isLoading, router]);

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<UserRole>('founder');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!email || !password) {
      setError('Please fill in both email and password.');
      return;
    }

    try {
      setSubmitting(true);
      const loggedInUser = await login({
        email,
        password,
        role: isMockEnabled ? role : undefined,
      });
      router.push(`/${loggedInUser.role}/dashboard`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Invalid credentials. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (isLoading || user) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', padding: 'var(--space-8)' }}>
        <div className="spinner" />
      </div>
    );
  }

  return (
    <div>
      <h2 style={{ fontSize: 'var(--font-size-xl)', fontWeight: 'var(--font-weight-bold)', marginBottom: 'var(--space-2)' }}>
        Welcome back
      </h2>
      <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)', marginBottom: 'var(--space-6)' }}>
        Sign in with your email and password to access your workspace.
      </p>

      {error && (
        <div
          role="alert"
          style={{
            backgroundColor: 'var(--color-error-bg)',
            color: 'var(--color-error)',
            padding: 'var(--space-3)',
            borderRadius: 'var(--radius-md)',
            fontSize: 'var(--font-size-xs)',
            marginBottom: 'var(--space-4)',
          }}
        >
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
        <Input
          label="Email address"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@carnet.dev"
          autoComplete="email"
          required
        />

        <Input
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••"
          autoComplete="current-password"
          required
        />

        {/* Mock mode role selector so any email/password can test each role */}
        {isMockEnabled && (
          <Select
            label="Mock Mode Role"
            value={role}
            onChange={(e) => setRole(e.target.value as UserRole)}
            options={MOCK_ROLE_OPTIONS}
            hint="Mock mode: test any role with any email & password"
          />
        )}

        <Button type="submit" variant="primary" block disabled={submitting}>
          {submitting ? 'Signing in...' : 'Sign in'}
        </Button>
      </form>

      <div style={{ marginTop: 'var(--space-6)', textAlign: 'center', fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)' }}>
        Don&apos;t have an account?{' '}
        <Link href="/register" style={{ color: 'var(--color-accent)', fontWeight: 'var(--font-weight-semibold)' }}>
          Create an account
        </Link>
      </div>
    </div>
  );
}
