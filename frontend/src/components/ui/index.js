import React from 'react';
import { Loader2, AlertCircle, Inbox } from 'lucide-react';

/** Join class names, dropping falsy entries. */
export function cx(...parts) {
  return parts.filter(Boolean).join(' ');
}

/* ------------------------------- Button ------------------------------ */

const BUTTON_VARIANTS = {
  // Accent is the conversion colour; primary is for navigation and defaults.
  accent: 'bg-accent text-on-accent hover:bg-accent-hover shadow-sm',
  primary: 'bg-primary text-on-primary hover:bg-primary-hover shadow-sm',
  outline:
    'border border-border bg-card text-card-foreground hover:bg-muted',
  ghost: 'text-muted-foreground hover:bg-muted hover:text-foreground',
};

const BUTTON_SIZES = {
  // Every size clears the 44px minimum touch target.
  sm: 'min-h-[44px] px-4 text-sm',
  md: 'min-h-[48px] px-5 text-base',
  lg: 'min-h-[52px] px-7 text-base',
};

export function Button({
  as: Tag = 'button',
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  className,
  children,
  ...rest
}) {
  const isDisabled = disabled || loading;
  return (
    <Tag
      className={cx(
        'inline-flex items-center justify-center gap-2 rounded-xl font-semibold',
        'transition-colors duration-200 cursor-pointer select-none',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        BUTTON_VARIANTS[variant],
        BUTTON_SIZES[size],
        isDisabled && 'opacity-60 pointer-events-none',
        className
      )}
      aria-busy={loading || undefined}
      disabled={Tag === 'button' ? isDisabled : undefined}
      {...rest}
    >
      {loading && <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />}
      {children}
    </Tag>
  );
}

/* -------------------------------- Card ------------------------------- */

export function Card({ className, glass = false, children, ...rest }) {
  return (
    <div
      className={cx(
        'rounded-2xl',
        glass ? 'glass' : 'bg-card border border-border shadow-sm',
        className
      )}
      {...rest}
    >
      {children}
    </div>
  );
}

/* -------------------------------- Badge ------------------------------ */

const BADGE_TONES = {
  neutral: 'bg-muted text-muted-foreground',
  primary: 'bg-primary/10 text-primary',
  accent: 'bg-accent/10 text-accent',
  success: 'bg-success/10 text-success',
  warning: 'bg-warning/10 text-warning',
};

export function Badge({ tone = 'neutral', className, children, ...rest }) {
  return (
    <span
      className={cx(
        // whitespace-nowrap stops a two-word chip breaking across lines.
        'inline-flex items-center whitespace-nowrap rounded-lg px-2.5 py-1',
        'text-xs font-semibold',
        BADGE_TONES[tone],
        className
      )}
      {...rest}
    >
      {children}
    </span>
  );
}

/* ------------------------------- Field ------------------------------- */

/**
 * Labelled form control. The label is always visible (never placeholder-only),
 * help text and errors are tied to the input through aria-describedby, and the
 * error sits next to the field it belongs to.
 */
export function Field({ id, label, hint, error, required, children }) {
  const hintId = hint ? `${id}-hint` : undefined;
  const errorId = error ? `${id}-error` : undefined;

  return (
    <div className="space-y-2">
      <label htmlFor={id} className="block text-sm font-semibold text-foreground">
        {label}
        {required && (
          <span className="text-destructive" aria-hidden="true">
            {' '}
            *
          </span>
        )}
        {required && <span className="sr-only"> (required)</span>}
      </label>
      {hint && (
        <p id={hintId} className="text-sm text-muted-foreground">
          {hint}
        </p>
      )}
      {React.cloneElement(children, {
        id,
        'aria-describedby': cx(hintId, errorId) || undefined,
        'aria-invalid': error ? true : undefined,
      })}
      {error && (
        <p
          id={errorId}
          className="flex items-center gap-1.5 text-sm font-medium text-destructive"
        >
          <AlertCircle className="h-4 w-4 shrink-0" aria-hidden="true" />
          {error}
        </p>
      )}
    </div>
  );
}

export const inputClasses =
  'w-full min-h-[48px] rounded-xl border border-border bg-card px-4 py-3 ' +
  'text-base text-foreground placeholder:text-muted-foreground ' +
  'transition-colors duration-200 ' +
  'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:border-primary';

/* ---------------------------- async states --------------------------- */

/** Skeleton block sized by the caller; reserves space so layout cannot shift. */
export function Skeleton({ className }) {
  return (
    <div
      className={cx('relative overflow-hidden rounded-xl bg-muted', className)}
      aria-hidden="true"
    >
      <div className="absolute inset-0 -translate-x-full animate-shimmer bg-gradient-to-r from-transparent via-black/5 to-transparent" />
    </div>
  );
}

export function Spinner({ label = 'Loading' }) {
  return (
    <div className="flex items-center justify-center gap-3 py-12" role="status">
      <Loader2 className="h-6 w-6 animate-spin text-primary" aria-hidden="true" />
      <span className="text-muted-foreground">{label}</span>
    </div>
  );
}

export function ErrorState({ message, onRetry }) {
  return (
    <Card className="p-6" role="alert">
      <div className="flex items-start gap-3">
        <AlertCircle
          className="mt-0.5 h-5 w-5 shrink-0 text-destructive"
          aria-hidden="true"
        />
        <div className="space-y-3">
          <p className="font-semibold text-foreground">Something went wrong</p>
          <p className="text-sm text-muted-foreground">{message}</p>
          {onRetry && (
            <Button variant="outline" size="sm" onClick={onRetry}>
              Try again
            </Button>
          )}
        </div>
      </div>
    </Card>
  );
}

export function EmptyState({ title, description, action }) {
  return (
    <Card className="p-10 text-center">
      <Inbox
        className="mx-auto h-10 w-10 text-muted-foreground"
        aria-hidden="true"
      />
      <p className="mt-4 text-lg font-semibold text-foreground">{title}</p>
      {description && (
        <p className="mx-auto mt-2 max-w-md text-sm text-muted-foreground">
          {description}
        </p>
      )}
      {action && <div className="mt-6 flex justify-center">{action}</div>}
    </Card>
  );
}

/* ------------------------------ Meter -------------------------------- */

/**
 * Horizontal percentage meter. The number is always printed next to the bar,
 * so the value does not depend on reading the colour or the length.
 */
export function Meter({ value, label, tone = 'primary' }) {
  const pct = Math.round(Math.min(Math.max(value, 0), 1) * 100);
  const barTone = tone === 'accent' ? 'bg-accent' : 'bg-primary';

  return (
    <div className="space-y-1.5">
      <div className="flex items-baseline justify-between gap-3">
        <span className="text-sm font-medium text-muted-foreground">{label}</span>
        <span className="text-sm font-bold tabular-nums text-foreground">
          {pct}%
        </span>
      </div>
      <div
        className="h-2 overflow-hidden rounded-full bg-muted"
        role="progressbar"
        aria-valuenow={pct}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={label}
      >
        <div
          className={cx('h-full rounded-full transition-all duration-500', barTone)}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
