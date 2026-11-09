import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import {
  ArrowLeft,
  Clock,
  TrendingUp,
  Wallet,
  BookOpen,
  Library,
} from 'lucide-react';
import { getCareerById, getLearningRoadmap } from '../lib/api';
import { Card, Badge, Button, Skeleton, ErrorState } from './ui';
import CareerResources from './Resources';

function formatSalary(range) {
  if (!range?.min || !range?.max) return 'Not published';
  const fmt = (n) => n.toLocaleString('en-US', { maximumFractionDigits: 0 });
  return `${range.currency || 'USD'} ${fmt(range.min)} – ${fmt(range.max)}`;
}

/** Stat tile. Label above, value below, icon decorative. */
function Stat({ icon: Icon, label, value }) {
  return (
    <Card className="p-5">
      <div className="flex items-center gap-2 text-muted-foreground">
        <Icon className="h-4 w-4" aria-hidden="true" />
        <span className="text-sm font-medium">{label}</span>
      </div>
      <p className="mt-2 text-lg font-bold text-foreground">{value}</p>
    </Card>
  );
}

export default function CareerDetails() {
  const { id } = useParams();
  const [career, setCareer] = useState(null);
  const [roadmap, setRoadmap] = useState(null);
  const [error, setError] = useState(null);

  const load = React.useCallback(() => {
    setError(null);
    setCareer(null);
    setRoadmap(null);
    getCareerById(id)
      .then(setCareer)
      .catch((err) => setError(err.message));
    // The roadmap may call the model, so it loads independently — the page
    // body does not wait on it.
    getLearningRoadmap(id)
      .then(setRoadmap)
      .catch(() => setRoadmap({ roadmap: [] }));
  }, [id]);

  useEffect(load, [load]);

  if (error) {
    return (
      <div className="space-y-5">
        <ErrorState message={error} onRetry={load} />
        <Button as={Link} to="/careers" variant="outline">
          <ArrowLeft className="h-4 w-4" aria-hidden="true" />
          Back to all careers
        </Button>
      </div>
    );
  }

  if (!career) {
    return (
      <div className="space-y-5">
        <Skeleton className="h-10 w-2/3" />
        <Skeleton className="h-24" />
        <div className="grid gap-4 sm:grid-cols-3">
          <Skeleton className="h-24" />
          <Skeleton className="h-24" />
          <Skeleton className="h-24" />
        </div>
        <Skeleton className="h-72" />
      </div>
    );
  }

  const steps = roadmap?.roadmap ?? [];

  return (
    <div className="space-y-8">
      <Button as={Link} to="/careers" variant="ghost" size="sm" className="-ml-3">
        <ArrowLeft className="h-4 w-4" aria-hidden="true" />
        All careers
      </Button>

      <header>
        <Badge tone="primary">{career.category}</Badge>
        <h1 className="mt-4 text-3xl font-extrabold tracking-tight text-foreground sm:text-4xl">
          {career.title}
        </h1>
        <p className="mt-4 max-w-3xl text-lg leading-relaxed text-muted-foreground">
          {career.description}
        </p>
      </header>

      <div className="grid gap-4 sm:grid-cols-3">
        <Stat
          icon={Wallet}
          label="Salary range"
          value={formatSalary(career.salary_range)}
        />
        <Stat
          icon={TrendingUp}
          label="Growth score"
          value={`${career.growth_potential ?? '—'}/100`}
        />
        <Stat
          icon={Clock}
          label="Time to job-ready"
          value={roadmap?.estimated_time ?? '6–12 months'}
        />
      </div>

      <section aria-labelledby="skills-heading">
        <h2
          id="skills-heading"
          className="text-2xl font-bold tracking-tight text-foreground"
        >
          Skills
        </h2>
        <div className="mt-5 grid gap-5 sm:grid-cols-2">
          <Card className="p-5">
            <h3 className="text-sm font-bold text-foreground">Required</h3>
            <ul className="mt-3 flex flex-wrap gap-1.5">
              {(career.required_skills || []).map((s) => (
                <li key={s}>
                  <Badge tone="primary">{s}</Badge>
                </li>
              ))}
            </ul>
          </Card>
          <Card className="p-5">
            <h3 className="text-sm font-bold text-foreground">
              Nice to have
            </h3>
            {career.preferred_skills?.length ? (
              <ul className="mt-3 flex flex-wrap gap-1.5">
                {career.preferred_skills.map((s) => (
                  <li key={s}>
                    <Badge>{s}</Badge>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-3 text-sm text-muted-foreground">
                Nothing listed.
              </p>
            )}
          </Card>
        </div>
      </section>

      <section aria-labelledby="roadmap-heading">
        <h2
          id="roadmap-heading"
          className="flex items-center gap-2 text-2xl font-bold tracking-tight text-foreground"
        >
          <BookOpen className="h-6 w-6 text-primary" aria-hidden="true" />
          Learning roadmap
        </h2>

        {roadmap === null ? (
          <div className="mt-5 space-y-3">
            {Array.from({ length: 5 }, (_, i) => (
              <Skeleton key={i} className="h-20" />
            ))}
          </div>
        ) : steps.length === 0 ? (
          <p className="mt-4 text-muted-foreground">
            No roadmap published for this career yet.
          </p>
        ) : (
          <ol className="mt-5 space-y-3">
            {steps.map((step, i) => {
              // The endpoint returns plain strings without a key, and
              // structured objects when the AI pass succeeded.
              const structured = typeof step === 'object' && step !== null;
              const title = structured ? step.title : step;
              return (
                <li key={i}>
                  <Card className="flex gap-4 p-5">
                    <span className="grid h-9 w-9 shrink-0 place-items-center rounded-xl bg-primary/10 text-sm font-extrabold text-primary">
                      {structured ? step.step : i + 1}
                    </span>
                    <div className="min-w-0 flex-1">
                      <h3 className="font-bold text-foreground">{title}</h3>
                      {structured && step.description && (
                        <p className="mt-1.5 text-sm leading-relaxed text-muted-foreground">
                          {step.description}
                        </p>
                      )}
                      {structured && (step.duration || step.resources?.length) && (
                        <div className="mt-3 flex flex-wrap items-center gap-1.5">
                          {step.duration && (
                            <Badge tone="accent">{step.duration}</Badge>
                          )}
                          {(step.resources || []).map((r) => (
                            <Badge key={r}>{r}</Badge>
                          ))}
                        </div>
                      )}
                    </div>
                  </Card>
                </li>
              );
            })}
          </ol>
        )}
      </section>

      <section aria-labelledby="resources-heading">
        <h2
          id="resources-heading"
          className="flex items-center gap-2 text-2xl font-bold tracking-tight text-foreground"
        >
          <Library className="h-6 w-6 text-primary" aria-hidden="true" />
          Where to learn this
        </h2>
        <CareerResources careerId={id} />
      </section>

      <Card glass className="p-6 text-center">
        <p className="text-muted-foreground">
          Want to know how close you already are?
        </p>
        <div className="mt-4 flex justify-center">
          <Button as={Link} to="/profile" variant="accent">
            Check my match for this role
          </Button>
        </div>
      </Card>
    </div>
  );
}
