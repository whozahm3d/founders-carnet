'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { UserRole } from '@/types/auth';
import { Input, Select, Button, ConsentBox } from '@/components/ui';

const ROLE_OPTIONS = [
  { value: 'founder', label: 'Founder — Building a Pakistani startup' },
  { value: 'talent', label: 'Talent — Looking for tech roles / internships' },
  { value: 'mentor', label: 'Mentor — Advising early-stage founders' },
  { value: 'investor', label: 'Investor — Looking for vetted deal flow' },
];

export default function RegisterPage() {
  const router = useRouter();
  const { user, register, isLoading } = useAuth();

  // If already logged in, redirect to user's role dashboard
  useEffect(() => {
    if (!isLoading && user) {
      router.replace(`/${user.role}/dashboard`);
    }
  }, [user, isLoading, router]);

  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<UserRole>('founder');
  const [agreedToTerms, setAgreedToTerms] = useState(false);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!fullName || !email || !password) {
      setError('Please fill in all required fields.');
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters.');
      return;
    }

    if (!agreedToTerms) {
      setError('You must agree to the platform terms and consent conditions.');
      return;
    }

    try {
      setSubmitting(true);
      const user = await register({
        fullName,
        email,
        password,
        role,
        agreedToTerms,
      });
      router.push(`/${user.role}/dashboard`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Registration failed.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      <h2 style={{ fontSize: 'var(--font-size-xl)', fontWeight: 'var(--font-weight-bold)', marginBottom: 'var(--space-2)' }}>
        Create an account
      </h2>
      <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)', marginBottom: 'var(--space-6)' }}>
        Join the Pakistani startup ecosystem network.
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
          label="Full name"
          type="text"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          placeholder="e.g. Ahmed Khan"
          autoComplete="name"
          required
        />

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
          placeholder="At least 8 characters"
          autoComplete="new-password"
          hint="Minimum 8 characters (NFR-4 secure)"
          required
        />

        <Select
          label="I am joining as"
          value={role}
          onChange={(e) => setRole(e.target.value as UserRole)}
          options={ROLE_OPTIONS}
          hint="Your role determines your workspace permissions"
        />

        <ConsentBox
          id="terms-consent"
          checked={agreedToTerms}
          onChange={setAgreedToTerms}
          label="Terms & Privacy Consent"
          details="I consent to the processing of startup data and mutual contact reveal protocol (NFR-6, PECA 2016 compliant)."
        />

        <Button type="submit" variant="primary" block disabled={submitting}>
          {submitting ? 'Creating account...' : 'Create account'}
        </Button>
      </form>

      <div style={{ marginTop: 'var(--space-6)', textAlign: 'center', fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)' }}>
        Already have an account?{' '}
        <Link href="/login" style={{ color: 'var(--color-accent)', fontWeight: 'var(--font-weight-semibold)' }}>
          Sign in
        </Link>
      </div>
    </div>
  );
}
