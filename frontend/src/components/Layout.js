import React, { useEffect, useState, useCallback } from 'react';
import { Link, NavLink, useLocation } from 'react-router-dom';
import { Compass, Sun, Moon, Menu, X, Cpu, Database } from 'lucide-react';
import { getHealth } from '../lib/api';
import { cx, Badge } from './ui';

/* --------------------------- theme handling --------------------------- */

const STORAGE_KEY = 'futuretrack-theme';

function readInitialTheme() {
  try {
    const saved = window.localStorage.getItem(STORAGE_KEY);
    if (saved === 'light' || saved === 'dark') return saved;
  } catch {
    // Private browsing or blocked storage: fall through to the default.
  }
  // Light is the product default; the OS preference only decides for dark.
  if (window.matchMedia?.('(prefers-color-scheme: dark)').matches) return 'dark';
  return 'light';
}

function useTheme() {
  const [theme, setTheme] = useState(readInitialTheme);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark');
    try {
      window.localStorage.setItem(STORAGE_KEY, theme);
    } catch {
      // Not fatal — the class above has already applied for this session.
    }
  }, [theme]);

  const toggle = useCallback(
    () => setTheme((t) => (t === 'dark' ? 'light' : 'dark')),
    []
  );
  return { theme, toggle };
}

/* ------------------------- backend status chip ------------------------ */

/**
 * Shows whether the API is reachable and which optional services resolved.
 * Without this, a visitor cannot tell AI answers from rule-based ones.
 */
function BackendStatus() {
  const [health, setHealth] = useState(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let cancelled = false;
    getHealth()
      .then((h) => !cancelled && setHealth(h))
      .catch(() => !cancelled && setFailed(true));
    return () => {
      cancelled = true;
    };
  }, []);

  if (failed) {
    return (
      <Badge tone="warning" className="hidden sm:inline-flex">
        API offline
      </Badge>
    );
  }
  if (!health) return null;

  const aiDep = health.dependencies?.ai;
  const ai = aiDep?.ok;
  const db = health.dependencies?.mongodb?.ok;

  return (
    <div className="hidden items-center gap-2 sm:flex">
      <Badge tone={ai ? 'success' : 'neutral'} title={aiDep?.detail}>
        <Cpu className="mr-1 h-3 w-3" aria-hidden="true" />
        {ai ? aiDep.provider : 'Rule-based'}
      </Badge>
      <Badge tone={db ? 'success' : 'neutral'} title={health.dependencies?.mongodb?.detail}>
        <Database className="mr-1 h-3 w-3" aria-hidden="true" />
        {db ? 'MongoDB' : 'In-memory'}
      </Badge>
    </div>
  );
}

/* ------------------------------- layout ------------------------------- */

const NAV = [
  { to: '/', label: 'Home' },
  { to: '/profile', label: 'Get matched' },
  { to: '/careers', label: 'Browse careers' },
];

export default function Layout({ children }) {
  const { theme, toggle } = useTheme();
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();

  // A route change must always close the mobile menu, or back navigation
  // leaves it hanging open over the new page.
  useEffect(() => setMenuOpen(false), [location.pathname]);

  const navLinkClass = ({ isActive }) =>
    cx(
      'flex min-h-[44px] items-center rounded-xl px-3.5 text-sm font-semibold',
      'transition-colors duration-200',
      isActive
        ? 'bg-primary/10 text-primary'
        : 'text-muted-foreground hover:bg-muted hover:text-foreground'
    );

  return (
    <div className="min-h-screen">
      <div className="page-wash" aria-hidden="true" />

      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-xl focus:bg-primary focus:px-4 focus:py-3 focus:text-on-primary"
      >
        Skip to content
      </a>

      <header className="sticky top-0 z-40 glass">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
          <Link
            to="/"
            className="flex items-center gap-2.5 rounded-xl font-extrabold tracking-tight text-foreground"
          >
            <span className="grid h-9 w-9 place-items-center rounded-xl bg-primary text-on-primary">
              <Compass className="h-5 w-5" aria-hidden="true" />
            </span>
            <span className="text-lg">FutureTrack&nbsp;AI</span>
          </Link>

          <nav className="hidden items-center gap-1 md:flex" aria-label="Main">
            {NAV.map((item) => (
              <NavLink key={item.to} to={item.to} end={item.to === '/'} className={navLinkClass}>
                {item.label}
              </NavLink>
            ))}
          </nav>

          <div className="flex items-center gap-2">
            <BackendStatus />
            <button
              type="button"
              onClick={toggle}
              className="grid h-11 w-11 cursor-pointer place-items-center rounded-xl text-muted-foreground transition-colors duration-200 hover:bg-muted hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {theme === 'dark' ? (
                <Sun className="h-5 w-5" aria-hidden="true" />
              ) : (
                <Moon className="h-5 w-5" aria-hidden="true" />
              )}
            </button>
            <button
              type="button"
              onClick={() => setMenuOpen((o) => !o)}
              className="grid h-11 w-11 cursor-pointer place-items-center rounded-xl text-muted-foreground transition-colors duration-200 hover:bg-muted md:hidden focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              aria-label={menuOpen ? 'Close menu' : 'Open menu'}
              aria-expanded={menuOpen}
            >
              {menuOpen ? (
                <X className="h-5 w-5" aria-hidden="true" />
              ) : (
                <Menu className="h-5 w-5" aria-hidden="true" />
              )}
            </button>
          </div>
        </div>

        {menuOpen && (
          <nav
            className="animate-fade-in border-t border-border px-4 py-3 md:hidden"
            aria-label="Main"
          >
            <div className="flex flex-col gap-1">
              {NAV.map((item) => (
                <NavLink key={item.to} to={item.to} end={item.to === '/'} className={navLinkClass}>
                  {item.label}
                </NavLink>
              ))}
            </div>
          </nav>
        )}
      </header>

      <main id="main" className="mx-auto max-w-6xl px-4 py-10">
        {children}
      </main>

      <footer className="mt-section border-t border-border">
        <div className="mx-auto max-w-6xl px-4 py-8 text-sm text-muted-foreground">
          <p>
            FutureTrack AI — FastAPI + React + MongoDB. Match scores are
            computed deterministically; explanations come from an LLM with
            JSON-schema validation and retries.
          </p>
        </div>
      </footer>
    </div>
  );
}
