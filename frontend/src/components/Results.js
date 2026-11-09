import React, { useState } from 'react';
import { Link, useLocation, Navigate } from 'react-router-dom';
import {
  ArrowRight,
  Check,
  AlertTriangle,
  Layers,
  ChevronDown,
  Trophy,
} from 'lucide-react';
import { getSkillGap, getSkillResources } from '../lib/api';
import { SkillResources } from './Resources';
import { Button, Card, Badge, Meter, Spinner, ErrorState, cx } from './ui';

function formatSalary(range) {
  if (!range?.min || !range?.max) return null;
  const fmt = (n) => `${Math.round(n / 1000)}k`;
  return `${range.currency || 'USD'} ${fmt(range.min)}–${fmt(range.max)}`;
}

/* -------------------------- skill gap panel --------------------------- */

/**
 * One missing skill, expandable to its learning resources. Resources are
 * fetched per skill on demand rather than all upfront, so opening the gap
 * panel stays a single request.
 */
function MissingSkill({ skill, index }) {
  const [open, setOpen] = useState(false);
  const [resources, setResources] = useState(null);

  function toggle() {
    const next = !open;
    setOpen(next);
    if (next && resources === null) {
      getSkillResources(skill)
        .then((d) => setResources(d.resources))
        .catch(() => setResources([]));
    }
  }

  return (
    <li>
      <button
        type="button"
        onClick={toggle}
        aria-expanded={open}
        className="flex min-h-[44px] w-full cursor-pointer items-center gap-2 rounded-lg px-1 text-left text-sm text-foreground transition-colors duration-200 hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      >
        <span className="grid h-5 w-5 shrink-0 place-items-center rounded-md bg-warning/15 text-xs font-bold text-warning">
          {index + 1}
        </span>
        <span className="flex-1">{skill}</span>
        <ChevronDown
          className={cx(
            'h-4 w-4 shrink-0 text-muted-foreground transition-transform duration-200',
            open && 'rotate-180'
          )}
          aria-hidden="true"
        />
      </button>
      {open &&
        (resources === null ? (
          <p className="px-1 py-2 text-xs text-muted-foreground">Loading…</p>
        ) : (
          <SkillResources resources={resources} />
        ))}
    </li>
  );
}

function SkillGapPanel({ careerId, profile }) {
  const [state, setState] = useState('idle'); // idle | loading | done | error
  const [gap, setGap] = useState(null);
  const [error, setError] = useState(null);

  async function run() {
    setState('loading');
    setError(null);
    try {
      const data = await getSkillGap({
        careerId,
        skills: profile?.skills ?? [],
        experienceYears: profile?.experience_years ?? 0,
      });
      setGap(data);
      setState('done');
    } catch (err) {
      setError(err.message);
      setState('error');
    }
  }

  if (state === 'idle') {
    return (
      <Button variant="outline" size="sm" onClick={run}>
        <Layers className="h-4 w-4" aria-hidden="true" />
        Analyse my skill gap
      </Button>
    );
  }

  if (state === 'loading') return <Spinner label="Comparing your skills…" />;

  if (state === 'error') {
    return <ErrorState message={error} onRetry={run} />;
  }

  return (
    <div className="animate-fade-in space-y-5 rounded-xl bg-muted/50 p-5">
      <Meter value={gap.coverage} label="Required skills you already cover" />

      <p className="text-sm leading-relaxed text-foreground">{gap.summary}</p>

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <h4 className="flex items-center gap-1.5 text-sm font-bold text-success">
            <Check className="h-4 w-4" aria-hidden="true" />
            You have ({gap.skills_matched.length})
          </h4>
          {gap.skills_matched.length ? (
            <ul className="mt-2.5 flex flex-wrap gap-1.5">
              {gap.skills_matched.map((s) => (
                <li key={s}>
                  <Badge tone="success">{s}</Badge>
                </li>
              ))}
            </ul>
          ) : (
            <p className="mt-2 text-sm text-muted-foreground">
              None of the required skills yet.
            </p>
          )}
        </div>

        <div>
          <h4 className="flex items-center gap-1.5 text-sm font-bold text-warning">
            <AlertTriangle className="h-4 w-4" aria-hidden="true" />
            To learn ({gap.skills_missing.length})
          </h4>
          {gap.skills_missing.length ? (
            <ol className="mt-2.5 space-y-2">
              {gap.priority_order.map((s, i) => (
                <MissingSkill key={s} skill={s} index={i} />
              ))}
            </ol>
          ) : (
            <p className="mt-2 text-sm text-muted-foreground">
              Nothing missing — you meet every listed requirement.
            </p>
          )}
        </div>
      </div>

      {gap.estimated_months > 0 && (
        <p className="text-sm text-muted-foreground">
          Rough time to close the gap:{' '}
          <strong className="font-bold text-foreground">
            {gap.estimated_months} months
          </strong>
          {gap.ai_generated && ' (AI estimate)'}
        </p>
      )}
    </div>
  );
}

