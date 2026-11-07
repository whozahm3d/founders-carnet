'use client';

import { PageHeader } from '@/components/layout/PageHeader';
import { Card, EmptyState } from '@/components/ui';

interface PlaceholderPageProps {
  title: string;
  subtitle: string;
  roleName: string;
}

export function PlaceholderPage({ title, subtitle, roleName }: PlaceholderPageProps) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)', width: '100%' }}>
      <PageHeader title={title} subtitle={subtitle} />
      <Card>
        <EmptyState
          title="Coming soon"
          description={`The ${title} screen for ${roleName} is currently under active implementation.`}
        />
      </Card>
    </div>
  );
}
