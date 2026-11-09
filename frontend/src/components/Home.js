import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowRight,
  Target,
  Map,
  ShieldCheck,
  Search,
  Layers,
} from 'lucide-react';
import { getCategories } from '../lib/api';
import { Button, Card, Badge, Skeleton } from './ui';

const FEATURES = [
  {
    icon: Target,
    title: 'Matched on your actual skills',
    body: 'Your skills, interests and experience are scored against every career in the database. The score is computed in Python, not guessed by a model.',
  },
  {
    icon: ShieldCheck,
    title: 'Validated AI explanations',
    body: 'GPT-4o-mini writes the reasoning, but every response is checked against a JSON Schema first. Malformed output is retried, then falls back to a rule-based explanation.',
  },
  {
    icon: Map,
    title: 'Step-by-step roadmaps',
    body: 'Each career comes with an ordered learning path — what to learn, in what order, and roughly how long it takes.',
  },
  {
    icon: Layers,
    title: 'Skill-gap analysis',
    body: 'Pick a target role and see exactly which required skills you already cover, which are missing, and the order to close them in.',
  },
];

export default function Home() {
  const [categories, setCategories] = useState(null);

  useEffect(() => {
    let cancelled = false;
    getCategories()
      .then((d) => !cancelled && setCategories(d))
      .catch(() => !cancelled && setCategories({ categories: [] }));
    return () => {
      cancelled = true;
    };
  }, []);

  const careerCount =
    categories?.categories?.reduce((sum, c) => sum + c.career_count, 0) ?? null;

  return (
    <div className="space-y-section">
      {/* ------------------------------ hero ------------------------------ */}
      <section className="animate-fade-in-up">
        <Badge tone="accent">AI career guidance</Badge>
        <h1 className="mt-5 max-w-3xl text-4xl font-extrabold leading-[1.1] tracking-tight text-foreground sm:text-5xl lg:text-6xl">
          Find the tech career your skills already point to.
        </h1>
        <p className="mt-5 max-w-2xl text-lg text-muted-foreground">
          Describe what you know and what you enjoy. FutureTrack scores you
          against{' '}
          {careerCount ? (
            <strong className="font-bold text-foreground">
              {careerCount} career paths
            </strong>
          ) : (
            'every career path'
          )}
          , explains each match, and hands you the roadmap to get there.
        </p>

        <div className="mt-8 flex flex-wrap gap-3">
          <Button as={Link} to="/profile" variant="accent" size="lg">
            Get my recommendations
            <ArrowRight className="h-5 w-5" aria-hidden="true" />
          </Button>
          <Button as={Link} to="/careers" variant="outline" size="lg">
            <Search className="h-5 w-5" aria-hidden="true" />
            Browse all careers
          </Button>
        </div>
      </section>

      {/* ---------------------------- features --------------------------- */}
      <section aria-labelledby="how-heading">
        <h2
          id="how-heading"
          className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl"
        >
          How the matching works
        </h2>
        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          {FEATURES.map(({ icon: Icon, title, body }) => (
            <Card key={title} className="p-6">
              <span className="grid h-11 w-11 place-items-center rounded-xl bg-primary/10 text-primary">
                <Icon className="h-5 w-5" aria-hidden="true" />
              </span>
              <h3 className="mt-4 text-lg font-bold text-foreground">{title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                {body}
              </p>
            </Card>
          ))}
        </div>
      </section>

      {/* --------------------------- categories -------------------------- */}
      <section aria-labelledby="cat-heading">
        <h2
          id="cat-heading"
          className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl"
        >
          Fields covered
        </h2>

        {categories === null ? (
          <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {[0, 1, 2, 3, 4, 5].map((i) => (
              <Skeleton key={i} className="h-28" />
            ))}
          </div>
        ) : (
          <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {categories.categories.map((cat) => (
              <Card key={cat.name} className="p-5">
                <div className="flex items-start justify-between gap-3">
                  <h3 className="font-bold text-foreground">{cat.name}</h3>
                  <Badge tone="primary">{cat.career_count}</Badge>
                </div>
                <p className="mt-2 text-sm text-muted-foreground">
                  {cat.careers.slice(0, 3).join(' · ')}
                  {cat.careers.length > 3 && ' …'}
                </p>
              </Card>
            ))}
          </div>
        )}
      </section>

      {/* ------------------------------- CTA ----------------------------- */}
      <section>
        <Card glass className="p-8 text-center sm:p-12">
          <h2 className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
            Ready to see your matches?
          </h2>
          <p className="mx-auto mt-3 max-w-xl text-muted-foreground">
            The form takes about a minute. No account, no email.
          </p>
          <div className="mt-7 flex justify-center">
            <Button as={Link} to="/profile" variant="accent" size="lg">
              Start now
              <ArrowRight className="h-5 w-5" aria-hidden="true" />
            </Button>
          </div>
        </Card>
      </section>
    </div>
  );
}
