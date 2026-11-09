import React, { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { Search, ArrowRight, X } from 'lucide-react';
import { getCareers, getCategories } from '../lib/api';
import {
  Card,
  Badge,
  Button,
  Skeleton,
  ErrorState,
  EmptyState,
  inputClasses,
  cx,
} from './ui';

export default function CareerBrowser() {
  const [careers, setCareers] = useState(null);
  const [categories, setCategories] = useState([]);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('All');

  const load = React.useCallback(() => {
    setError(null);
    setCareers(null);
    Promise.all([getCareers(), getCategories().catch(() => null)])
      .then(([careerList, categoryData]) => {
        setCareers(careerList);
        setCategories(categoryData?.categories?.map((c) => c.name) ?? []);
      })
      .catch((err) => setError(err.message));
  }, []);

  useEffect(load, [load]);

  // Filtering runs client-side: the whole catalogue is 24 rows, so a request
  // per keystroke would add latency without adding accuracy.
  const filtered = useMemo(() => {
    if (!careers) return [];
    const q = query.trim().toLowerCase();
    return careers.filter((c) => {
      if (activeCategory !== 'All' && c.category !== activeCategory) return false;
      if (!q) return true;
      return (
        c.title.toLowerCase().includes(q) ||
        c.description.toLowerCase().includes(q) ||
        c.category.toLowerCase().includes(q) ||
        (c.required_skills || []).some((s) => s.toLowerCase().includes(q))
      );
    });
  }, [careers, query, activeCategory]);

  return (
    <div className="space-y-7">
      <div>
        <h1 className="text-3xl font-extrabold tracking-tight text-foreground sm:text-4xl">
          Browse careers
        </h1>
        <p className="mt-3 text-muted-foreground">
          Every path in the database, with the skills each one expects.
        </p>
      </div>

      {/* --------------------------- filters --------------------------- */}
      <div className="space-y-4">
        <div className="relative">
          <Search
            className="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground"
            aria-hidden="true"
          />
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by title, skill or field"
            aria-label="Search careers"
            className={cx(inputClasses, 'pl-12 pr-12')}
          />
          {query && (
            <button
              type="button"
              onClick={() => setQuery('')}
              aria-label="Clear search"
              className="absolute right-2 top-1/2 grid h-10 w-10 -translate-y-1/2 cursor-pointer place-items-center rounded-lg text-muted-foreground transition-colors duration-200 hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              <X className="h-4 w-4" aria-hidden="true" />
            </button>
          )}
        </div>

        {categories.length > 0 && (
          <div
            className="flex flex-wrap gap-2"
            role="group"
            aria-label="Filter by field"
          >
            {['All', ...categories].map((cat) => {
              const active = activeCategory === cat;
              return (
                <button
                  key={cat}
                  type="button"
                  onClick={() => setActiveCategory(cat)}
                  aria-pressed={active}
                  className={cx(
                    'min-h-[44px] cursor-pointer whitespace-nowrap rounded-xl border px-4 text-sm font-semibold',
                    'transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
                    active
                      ? 'border-primary bg-primary text-on-primary'
                      : 'border-border bg-card text-muted-foreground hover:bg-muted hover:text-foreground'
                  )}
                >
                  {cat}
                </button>
              );
            })}
          </div>
        )}
      </div>

      {/* ---------------------------- list ----------------------------- */}
      {error ? (
        <ErrorState message={error} onRetry={load} />
      ) : careers === null ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }, (_, i) => (
            <Skeleton key={i} className="h-56" />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <EmptyState
          title="No careers match that"
          description={
            query
              ? `Nothing matched "${query}". Try a broader term, or clear the filters.`
              : 'No careers in this field yet.'
          }
          action={
            <Button
              variant="outline"
              onClick={() => {
                setQuery('');
                setActiveCategory('All');
              }}
            >
              Clear filters
            </Button>
          }
        />
      ) : (
        <>
          <p className="text-sm text-muted-foreground" role="status">
            Showing {filtered.length} of {careers.length} careers
          </p>
          <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {filtered.map((career) => (
              <li key={career.id} className="animate-fade-in-up">
                <Card className="flex h-full flex-col p-5">
                  <Badge tone="primary" className="self-start">
                    {career.category}
                  </Badge>
                  <h2 className="mt-3 text-lg font-bold text-foreground">
                    {career.title}
                  </h2>
                  <p className="mt-2 flex-1 text-sm leading-relaxed text-muted-foreground">
                    {career.description}
                  </p>

                  {career.required_skills?.length > 0 && (
                    <ul className="mt-4 flex flex-wrap gap-1.5">
                      {career.required_skills.slice(0, 4).map((s) => (
                        <li key={s}>
                          <Badge>{s}</Badge>
                        </li>
                      ))}
                      {career.required_skills.length > 4 && (
                        <li>
                          <Badge>+{career.required_skills.length - 4}</Badge>
                        </li>
                      )}
                    </ul>
                  )}

                  <div className="mt-5">
                    <Button
                      as={Link}
                      to={`/careers/${career.id}`}
                      variant="outline"
                      size="sm"
                      className="w-full"
                    >
                      View roadmap
                      <ArrowRight className="h-4 w-4" aria-hidden="true" />
                    </Button>
                  </div>
                </Card>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