/* --------------------------- result card ------------------------------ */

function ResultCard({ rec, rank, profile }) {
  const [openPath, setOpenPath] = useState(false);
  const careerId = rec.career_id;
  const salary = formatSalary(rec.salary_range);

  return (
    <Card className="overflow-hidden">
      <div className="p-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="min-w-0">
            <div className="flex items-center gap-2.5">
              <span
                className={cx(
                  'grid h-8 w-8 shrink-0 place-items-center rounded-xl text-sm font-extrabold',
                  rank === 1
                    ? 'bg-accent text-on-accent'
                    : 'bg-primary/10 text-primary'
                )}
              >
                {rank === 1 ? (
                  <Trophy className="h-4 w-4" aria-hidden="true" />
                ) : (
                  rank
                )}
              </span>
              <h2 className="truncate text-xl font-bold text-foreground">
                {rec.career}
              </h2>
            </div>
            {salary && (
              <p className="mt-2 text-sm text-muted-foreground">
                Typical range {salary} · growth score {rec.growth_potential}/100
              </p>
            )}
          </div>

          <div className="w-full sm:w-44">
            <Meter
              value={rec.match_score}
              label="Match"
              tone={rank === 1 ? 'accent' : 'primary'}
            />
          </div>
        </div>

        <p className="mt-5 leading-relaxed text-foreground">{rec.reasoning}</p>

        {rec.required_skills?.length > 0 && (
          <div className="mt-5">
            <h3 className="text-sm font-semibold text-muted-foreground">
              Required skills
            </h3>
            <ul className="mt-2.5 flex flex-wrap gap-1.5">
              {rec.required_skills.map((s) => (
                <li key={s}>
                  <Badge tone="primary">{s}</Badge>
                </li>
              ))}
            </ul>
          </div>
        )}

        {rec.learning_path?.length > 0 && (
          <div className="mt-5">
            <button
              type="button"
              onClick={() => setOpenPath((o) => !o)}
              aria-expanded={openPath}
              className="flex min-h-[44px] cursor-pointer items-center gap-1.5 text-sm font-semibold text-primary transition-colors duration-200 hover:text-primary-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              {openPath ? 'Hide' : 'Show'} the {rec.learning_path.length}-step
              learning path
              <ChevronDown
                className={cx(
                  'h-4 w-4 transition-transform duration-200',
                  openPath && 'rotate-180'
                )}
                aria-hidden="true"
              />
            </button>
            {openPath && (
              <ol className="animate-fade-in mt-3 space-y-2">
                {rec.learning_path.map((step, i) => (
                  <li
                    key={i}
                    className="flex items-start gap-2.5 text-sm text-foreground"
                  >
                    <span className="mt-0.5 grid h-5 w-5 shrink-0 place-items-center rounded-md bg-primary/10 text-xs font-bold text-primary">
                      {i + 1}
                    </span>
                    {typeof step === 'string' ? step : step.title}
                  </li>
                ))}
              </ol>
            )}
          </div>
        )}

        <div className="mt-6 flex flex-wrap items-center gap-3 border-t border-border pt-5">
          <SkillGapPanel careerId={careerId} profile={profile} />
          <Button as={Link} to={`/careers/${careerId}`} variant="ghost" size="sm">
            Full details
            <ArrowRight className="h-4 w-4" aria-hidden="true" />
          </Button>
        </div>
      </div>
    </Card>
  );
}

/* ------------------------------- page --------------------------------- */

export default function Results() {
  const location = useLocation();
  const { data, profile } = location.state || {};

  // Reached directly or after a refresh: there is no profile to show results
  // for, so send the visitor back to the form instead of rendering an error.
  if (!data) return <Navigate to="/profile" replace />;

  const recommendations = data.recommendations || [];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold tracking-tight text-foreground sm:text-4xl">
          Your top {recommendations.length}{' '}
          {recommendations.length === 1 ? 'match' : 'matches'}
        </h1>
        {data.user_profile_summary && (
          <p className="mt-3 text-muted-foreground">{data.user_profile_summary}</p>
        )}
      </div>

      <div className="space-y-5">
        {recommendations.map((rec, i) => (
          <ResultCard
            key={rec.career}
            rec={rec}
            rank={i + 1}
            profile={profile}
          />
        ))}
      </div>

      <Card glass className="p-6 text-center">
        <p className="text-muted-foreground">
          Want to explore outside your matches?
        </p>
        <div className="mt-4 flex flex-wrap justify-center gap-3">
          <Button as={Link} to="/careers" variant="outline">
            Browse all careers
          </Button>
          <Button as={Link} to="/profile" variant="ghost">
            Edit my profile
          </Button>
        </div>
      </Card>
    </div>
  );
}
