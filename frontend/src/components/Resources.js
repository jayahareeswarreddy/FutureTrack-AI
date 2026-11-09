import React, { useEffect, useState } from 'react';
import {
  BookOpen,
  FileText,
  Youtube,
  GraduationCap,
  ExternalLink,
} from 'lucide-react';
import { getCareerResources } from '../lib/api';
import { Card, Badge, Skeleton, ErrorState, cx } from './ui';

/** Icon + styling per resource kind. Never colour alone — the label repeats it. */
const KIND = {
  docs: { icon: FileText, label: 'Docs', tone: 'primary' },
  course: { icon: GraduationCap, label: 'Course', tone: 'success' },
  video: { icon: Youtube, label: 'Video', tone: 'accent' },
  book: { icon: BookOpen, label: 'Book', tone: 'warning' },
};

export function ResourceLink({ resource }) {
  const meta = KIND[resource.kind] ?? KIND.docs;
  const Icon = meta.icon;

  return (
    <a
      href={resource.url}
      target="_blank"
      rel="noopener noreferrer"
      className={cx(
        'group flex min-h-[44px] items-center gap-3 rounded-xl border border-border',
        'bg-card px-3.5 py-2.5 transition-colors duration-200',
        'hover:border-primary hover:bg-muted',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring'
      )}
    >
      <span
        className={cx(
          'grid h-8 w-8 shrink-0 place-items-center rounded-lg',
          meta.tone === 'primary' && 'bg-primary/10 text-primary',
          meta.tone === 'success' && 'bg-success/10 text-success',
          meta.tone === 'accent' && 'bg-accent/10 text-accent',
          meta.tone === 'warning' && 'bg-warning/10 text-warning'
        )}
      >
        <Icon className="h-4 w-4" aria-hidden="true" />
      </span>

      <span className="min-w-0 flex-1">
        <span className="block truncate text-sm font-semibold text-foreground">
          {resource.title}
        </span>
        <span className="block truncate text-xs text-muted-foreground">
          {meta.label} · {resource.provider}
        </span>
      </span>

      <ExternalLink
        className="h-4 w-4 shrink-0 text-muted-foreground transition-colors duration-200 group-hover:text-primary"
        aria-hidden="true"
      />
      {/* States the new-tab behaviour for screen readers without cluttering the label. */}
      <span className="sr-only">(opens in a new tab)</span>
    </a>
  );
}

/** Compact list used inside the skill-gap panel. */
export function SkillResources({ resources }) {
  if (!resources?.length) return null;
  return (
    <ul className="mt-2 space-y-1.5">
      {resources.map((r) => (
        <li key={r.url}>
          <ResourceLink resource={r} />
        </li>
      ))}
    </ul>
  );
}

/** Full per-career panel, grouped by the skill each resource teaches. */
export default function CareerResources({ careerId }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const load = React.useCallback(() => {
    setError(null);
    setData(null);
    getCareerResources(careerId)
      .then(setData)
      .catch((err) => setError(err.message));
  }, [careerId]);

  useEffect(load, [load]);

  if (error) return <ErrorState message={error} onRetry={load} />;

  if (!data) {
    return (
      <div className="mt-5 grid gap-4 sm:grid-cols-2">
        {Array.from({ length: 4 }, (_, i) => (
          <Skeleton key={i} className="h-40" />
        ))}
      </div>
    );
  }

  return (
    <>
      <p className="mt-3 text-muted-foreground">
        {data.total_resources} free resources — official documentation, books
        and video courses, grouped by the skill they teach.
      </p>
      <div className="mt-5 grid gap-4 sm:grid-cols-2">
        {data.by_skill.map((group) => (
          <Card key={group.skill} className="p-5">
            <div className="flex items-center justify-between gap-2">
              <h3 className="font-bold text-foreground">{group.skill}</h3>
              <Badge>{group.resources.length}</Badge>
            </div>
            <ul className="mt-3 space-y-2">
              {group.resources.map((r) => (
                <li key={r.url}>
                  <ResourceLink resource={r} />
                </li>
              ))}
            </ul>
          </Card>
        ))}
      </div>
    </>
  );
}
