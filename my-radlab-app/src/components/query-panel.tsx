"use client";

import { useState } from "react";

import { t, type Lang } from "@/lib/i18n";
import { cn } from "@/lib/utils";

export type ArticleStyle = "simple" | "formal";

interface QueryPanelProps {
  lang: Lang;
  query: string;
  onQueryChange: (value: string) => void;
  style: ArticleStyle;
  onStyleChange: (value: ArticleStyle) => void;
  lastDays: number;
  onLastDaysChange: (value: number) => void;
  onSubmit: () => void;
  busy: boolean;
  error: string | null;
  hasRun: boolean;
  /** Random predefined queries drawn on each page entry / refresh. */
  suggestions?: string[];
  onUseSuggestion?: (value: string) => void;
  onShuffleSuggestions?: () => void;
  /** When true the panel shrinks to a slim bar so the article owns the top. */
  collapsed?: boolean;
}

const LAST_DAYS_OPTIONS = [1, 2, 7];

export function QueryPanel({
  lang,
  query,
  onQueryChange,
  style,
  onStyleChange,
  lastDays,
  onLastDaysChange,
  onSubmit,
  busy,
  error,
  hasRun,
  suggestions = [],
  onUseSuggestion,
  onShuffleSuggestions,
  collapsed = false,
}: QueryPanelProps) {
  const [localError, setLocalError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState(true);

  function handleSubmit() {
    if (!query.trim()) {
      setLocalError(t(lang, "no_query_error"));
      return;
    }
    setLocalError(null);
    setExpanded(false);
    onSubmit();
  }

  const shownError = localError ?? error;
  const compact = collapsed && !expanded;

  if (compact) {
    return (
      <section className="panel rounded-2xl px-4 py-3 sm:px-5">
        <div className="flex flex-wrap items-center gap-3">
          <span className="inline-flex h-7 shrink-0 items-center rounded-md bg-teal-50 px-2 text-xs font-medium text-teal-700">
            01
          </span>
          <button
            onClick={() => setExpanded(true)}
            className="min-w-0 flex-1 truncate text-left text-sm text-slate-700 transition hover:text-teal-800"
            title={query}
          >
            {query}
          </button>
          <span className="hidden shrink-0 rounded-full border border-slate-200 bg-slate-50 px-2.5 py-1 text-xs text-slate-600 sm:inline">
            {t(lang, style === "simple" ? "style_simple" : "style_formal")} · {lastDays}d
          </span>
          <button
            onClick={() => setExpanded(true)}
            className="shrink-0 rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs text-teal-800 transition hover:border-teal-300 hover:bg-teal-50"
          >
            ✎ {t(lang, "btn_edit_query")}
          </button>
          <button
            onClick={handleSubmit}
            disabled={busy}
            className="shrink-0 rounded-lg bg-teal-800 px-4 py-2 text-xs font-semibold text-white transition hover:bg-teal-900 disabled:opacity-60"
          >
            {busy ? "…" : t(lang, "btn_run_again")} →
          </button>
        </div>
      </section>
    );
  }

  return (
    <section className="panel relative overflow-hidden rounded-2xl p-5 sm:p-8">
      <div className="relative">
        <div className="mb-5 flex items-center gap-3">
          <span className="inline-flex h-7 items-center rounded-md bg-teal-50 px-2 text-xs font-medium text-teal-700">
            01
          </span>
          <h2 id="query-heading" className="text-lg font-semibold tracking-tight text-slate-900">
            {t(lang, "query_label")}
          </h2>
          {collapsed && (
            <button
              onClick={() => setExpanded(false)}
              className="ml-auto rounded-lg border border-slate-200 px-3 py-2 text-xs text-slate-600 transition hover:text-slate-900"
            >
              ⌃ {t(lang, "btn_close_editor")}
            </button>
          )}
        </div>

        <label className="block">
          <textarea
            aria-labelledby="query-heading"
            value={query}
            onChange={(e) => onQueryChange(e.target.value)}
            onKeyDown={(e) => {
              if ((e.metaKey || e.ctrlKey) && e.key === "Enter") handleSubmit();
            }}
            placeholder={t(lang, "query_placeholder")}
            rows={4}
            disabled={busy}
            className="w-full resize-y rounded-xl border border-slate-300 bg-slate-50/60 px-4 py-4 text-base leading-relaxed text-slate-900 placeholder:text-slate-500 transition focus:border-teal-600 focus:bg-white disabled:opacity-60"
          />
        </label>

        {suggestions.length > 0 && (
          <div className="mt-5">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs font-medium text-slate-700">
                ✦ {t(lang, "suggestions_title")}
              </span>
              <span className="hidden text-xs text-slate-500 sm:inline">
                · {t(lang, "suggestions_hint")}
              </span>
              {onShuffleSuggestions && (
                <button
                  type="button"
                  onClick={onShuffleSuggestions}
                  className="ml-auto rounded-lg px-3 py-2 text-xs text-teal-700 transition hover:bg-teal-50 hover:text-teal-900"
                >
                  ⟳ {t(lang, "suggestions_refresh")}
                </button>
              )}
            </div>
            <div className="mt-2 flex flex-col gap-2">
              {suggestions.map((suggestion, idx) => (
                <button
                  key={`${idx}-${suggestion}`}
                  type="button"
                  disabled={busy}
                  title={suggestion}
                  onClick={() => onUseSuggestion?.(suggestion)}
                  className={cn(
                    "group flex items-start gap-3 rounded-xl border px-4 py-3 text-left text-sm leading-relaxed transition disabled:opacity-60",
                    query.trim() === suggestion.trim()
                      ? "border-teal-600 bg-teal-50 text-teal-900"
                      : "border-slate-200 bg-white text-slate-600 hover:border-teal-300 hover:bg-teal-50/50 hover:text-slate-900"
                  )}
                >
                  <span className="mt-0.5 shrink-0 text-xs text-teal-700">
                    {String(idx + 1).padStart(2, "0")}
                  </span>
                  <span className="min-w-0 flex-1">{suggestion}</span>
                  <span className="mt-px shrink-0 text-sm text-slate-400 transition group-hover:text-teal-700">
                    ↵
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}

        <div className="mt-6 grid gap-5 border-t border-slate-100 pt-6 sm:grid-cols-[1fr_auto]">
          <div>
            <span className="mb-2 block text-xs font-medium text-slate-600">
              {t(lang, "style_label")}
            </span>
            <div className="flex gap-2">
              {(["simple", "formal"] as ArticleStyle[]).map((value) => (
                <button
                  key={value}
                  type="button"
                  disabled={busy}
                  onClick={() => onStyleChange(value)}
                  aria-pressed={style === value}
                  className={cn(
                    "flex-1 rounded-xl border px-3 py-3 text-left text-sm transition disabled:opacity-60",
                    style === value
                      ? "border-teal-600 bg-teal-50 text-teal-900"
                      : "border-slate-200 bg-white text-slate-600 hover:border-slate-400 hover:text-slate-900"
                  )}
                >
                  <span className="block font-medium">
                    {value === "simple"
                      ? `✎ ${t(lang, "style_simple")}`
                      : `🏛 ${t(lang, "style_formal")}`}
                  </span>
                </button>
              ))}
            </div>
          </div>

          <div>
            <span className="mb-2 block text-xs font-medium text-slate-600">
              {t(lang, "last_days_label")}
            </span>
            <div className="flex gap-1 rounded-xl border border-slate-200 bg-slate-50 p-1">
              {LAST_DAYS_OPTIONS.map((days) => (
                <button
                  key={days}
                  type="button"
                  disabled={busy}
                  onClick={() => onLastDaysChange(days)}
                  aria-pressed={lastDays === days}
                  className={cn(
                    "min-w-12 rounded-lg px-3 py-2 text-sm transition disabled:opacity-60",
                    lastDays === days
                      ? "bg-white font-medium text-teal-800 shadow-sm"
                      : "text-slate-600 hover:bg-white hover:text-slate-900"
                  )}
                >
                  {days}d
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:items-center">
          <button
            type="button"
            onClick={handleSubmit}
            disabled={busy}
            className={cn(
              "group relative inline-flex items-center justify-center gap-3 overflow-hidden rounded-xl px-6 py-3.5 text-sm font-semibold text-white transition",
              "bg-teal-800 shadow-sm",
              "hover:bg-teal-900 disabled:cursor-not-allowed disabled:opacity-60"
            )}
          >
            <span className="relative">
              {busy ? "…" : hasRun ? t(lang, "btn_run_again") : t(lang, "btn_run")}
            </span>
            {!busy && <span className="relative">→</span>}
          </button>
          <span className="text-xs text-slate-500">
            ⌘/Ctrl + Enter
          </span>
        </div>

        {shownError && (
          <div role="alert" className="mt-4 flex items-center gap-2 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800">
            <span>⚠</span>
            {shownError}
          </div>
        )}
      </div>
    </section>
  );
}
