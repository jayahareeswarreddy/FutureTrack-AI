import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { X, Plus, Sparkles } from 'lucide-react';
import { getSkills, getRecommendations } from '../lib/api';
import { Button, Card, Field, inputClasses, ErrorState, cx } from './ui';

const EDUCATION_LEVELS = [
  'High school',
  'Diploma',
  'Bachelors',
  'Masters',
  'PhD',
  'Self-taught',
];

const INTEREST_OPTIONS = [
  'Artificial intelligence',
  'Web development',
  'Data analysis',
  'Cloud infrastructure',
  'Cybersecurity',
  'Mobile apps',
  'Game development',
  'Product design',
  'Research',
  'Automation',
];

/* ------------------------- skill token input -------------------------- */

/**
 * Multi-value skill input. Suggestions come from GET /skills, which ranks
 * skills by how many careers require them, so the most useful ones surface
 * first. Typed values that are not in the catalogue are still accepted.
 */
function SkillPicker({ id, skills, onChange, catalogue, error }) {
  const [draft, setDraft] = useState('');
  const [open, setOpen] = useState(false);
  const wrapRef = useRef(null);

  // Click-away closes the suggestion list.
  useEffect(() => {
    function onDocClick(e) {
      if (wrapRef.current && !wrapRef.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener('mousedown', onDocClick);
    return () => document.removeEventListener('mousedown', onDocClick);
  }, []);

  const lowered = useMemo(() => skills.map((s) => s.toLowerCase()), [skills]);

  const suggestions = useMemo(() => {
    const q = draft.trim().toLowerCase();
    if (!q) return [];
    return catalogue
      .filter((s) => s.toLowerCase().includes(q) && !lowered.includes(s.toLowerCase()))
      .slice(0, 6);
  }, [draft, catalogue, lowered]);

  function add(value) {
    const clean = value.trim();
    if (!clean) return;
    if (lowered.includes(clean.toLowerCase())) {
      setDraft('');
      return;
    }
    onChange([...skills, clean]);
    setDraft('');
    setOpen(false);
  }

  function onKeyDown(e) {
    if (e.key === 'Enter') {
      // Enter adds a skill; it must not submit the whole form.
      e.preventDefault();
      add(suggestions[0] && draft.trim() === '' ? suggestions[0] : draft);
    } else if (e.key === 'Backspace' && draft === '' && skills.length) {
      onChange(skills.slice(0, -1));
    } else if (e.key === 'Escape') {
      setOpen(false);
    }
  }

  return (
    <div ref={wrapRef} className="relative">
      {skills.length > 0 && (
        <ul className="mb-2.5 flex flex-wrap gap-2">
          {skills.map((skill) => (
            <li key={skill}>
              <span className="inline-flex items-center gap-1.5 whitespace-nowrap rounded-lg bg-primary/10 py-1 pl-3 pr-1 text-sm font-semibold text-primary">
                {skill}
                <button
                  type="button"
                  onClick={() => onChange(skills.filter((s) => s !== skill))}
                  aria-label={`Remove ${skill}`}
                  className="grid h-7 w-7 cursor-pointer place-items-center rounded-md transition-colors duration-200 hover:bg-primary/20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                >
                  <X className="h-3.5 w-3.5" aria-hidden="true" />
                </button>
              </span>
            </li>
          ))}
        </ul>
      )}

      <div className="flex gap-2">
        <input
          id={id}
          type="text"
          value={draft}
          onChange={(e) => {
            setDraft(e.target.value);
            setOpen(true);
          }}
          onKeyDown={onKeyDown}
          onFocus={() => setOpen(true)}
          placeholder="e.g. Python"
          autoComplete="off"
          role="combobox"
          aria-expanded={open && suggestions.length > 0}
          aria-autocomplete="list"
          aria-controls={`${id}-suggestions`}
          aria-invalid={error ? true : undefined}
          className={inputClasses}
        />
        <Button
          type="button"
          variant="outline"
          size="md"
          onClick={() => add(draft)}
          disabled={!draft.trim()}
          aria-label="Add skill"
        >
          <Plus className="h-4 w-4" aria-hidden="true" />
          <span className="hidden sm:inline">Add</span>
        </Button>
      </div>

      {open && suggestions.length > 0 && (
        <ul
          id={`${id}-suggestions`}
          role="listbox"
          className="absolute z-20 mt-2 w-full overflow-hidden rounded-xl border border-border bg-card shadow-lg"
        >
          {suggestions.map((s) => (
            <li key={s} role="option" aria-selected="false">
              <button
                type="button"
                onClick={() => add(s)}
                className="flex min-h-[44px] w-full cursor-pointer items-center px-4 text-left text-sm text-card-foreground transition-colors duration-200 hover:bg-muted focus-visible:bg-muted focus-visible:outline-none"
              >
                {s}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

/* ------------------------------- form --------------------------------- */

export default function ProfileForm() {
  const navigate = useNavigate();

  const [skills, setSkills] = useState([]);
  const [interests, setInterests] = useState([]);
  const [education, setEducation] = useState('');
  const [experience, setExperience] = useState('0');
  const [goals, setGoals] = useState('');

  const [catalogue, setCatalogue] = useState([]);
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    getSkills(200)
      .then((d) => !cancelled && setCatalogue(d.skills.map((s) => s.skill)))
      .catch(() => {
        // Autocomplete is a convenience; typing still works without it.
      });
    return () => {
      cancelled = true;
    };
  }, []);

  function validate() {
    const next = {};
    if (skills.length === 0) {
      next.skills = 'Add at least one skill so there is something to match on.';
    }
    const years = Number(experience);
    if (!Number.isFinite(years) || years < 0 || years > 60) {
      next.experience = 'Enter a number of years between 0 and 60.';
    }
    setErrors(next);
    return next;
  }

  async function onSubmit(e) {
    e.preventDefault();
    setSubmitError(null);

    const found = validate();
    if (Object.keys(found).length > 0) {
      // Move focus to the first field in error so the problem is unmissable.
      const firstId = Object.keys(found)[0];
      document.getElementById(firstId)?.focus();
      return;
    }

    setSubmitting(true);
    try {
      const payload = {
        skills,
        interests,
        education_level: education,
        experience_years: Number(experience),
        goals: goals.trim(),
      };
      const data = await getRecommendations(payload);
      navigate('/results', { state: { data, profile: payload } });
    } catch (err) {
      setSubmitError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  function toggleInterest(value) {
    setInterests((cur) =>
      cur.includes(value) ? cur.filter((i) => i !== value) : [...cur, value]
    );
  }

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="text-3xl font-extrabold tracking-tight text-foreground sm:text-4xl">
        Tell us what you know
      </h1>
      <p className="mt-3 text-muted-foreground">
        Only your skills are required. The more you add, the sharper the match.
      </p>

      {submitError && (
        <div className="mt-6">
          <ErrorState message={submitError} onRetry={() => setSubmitError(null)} />
        </div>
      )}

      <Card className="mt-7 p-6 sm:p-8">
        <form onSubmit={onSubmit} noValidate className="space-y-7">
          <Field
            id="skills"
            label="Your skills"
            hint="Type a skill and press Enter. Suggestions are ranked by how many careers need them."
            error={errors.skills}
            required
          >
            <SkillPicker
              skills={skills}
              onChange={(next) => {
                setSkills(next);
                if (next.length) setErrors((e) => ({ ...e, skills: undefined }));
              }}
              catalogue={catalogue}
              error={errors.skills}
            />
          </Field>

          <fieldset>
            <legend className="text-sm font-semibold text-foreground">
              What interests you?
            </legend>
            <p className="mt-2 text-sm text-muted-foreground">
              Optional. Pick any that apply.
            </p>
            <div className="mt-3 flex flex-wrap gap-2">
              {INTEREST_OPTIONS.map((option) => {
                const active = interests.includes(option);
                return (
                  <button
                    key={option}
                    type="button"
                    onClick={() => toggleInterest(option)}
                    aria-pressed={active}
                    className={cx(
                      'min-h-[44px] cursor-pointer whitespace-nowrap rounded-xl border px-4 text-sm font-semibold',
                      'transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
                      active
                        ? 'border-primary bg-primary text-on-primary'
                        : 'border-border bg-card text-muted-foreground hover:bg-muted hover:text-foreground'
                    )}
                  >
                    {option}
                  </button>
                );
              })}
            </div>
          </fieldset>

          <Field id="education" label="Highest education" hint="Optional.">
            <select
              value={education}
              onChange={(e) => setEducation(e.target.value)}
              className={cx(inputClasses, 'cursor-pointer')}
            >
              <option value="">Prefer not to say</option>
              {EDUCATION_LEVELS.map((level) => (
                <option key={level} value={level}>
                  {level}
                </option>
              ))}
            </select>
          </Field>

          <Field
            id="experience"
            label="Years of experience"
            error={errors.experience}
          >
            <input
              type="number"
              min="0"
              max="60"
              step="1"
              inputMode="numeric"
              value={experience}
              onChange={(e) => {
                setExperience(e.target.value);
                setErrors((er) => ({ ...er, experience: undefined }));
              }}
              className={inputClasses}
            />
          </Field>

          <Field
            id="goals"
            label="What are you aiming for?"
            hint="Optional. One or two sentences is plenty — this is passed to the model for the explanation."
          >
            <textarea
              rows={4}
              value={goals}
              onChange={(e) => setGoals(e.target.value)}
              maxLength={600}
              placeholder="I want to move into machine learning without starting over."
              className={cx(inputClasses, 'resize-y')}
            />
          </Field>

          <Button
            type="submit"
            variant="accent"
            size="lg"
            loading={submitting}
            className="w-full"
          >
            {!submitting && <Sparkles className="h-5 w-5" aria-hidden="true" />}
            {submitting ? 'Scoring your profile…' : 'Show my matches'}
          </Button>
        </form>
      </Card>
    </div>
  );
}
